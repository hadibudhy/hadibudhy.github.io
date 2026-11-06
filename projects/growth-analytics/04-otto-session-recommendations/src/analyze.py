"""Evaluate two simple OTTO session-recommendation baselines offline."""

from __future__ import annotations

import gzip
import hashlib
import json
import random
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import matplotlib.pyplot as plt
import numpy as np

try:
    import orjson

    def loads(line: bytes) -> dict:
        return orjson.loads(line)

    def dumps(value: dict) -> bytes:
        return orjson.dumps(value)
except ImportError:
    def loads(line: bytes) -> dict:
        return json.loads(line)

    def dumps(value: dict) -> bytes:
        return json.dumps(value, separators=(",", ":")).encode("utf-8")


ROOT = Path(__file__).resolve().parents[4]
SOURCE_ZIP = ROOT / "analysis_data" / "raw" / "otto" / "otto-recsys-train.jsonl.zip"
WORK = ROOT / "analysis_data" / "processed" / "otto-session-recommendations"
RAW_VALIDATION_FILE = WORK / "validation-sessions.jsonl.gz"
VALIDATION_FILE = WORK / "validation-prefixes.jsonl.gz"
IMAGES = ROOT / "public" / "images"
METRICS_PATH = ROOT / "public" / "data" / "otto-session-recommendations-metrics.json"
MANIFEST_PATH = ROOT / "public" / "data" / "evidence" / "otto-session-recommendations.json"

ACCESSED = "2026-11-06"
HOLDOUT_DAYS = 2
SEED = 42
K = 20
ITEM_ID_CAPACITY = 2_000_000
MILLIS_PER_DAY = 24 * 60 * 60 * 1000
EVENT_TYPES = ("clicks", "carts", "orders")
TYPE_INDEX = {event_type: index for index, event_type in enumerate(EVENT_TYPES)}
WEIGHTS = {"clicks": 0.10, "carts": 0.30, "orders": 0.60}
MODEL_NAMES = ("Popularity only", "Recent session items + popularity")

sys.path.insert(0, str(ROOT))
from scripts.chart_theme import (  # noqa: E402
    ACCENT,
    HIGHLIGHT,
    MUTED,
    SECONDARY,
    add_header,
    add_source,
    style_axis,
    style_figure,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def member_name(archive: zipfile.ZipFile) -> str:
    matches = [name for name in archive.namelist() if PurePosixPath(name).name == "otto-recsys-train.jsonl"]
    if len(matches) != 1:
        raise ValueError("Source archive must contain exactly one otto-recsys-train.jsonl")
    return matches[0]


def iter_sessions(source_zip: Path, digest=None):
    with zipfile.ZipFile(source_zip) as archive:
        with archive.open(member_name(archive)) as stream:
            for line in stream:
                if digest is not None:
                    digest.update(line)
                yield loads(line)


def scan_source(source_zip: Path) -> dict:
    source_digest = hashlib.sha256()
    sessions = 0
    min_ts = None
    max_ts = None
    for session in iter_sessions(source_zip, source_digest):
        events = session["events"]
        if len(events) < 2:
            raise ValueError(f"Session {session['session']} has fewer than two events")
        sessions += 1
        start_ts = events[0]["ts"]
        end_ts = events[-1]["ts"]
        min_ts = start_ts if min_ts is None else min(min_ts, start_ts)
        max_ts = end_ts if max_ts is None else max(max_ts, end_ts)
        if sessions % 1_000_000 == 0:
            print(f"Scanned {sessions:,} sessions")
    if not sessions or max_ts is None:
        raise ValueError("Source archive contains no usable sessions")
    return {
        "sessions": sessions,
        "min_ts": min_ts,
        "max_ts": max_ts,
        "source_sha256": source_digest.hexdigest(),
    }


def create_validation_prefixes(raw_path: Path, validation_path: Path, known_items: np.ndarray) -> int:
    rng = random.Random(SEED)
    validation_sessions = 0
    with gzip.open(raw_path, "rb") as raw_in, gzip.open(validation_path, "wb") as validation_out:
        for line in raw_in:
            raw_events = loads(line)
            events = [event for event in raw_events if known_items[event[0]]]
            if len(events) < 2:
                continue
            split_index = rng.randint(1, len(events) - 1)
            prefix = events[:split_index]
            suffix = events[split_index:]
            click = next((aid for aid, event_type in suffix if event_type == TYPE_INDEX["clicks"]), None)
            carts = sorted({aid for aid, event_type in suffix if event_type == TYPE_INDEX["carts"]})
            orders = sorted({aid for aid, event_type in suffix if event_type == TYPE_INDEX["orders"]})
            recent = []
            seen = set()
            for aid, _ in reversed(prefix):
                if aid not in seen:
                    recent.append(aid)
                    seen.add(aid)
                    if len(recent) == K:
                        break
            record = {
                "recent": recent,
                "labels": {"clicks": click, "carts": carts, "orders": orders, "prefix_length": len(prefix)},
            }
            validation_out.write(dumps(record) + b"\n")
            validation_sessions += 1
    return validation_sessions


def count_training_popularity(source_zip: Path, max_ts: int, raw_validation_path: Path, validation_path: Path) -> dict:
    split_ts = max_ts - HOLDOUT_DAYS * MILLIS_PER_DAY
    counts = np.zeros((len(EVENT_TYPES), ITEM_ID_CAPACITY), dtype=np.uint32)
    buffer = [[] for _ in EVENT_TYPES]
    buffer_sessions = 0
    train_sessions = 0
    train_sessions_dropped_short = 0
    train_events = 0
    raw_validation_sessions = 0
    event_counts = {event_type: 0 for event_type in EVENT_TYPES}
    max_aid = -1

    def flush() -> None:
        nonlocal buffer_sessions
        for index, ids in enumerate(buffer):
            if ids:
                counts[index] += np.bincount(np.asarray(ids, dtype=np.int32), minlength=ITEM_ID_CAPACITY).astype(np.uint32)
                ids.clear()
        buffer_sessions = 0

    raw_validation_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(raw_validation_path, "wb") as validation_out:
        for session in iter_sessions(source_zip):
            events = session["events"]
            compact = []
            retained = []
            previous_ts = -1
            for event in events:
                event_type = event["type"]
                aid = event["aid"]
                timestamp = event["ts"]
                if event_type not in TYPE_INDEX:
                    raise ValueError(f"Unexpected event type: {event_type}")
                if timestamp < previous_ts:
                    raise ValueError(f"Session {session['session']} is not timestamp ordered")
                if aid < 0 or aid >= ITEM_ID_CAPACITY:
                    raise ValueError(f"Item ID {aid} is outside the expected OTTO ID range")
                previous_ts = timestamp
                max_aid = max(max_aid, aid)
                event_counts[event_type] += 1
                event_type_index = TYPE_INDEX[event_type]
                compact.append([aid, event_type_index])
                if timestamp < split_ts:
                    retained.append((aid, event_type_index))
            if events[0]["ts"] > split_ts:
                validation_out.write(dumps(compact) + b"\n")
                raw_validation_sessions += 1
            else:
                if len(retained) >= 2:
                    train_sessions += 1
                    train_events += len(retained)
                    for aid, event_type_index in retained:
                        buffer[event_type_index].append(aid)
                    buffer_sessions += 1
                    if buffer_sessions >= 50_000:
                        flush()
                else:
                    train_sessions_dropped_short += 1
            if (train_sessions + raw_validation_sessions) % 1_000_000 == 0:
                print(f"Split scan: {train_sessions:,} train and {raw_validation_sessions:,} validation sessions")
        flush()

    if not train_sessions or not raw_validation_sessions:
        raise ValueError("Two-day temporal split produced an empty training or validation set")
    known_items = np.any(counts > 0, axis=0)
    validation_sessions = create_validation_prefixes(raw_validation_path, validation_path, known_items)
    if not validation_sessions:
        raise ValueError("No validation sessions remain after filtering items unseen in training")
    return {
        "split_ts": split_ts,
        "train_sessions": train_sessions,
        "train_sessions_dropped_short": train_sessions_dropped_short,
        "train_events": train_events,
        "raw_validation_sessions": raw_validation_sessions,
        "validation_sessions": validation_sessions,
        "event_counts": event_counts,
        "events": sum(event_counts.values()),
        "max_aid": max_aid,
        "popularity_counts": counts,
    }


def top_items(counts: np.ndarray) -> list[list[int]]:
    result = []
    for row in counts:
        candidate_count = min(K, int(np.count_nonzero(row)))
        if not candidate_count:
            result.append([])
            continue
        candidates = np.argpartition(row, len(row) - candidate_count)[-candidate_count:]
        ordered = sorted((int(item) for item in candidates), key=lambda item: (-int(row[item]), item))
        result.append(ordered)
    return result


def fill_recent(recent: list[int], popular: list[int]) -> list[int]:
    result = list(recent[:K])
    seen = set(result)
    for aid in popular:
        if aid not in seen:
            result.append(aid)
            seen.add(aid)
            if len(result) == K:
                break
    return result


def new_metric_state() -> dict:
    return {"sessions": 0,
            "hits": {event_type: 0 for event_type in EVENT_TYPES},
            "denominator": {event_type: 0 for event_type in EVENT_TYPES}}


def score_labels(state: dict, labels: dict, predictions: dict) -> None:
    state["sessions"] += 1
    click = labels["clicks"]
    if click is not None:
        state["denominator"]["clicks"] += 1
        if click in predictions["clicks"][:K]:
            state["hits"]["clicks"] += 1
    for event_type in ("carts", "orders"):
        targets = set(labels[event_type])
        if targets:
            state["denominator"][event_type] += min(K, len(targets))
            state["hits"][event_type] += len(targets.intersection(predictions[event_type][:K]))


def recalls(state: dict) -> dict:
    by_type = {}
    for event_type in EVENT_TYPES:
        denominator = state["denominator"][event_type]
        by_type[event_type] = state["hits"][event_type] / denominator if denominator else None
    weighted = (
        sum(WEIGHTS[event_type] * by_type[event_type] for event_type in EVENT_TYPES)
        if all(by_type[event_type] is not None for event_type in EVENT_TYPES)
        else None
    )
    return {"by_type": by_type, "weighted_recall_at_20": weighted, **state}


def evaluate(validation_path: Path, popular_items: list[list[int]]) -> dict:
    metrics = {name: new_metric_state() for name in MODEL_NAMES}
    groups = {
        "short (1–3 prefix events)": {name: new_metric_state() for name in MODEL_NAMES},
        "medium (4–8 prefix events)": {name: new_metric_state() for name in MODEL_NAMES},
        "long (9+ prefix events)": {name: new_metric_state() for name in MODEL_NAMES},
    }
    sessions = 0
    with gzip.open(validation_path, "rb") as validation_in:
        for line in validation_in:
            record = loads(line)
            labels = record["labels"]
            recent = record["recent"]
            prediction = {
                "clicks": popular_items[TYPE_INDEX["clicks"]],
                "carts": popular_items[TYPE_INDEX["carts"]],
                "orders": popular_items[TYPE_INDEX["orders"]],
            }
            personalized = {
                event_type: fill_recent(recent, popular_items[TYPE_INDEX[event_type]])
                for event_type in EVENT_TYPES
            }
            score_labels(metrics[MODEL_NAMES[0]], labels, prediction)
            score_labels(metrics[MODEL_NAMES[1]], labels, personalized)

            prefix_length = labels["prefix_length"]
            group = "short (1–3 prefix events)" if prefix_length <= 3 else (
                "medium (4–8 prefix events)" if prefix_length <= 8 else "long (9+ prefix events)"
            )
            score_labels(groups[group][MODEL_NAMES[0]], labels, prediction)
            score_labels(groups[group][MODEL_NAMES[1]], labels, personalized)
            sessions += 1

    return {
        "validation_sessions": sessions,
        "models": {name: recalls(state) for name, state in metrics.items()},
        "prefix_length_groups": {
            group: {name: recalls(state) for name, state in model_states.items()}
            for group, model_states in groups.items()
        },
    }


def plot_event_mix(profile: dict) -> str:
    path = IMAGES / "otto-session-event-mix.png"
    figure, axis = plt.subplots(figsize=(10, 5.6))
    style_figure(figure)
    style_axis(axis)
    labels = ["Clicks", "Carts", "Orders"]
    values = [profile["event_counts"][event_type] / 1_000_000 for event_type in EVENT_TYPES]
    bars = axis.bar(labels, values, color=[ACCENT, SECONDARY, HIGHLIGHT], width=0.58)
    axis.set_ylabel("Events (millions)")
    axis.set_ylim(0, max(values) * 1.18)
    axis.bar_label(bars, labels=[f"{value:,.1f}M" for value in values], padding=4, fontsize=10)
    add_header(figure, "OTTO session data", "2022 anonymized webshop and app events in the released training file")
    add_source(figure, "OTTO Recommender Systems Dataset; training file")
    figure.subplots_adjust(top=0.78, bottom=0.15, left=0.10, right=0.96)
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return "/images/otto-session-event-mix.png"


def plot_recall(metrics: dict) -> str:
    path = IMAGES / "otto-baseline-recall.png"
    figure, axis = plt.subplots(figsize=(10, 5.6))
    style_figure(figure)
    style_axis(axis)
    x = np.arange(len(EVENT_TYPES))
    width = 0.34
    colors = [ACCENT, SECONDARY]
    for index, name in enumerate(MODEL_NAMES):
        values = [metrics["models"][name]["by_type"][event_type] for event_type in EVENT_TYPES]
        bars = axis.bar(x + (index - 0.5) * width, values, width, label=name, color=colors[index])
        axis.bar_label(bars, labels=[f"{value:.3f}" for value in values], padding=3, fontsize=9)
    axis.set_xticks(x, ["Next click", "Cart items", "Ordered items"])
    axis.set_ylabel("Recall@20 (OTTO formula)")
    axis.set_ylim(0, 1.08)
    axis.legend(frameon=False, loc="upper left")
    add_header(
        figure,
        "Baseline Recall@20 by action type",
        f"Offline two-day holdout ({metrics['validation_sessions']:,} sessions); popularity uses training-period events only",
    )
    add_source(figure, "OTTO training sessions; OTTO Recall@20 formula")
    figure.subplots_adjust(top=0.78, bottom=0.16, left=0.10, right=0.97)
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return "/images/otto-baseline-recall.png"


def plot_prefix_groups(metrics: dict) -> str:
    path = IMAGES / "otto-prefix-context-recall.png"
    figure, axis = plt.subplots(figsize=(10, 5.6))
    style_figure(figure)
    style_axis(axis)
    groups = list(metrics["prefix_length_groups"])
    x = np.arange(len(groups))
    width = 0.34
    colors = [ACCENT, SECONDARY]
    for index, name in enumerate(MODEL_NAMES):
        raw_values = [metrics["prefix_length_groups"][group][name]["weighted_recall_at_20"] for group in groups]
        values = [np.nan if value is None else value for value in raw_values]
        bars = axis.bar(x + (index - 0.5) * width, values, width, label=name, color=colors[index])
        axis.bar_label(bars, labels=["—" if value is None else f"{value:.3f}" for value in raw_values], padding=3, fontsize=9)
    group_labels = ["Short", "Medium", "Long"]
    axis.set_xticks(x, [
        f"{label}\n(n={metrics['prefix_length_groups'][group][MODEL_NAMES[0]]['sessions']:,})"
        for label, group in zip(group_labels, groups)
    ])
    axis.set_ylabel("Weighted Recall@20")
    axis.set_ylim(0, 1.08)
    axis.legend(frameon=False, loc="upper left")
    add_header(figure, "Recall@20 by visible prefix length", "Validation groups by observed prefix size; cutoffs are descriptive")
    add_source(figure, "OTTO training sessions; OTTO competition Recall@20")
    figure.subplots_adjust(top=0.78, bottom=0.16, left=0.10, right=0.97)
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return "/images/otto-prefix-context-recall.png"


def write_outputs(profile: dict, split: dict, metrics: dict, source_hash: str) -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    artifacts = [plot_event_mix(profile), plot_recall(metrics), plot_prefix_groups(metrics)]
    summary = {
        "caseId": "otto-session-recommendations",
        "source": {
            "name": "OTTO Recommender Systems Dataset, training file",
            "url": "https://www.kaggle.com/datasets/otto/recsys-dataset",
            "publisher": "OTTO (GmbH & Co KG)",
            "accessed": ACCESSED,
            "license": "CC BY 4.0",
            "sha256": source_hash,
            "source_file": "otto-recsys-train.jsonl",
            "archive_file": SOURCE_ZIP.name,
        },
        "data": profile,
        "validation": {
            "holdout_days": HOLDOUT_DAYS,
            "seed": SEED,
            "cutoff_utc": datetime.fromtimestamp(split["split_ts"] / 1000, timezone.utc).isoformat(),
            "train_sessions": split["train_sessions"],
            "train_sessions_dropped_short": split["train_sessions_dropped_short"],
            "train_events": split["train_events"],
            "raw_validation_sessions": split["raw_validation_sessions"],
            "validation_sessions_dropped_after_filter": split["raw_validation_sessions"] - metrics["validation_sessions"],
            **metrics,
        },
        "method": {
            "popularity": "Top training-period item interaction counts by event type.",
            "recent_session_items_plus_popularity": "Up to 20 most recent distinct item IDs in the visible session prefix, filled with event-type popularity.",
            "metric": "OTTO weighted Recall@20: 0.10 clicks + 0.30 carts + 0.60 orders.",
        },
        "artifacts": artifacts,
    }
    METRICS_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    artifact_hashes = {artifact: sha256(ROOT / "public" / artifact.lstrip("/")) for artifact in artifacts}
    manifest = {
        "schemaVersion": 2,
        "caseId": "otto-session-recommendations",
        "status": "verified",
        "source": {
            "name": "OTTO Recommender Systems Dataset, training file",
            "url": "https://www.kaggle.com/datasets/otto/recsys-dataset",
            "publisher": "OTTO (GmbH & Co KG)",
            "accessed": ACCESSED,
            "grain": "one anonymized session with timestamped click, cart, and order events",
            "period": f"{datetime.fromtimestamp(profile['min_ts'] / 1000, timezone.utc).date()} through {datetime.fromtimestamp(profile['max_ts'] / 1000, timezone.utc).date()}",
            "rows": profile["sessions"],
            "sha256": source_hash,
            "file": "otto-recsys-train.jsonl",
            "archiveFile": SOURCE_ZIP.name,
            "license": "CC BY 4.0",
            "publicDataOnly": True,
            "mutableSource": True,
        },
        "validation": {
            "holdout": {
                "train_sessions": split["train_sessions"],
                "train_sessions_dropped_short": split["train_sessions_dropped_short"],
                "raw_validation_sessions": split["raw_validation_sessions"],
                "validation_sessions_scored": metrics["validation_sessions"],
                "validation_sessions_dropped_after_filter": split["raw_validation_sessions"] - metrics["validation_sessions"],
            },
            "checks": [
                f"all {profile['sessions']:,} sessions and {profile['events']:,} events in the pinned training file were parsed",
                f"a {HOLDOUT_DAYS}-day validation horizon was created from the latest training timestamps using seed {SEED}",
                f"{split['train_sessions_dropped_short']:,} training sessions with fewer than two pre-cutoff events were excluded, matching OTTO's split helper",
                f"{split['raw_validation_sessions'] - metrics['validation_sessions']:,} holdout sessions were removed after filtering unknown items or sessions shorter than two events",
                "item popularity counts use only sessions and events before the temporal cutoff",
                "validation predictions use only the visible prefix of each session",
                "click ground truth is the next click; cart and order ground truth are distinct future item IDs",
                "Recall@20 uses pooled hits and denominators with official 0.10, 0.30, and 0.60 action weights",
            ],
            "results": metrics["models"],
        },
        "artifacts": artifacts,
        "artifactHashes": artifact_hashes,
        "evidenceBoundary": "Offline ranking metrics on a historical public release do not measure impressions, assignment, CTR or purchase lift, revenue, margin, or current OTTO production performance.",
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if not SOURCE_ZIP.is_file():
        raise SystemExit(
            f"Missing {SOURCE_ZIP}. Download the official training file with: "
            "kaggle datasets download -d otto/recsys-dataset -f otto-recsys-train.jsonl -p analysis_data/raw/otto"
        )
    WORK.mkdir(parents=True, exist_ok=True)
    print("Scanning source profile")
    profile = scan_source(SOURCE_ZIP)
    source_hash = profile["source_sha256"]
    if MANIFEST_PATH.is_file():
        previous = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        expected_hash = previous.get("source", {}).get("sha256")
        if previous.get("caseId") != "otto-session-recommendations" or expected_hash != source_hash:
            raise SystemExit(
                f"OTTO training file hash changed: expected {expected_hash}, got {source_hash}. "
                "Review the new source and findings before updating the evidence manifest."
            )
    print("Building training-only popularity and temporal validation prefixes")
    split = count_training_popularity(SOURCE_ZIP, profile["max_ts"], RAW_VALIDATION_FILE, VALIDATION_FILE)
    profile["events"] = split["events"]
    profile["event_counts"] = split["event_counts"]
    profile["max_aid"] = split["max_aid"]
    print(f"Source: {profile['sessions']:,} sessions, {profile['events']:,} events")
    print("Evaluating popularity and recent-session baselines")
    metrics = evaluate(VALIDATION_FILE, top_items(split["popularity_counts"]))
    split.pop("popularity_counts")
    write_outputs(profile, split, metrics, source_hash)
    print(json.dumps({"source": profile, "validation": metrics}, indent=2))
    print(f"Wrote {METRICS_PATH.relative_to(ROOT)} and {MANIFEST_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
