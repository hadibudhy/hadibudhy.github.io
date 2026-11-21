"""Evaluate lexical ranking baselines on Amazon's ESCI Task 1 data."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import polars as pl
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "analysis_data" / "raw"
REFERENCE = RAW / "amazon-esci-reference"
EXAMPLES = REFERENCE / "shopping_queries_dataset" / "shopping_queries_dataset_examples.parquet"
PRODUCTS = RAW / "amazon-esci-products.parquet"
IMAGES = ROOT / "public" / "images"
METRICS_PATH = ROOT / "public" / "data" / "amazon-search-ranking-metrics.json"
MANIFEST_PATH = ROOT / "public" / "data" / "evidence" / "amazon-search-ranking.json"

ACCESS_DATE = "2026-11-07"
SEED = 42
TOP_K = 10
LABELS = ("E", "S", "C", "I")
ESCI_GAIN = {"E": 1.0, "C": 0.1, "S": 0.01, "I": 0.0}
FIELDS = ("product_title", "product_bullet_point", "product_description", "product_brand", "product_color")
TOKEN_RE = re.compile(r"[^\W_]+", flags=re.UNICODE)
EXPECTED_SHA256 = {
    "examples": "4a735b693b4a424a6fc67f5be6e4c811495c488bbf66d02a602d308b2744263a",
    "products": "25124442d064d64b26f74082d6fa09438d679efc0c183cf28d19064a2b65a265",
}
WEIGHT_GRID = tuple(
    (1.0, bullet, description, brand, color)
    for bullet, description, brand, color in itertools.product(
        (0.0, 0.5, 1.0), (0.0, 0.5), (0.0, 0.5), (0.0, 0.5)
    )
)

sys.path.insert(0, str(ROOT))
from scripts.chart_theme import (  # noqa: E402
    ACCENT,
    BORDER,
    HIGHLIGHT,
    MUTED,
    SECONDARY,
    WARNING,
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


def tokenize(value: str | None) -> set[str]:
    if not value:
        return set()
    return set(TOKEN_RE.findall(unicodedata.normalize("NFKC", value).casefold()))


def load_examples() -> tuple[pl.DataFrame, dict, dict]:
    columns = ["query_id", "query", "product_id", "product_locale", "esci_label", "small_version", "split"]
    frame = pl.read_parquet(EXAMPLES, columns=columns).filter(
        (pl.col("small_version") == 1) & (pl.col("product_locale") == "us")
    )
    if frame.is_empty():
        raise ValueError("The US small-version Task 1 slice is empty")

    inconsistent = frame.group_by("query_id").agg(
        pl.col("query").n_unique().alias("query_texts"),
        pl.col("split").n_unique().alias("splits"),
    ).filter((pl.col("query_texts") != 1) | (pl.col("splits") != 1))
    if inconsistent.height:
        raise ValueError(f"Found {inconsistent.height} query IDs with inconsistent text or split")

    queries = frame.select("query_id", "query", "split").unique(subset=["query_id"]).sort("query_id").to_dicts()
    query_text = {row["query_id"]: row["query"] for row in queries}
    query_split = {row["query_id"]: row["split"] for row in queries}
    return frame, query_text, query_split


def split_training_queries(query_split: dict) -> tuple[set, set, set]:
    train_queries = sorted((qid for qid, split in query_split.items() if split == "train"), key=str)
    test_queries = {qid for qid, split in query_split.items() if split == "test"}
    if set(train_queries).intersection(test_queries):
        raise ValueError("The supplied train and test query groups overlap")
    random.Random(SEED).shuffle(train_queries)
    tuning_count = max(1, round(len(train_queries) * 0.20))
    tuning_queries = set(train_queries[:tuning_count])
    calibration_queries = set(train_queries[tuning_count:])
    if not tuning_queries or not calibration_queries or not test_queries:
        raise ValueError("The query-disjoint calibration, tuning, and test sets must be nonempty")
    return calibration_queries, tuning_queries, test_queries


def make_query_weights(query_text: dict, calibration_queries: set) -> dict:
    tokens_by_query = {query_id: tokenize(text) for query_id, text in query_text.items()}
    document_frequency = Counter()
    for query_id in calibration_queries:
        document_frequency.update(tokens_by_query[query_id])
    document_count = len(calibration_queries)
    fallback_idf = math.log(document_count + 1) + 1.0
    idf = {token: math.log((document_count + 1) / (frequency + 1)) + 1.0
           for token, frequency in document_frequency.items()}
    result = {}
    for query_id, terms in tokens_by_query.items():
        weighted_terms = [(term, idf.get(term, fallback_idf)) for term in sorted(terms)]
        result[query_id] = (weighted_terms, sum(weight for _, weight in weighted_terms))
    return result


def product_match_features(frame: pl.DataFrame, query_weights: dict) -> tuple[np.ndarray, dict]:
    product_ids = frame.get_column("product_id").to_list()
    locales = frame.get_column("product_locale").to_list()
    query_ids = frame.get_column("query_id").to_list()
    rows_by_product = defaultdict(list)
    for row_index, key in enumerate(zip(locales, product_ids)):
        rows_by_product[key].append(row_index)

    candidate_ids = {product_id for _, product_id in rows_by_product}
    candidate_values = pa.array(sorted(candidate_ids), type=pa.string())
    parquet = pq.ParquetFile(PRODUCTS)
    features = np.zeros((frame.height, len(FIELDS)), dtype=np.float32)
    matched_products = set()
    empty_fields = Counter()
    columns = ["product_id", "product_locale", *FIELDS]

    for batch in parquet.iter_batches(columns=columns, batch_size=32768):
        mask = pc.and_(
            pc.equal(batch.column("product_locale"), "us"),
            pc.is_in(batch.column("product_id"), value_set=candidate_values),
        )
        for product in batch.filter(mask).to_pylist():
            product_key = (product["product_locale"], product["product_id"])
            if product_key in matched_products:
                raise ValueError(f"Duplicate product metadata row for {product_key}")
            matched_products.add(product_key)
            field_tokens = [tokenize(product.get(field)) for field in FIELDS]
            empty_fields.update(field for field in FIELDS if not product.get(field))
            for row_index in rows_by_product[product_key]:
                weighted_terms, denominator = query_weights[query_ids[row_index]]
                if denominator:
                    for field_index, terms in enumerate(field_tokens):
                        features[row_index, field_index] = sum(
                            weight for term, weight in weighted_terms if term in terms
                        ) / denominator

    missing_keys = set(rows_by_product).difference(matched_products)
    metadata = {
        "candidate_products": len(rows_by_product),
        "matched_products": len(matched_products),
        "missing_products": len(missing_keys),
        "pairs_without_product_metadata": sum(len(rows_by_product[key]) for key in missing_keys),
        "empty_product_fields": dict(empty_fields),
    }
    return features, metadata


def groups_by_query(query_ids: list) -> dict:
    groups = defaultdict(list)
    for row_index, query_id in enumerate(query_ids):
        groups[query_id].append(row_index)
    return dict(groups)


def query_ndcg_values(query_set: set, groups: dict, scores: np.ndarray,
                      product_ids: list, labels: list, cutoff: int | None = None) -> tuple[list[float], int]:
    query_scores = []
    zero_ideal_queries = 0
    for query_id in sorted(query_set, key=str):
        indices = groups[query_id]
        ranked = sorted(indices, key=lambda index: (-float(scores[index]), str(product_ids[index])))
        gains = [ESCI_GAIN[labels[index]] for index in indices]
        ideal = sorted(gains, reverse=True)
        limit = len(indices) if cutoff is None else min(cutoff, len(indices))
        denominator = sum(gain / math.log2(rank + 2) for rank, gain in enumerate(ideal[:limit]))
        if denominator == 0:
            zero_ideal_queries += 1
            query_scores.append(0.0)
            continue
        dcg = sum(ESCI_GAIN[labels[index]] / math.log2(rank + 2)
                  for rank, index in enumerate(ranked[:limit]))
        query_scores.append(dcg / denominator)
    return query_scores, zero_ideal_queries


def ndcg_for_queries(query_set: set, groups: dict, scores: np.ndarray,
                     product_ids: list, labels: list, cutoff: int | None = None) -> dict:
    query_scores, zero_ideal_queries = query_ndcg_values(query_set, groups, scores, product_ids, labels, cutoff)
    return {
        "mean_ndcg": float(np.mean(query_scores)) if query_scores else 0.0,
        "queries": len(query_scores),
        "zero_ideal_queries": zero_ideal_queries,
    }


def evaluate_scores(query_set: set, groups: dict, scores: np.ndarray,
                    product_ids: list, labels: list) -> dict:
    full = ndcg_for_queries(query_set, groups, scores, product_ids, labels)
    top10 = ndcg_for_queries(query_set, groups, scores, product_ids, labels, cutoff=10)
    return {
        "official_full_ndcg": full["mean_ndcg"],
        "local_ndcg_at_10": top10["mean_ndcg"],
        "queries": full["queries"],
        "zero_ideal_queries": full["zero_ideal_queries"],
    }


def top10_label_counts(query_set: set, groups: dict, scores: np.ndarray,
                       product_ids: list, labels: list) -> dict:
    counts = Counter()
    total = 0
    for query_id in sorted(query_set, key=str):
        ranked = sorted(groups[query_id], key=lambda index: (-float(scores[index]), str(product_ids[index])))[:TOP_K]
        counts.update(labels[index] for index in ranked)
        total += len(ranked)
    return {label: {"count": counts[label], "share": counts[label] / total if total else 0.0} for label in LABELS}


def weight_grid() -> list[tuple[float, ...]]:
    return [
        (1.0, bullet, description, brand, color)
        for bullet, description, brand, color in itertools.product(
            (0.0, 0.5, 1.0), (0.0, 0.5), (0.0, 0.5), (0.0, 0.5)
        )
    ]


def choose_field_weights(features: np.ndarray, query_ids: list, product_ids: list,
                         labels: list, groups: dict, tuning_queries: set) -> dict:
    best_weights = None
    best_score = -1.0
    grid_results = []
    for weights in weight_grid():
        scores = features @ np.asarray(weights, dtype=np.float32)
        score = ndcg_for_queries(tuning_queries, groups, scores, product_ids, labels)["mean_ndcg"]
        grid_results.append({"weights": list(weights), "tuning_ndcg": score})
        if score > best_score + 1e-12:
            best_score = score
            best_weights = weights
    return {"weights": list(best_weights), "tuning_ndcg": best_score, "grid": grid_results}


def paired_query_bootstrap(baseline: list[float], candidate: list[float]) -> dict:
    differences = np.asarray(candidate, dtype=np.float64) - np.asarray(baseline, dtype=np.float64)
    rng = np.random.default_rng(SEED)
    bootstrap_means = np.empty(2000, dtype=np.float64)
    for index in range(len(bootstrap_means)):
        sample = rng.integers(0, len(differences), size=len(differences))
        bootstrap_means[index] = differences[sample].mean()
    lower, upper = np.quantile(bootstrap_means, [0.025, 0.975])
    return {
        "mean_delta": float(differences.mean()),
        "confidence_interval_95": [float(lower), float(upper)],
        "queries": len(differences),
        "replicates": len(bootstrap_means),
        "seed": SEED,
    }


def label_distribution(query_ids: list, labels: list, query_split: dict) -> dict:
    result = {split: {label: 0 for label in LABELS} for split in ("train", "test")}
    for query_id, label in zip(query_ids, labels):
        result[query_split[query_id]][label] += 1
    return result


def plot_label_distribution(distribution: dict) -> str:
    path = ROOT / "public" / "images" / "amazon-esci-label-distribution.png"
    label_names = {"E": "Exact", "S": "Substitute", "C": "Complement", "I": "Irrelevant"}
    colors = {"E": ACCENT, "S": SECONDARY, "C": WARNING, "I": BORDER}
    splits = ("train", "test")
    totals = {split: sum(distribution[split].values()) for split in splits}
    bottoms = np.zeros(len(splits))
    figure, axis = plt.subplots(figsize=(10, 5.6))
    style_figure(figure)
    style_axis(axis)
    for label in LABELS:
        values = np.asarray([distribution[split][label] / totals[split] for split in splits])
        axis.bar(["Train", "Test"], values, bottom=bottoms, color=colors[label], label=label_names[label], width=0.54)
        bottoms += values
    axis.set_ylabel("Share of query–product judgments")
    axis.set_ylim(0, 1)
    axis.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    add_header(figure, "Relevance labels in the US Task 1 slice", "Amazon's reduced query-ranking set; split by query ID")
    add_source(figure, "Amazon Shopping Queries Dataset (ESCI), small_version=1")
    figure.subplots_adjust(top=0.78, bottom=0.24, left=0.11, right=0.96)
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return "/images/amazon-esci-label-distribution.png"


def plot_ndcg(results: dict) -> str:
    path = ROOT / "public" / "images" / "amazon-search-ranking-ndcg.png"
    models = list(results)
    metric_keys = ("official_full_ndcg", "local_ndcg_at_10")
    metric_labels = ("Full nDCG (official gains)", "nDCG@10 (local view)")
    x = np.arange(len(metric_keys))
    width = 0.34
    colors = [ACCENT, SECONDARY]
    figure, axis = plt.subplots(figsize=(10, 5.6))
    style_figure(figure)
    style_axis(axis)
    for index, model in enumerate(models):
        values = [results[model][key] for key in metric_keys]
        bars = axis.bar(x + (index - 0.5) * width, values, width, label=model, color=colors[index])
        axis.bar_label(bars, labels=[f"{value:.3f}" for value in values], padding=3, fontsize=9)
    axis.set_xticks(x, metric_labels)
    axis.set_ylabel("Mean query nDCG")
    maximum = max(value for model in models for value in (results[model][key] for key in metric_keys))
    axis.set_ylim(0, max(0.1, min(1.08, maximum * 1.2)))
    axis.legend(frameon=False, loc="upper left")
    add_header(figure, "Lexical ranking quality on held-out queries", "Field weights selected using training queries only")
    add_source(figure, "Amazon ESCI Task 1, US locale; official gain mapping")
    figure.subplots_adjust(top=0.78, bottom=0.18, left=0.11, right=0.97)
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return "/images/amazon-search-ranking-ndcg.png"


def plot_top10_labels(top10: dict) -> str:
    path = ROOT / "public" / "images" / "amazon-search-top10-labels.png"
    label_names = {"E": "Exact", "S": "Substitute", "C": "Complement", "I": "Irrelevant"}
    colors = {"E": ACCENT, "S": SECONDARY, "C": WARNING, "I": BORDER}
    models = list(top10)
    y = np.arange(len(models))
    left = np.zeros(len(models))
    figure, axis = plt.subplots(figsize=(10, 5.6))
    style_figure(figure)
    style_axis(axis)
    for label in LABELS:
        values = np.asarray([top10[model][label]["share"] for model in models])
        axis.barh(y, values, left=left, color=colors[label], label=label_names[label], height=0.54)
        left += values
    axis.set_yticks(y, models)
    axis.set_xlim(0, 1)
    axis.set_xlabel("Share of ranked top-10 candidates")
    axis.invert_yaxis()
    axis.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.16))
    add_header(figure, "What appears in the top ten?", "Test-query candidates grouped by human ESCI relevance label")
    add_source(figure, "Amazon ESCI Task 1, US locale")
    figure.subplots_adjust(top=0.78, bottom=0.26, left=0.31, right=0.97)
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return "/images/amazon-search-top10-labels.png"


def write_outputs(rows: pl.DataFrame, query_split: dict, hashes: dict, product_coverage: dict,
                  calibration_qids: set, tune_qids: set, test_qids: set, tuning: dict,
                  results: dict, top10: dict, distribution: dict, paired_delta: dict) -> None:
    artifacts = [plot_label_distribution(distribution), plot_ndcg(results), plot_top10_labels(top10)]
    data = {
        "caseId": "amazon-search-relevance",
        "source": {
            "publisher": "Amazon Science",
            "dataset": "Shopping Queries Dataset (ESCI), Task 1 small version",
            "release_year": 2022,
            "license": "Apache-2.0",
            "accessed": ACCESS_DATE,
            "examples_sha256": hashes["examples"],
            "products_sha256": hashes["products"],
        },
        "scope": {
            "locale": "us",
            "query_product_pairs": rows.height,
            "train_queries": sum(split == "train" for split in query_split.values()),
            "test_queries": len(test_qids),
            "calibration_queries": len(calibration_qids),
            "tuning_queries": len(tune_qids),
            "product_metadata": product_coverage,
            "label_distribution": distribution,
        },
        "model_selection": {
            "seed": SEED,
            "selected_field_weights": dict(zip(FIELDS, tuning["weights"])),
            "tuning_ndcg": tuning["tuning_ndcg"],
            "grid": tuning["grid"],
        },
        "test_results": results,
        "paired_query_bootstrap_delta": paired_delta,
        "test_top10_label_counts": top10,
        "metric": {
            "official_gain_map": ESCI_GAIN,
            "official_full_ndcg": "Per-query nDCG averaged over provided test queries with Amazon's TREC gain mapping.",
            "local_ndcg_at_10": "Top-10 nDCG with the same gain mapping; a custom local view.",
        },
        "artifacts": artifacts,
    }
    metrics_path = ROOT / "public" / "data" / "amazon-search-ranking-metrics.json"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    artifact_hashes = {path: sha256(ROOT / "public" / path.lstrip("/")) for path in artifacts}
    manifest = {
        "schemaVersion": 2,
        "caseId": "amazon-search-relevance",
        "status": "verified",
        "source": {
            "name": "Amazon Shopping Queries Dataset, Task 1 small version, US locale",
            "url": "https://github.com/amazon-science/esci-data",
            "publisher": "Amazon Science",
            "accessed": ACCESS_DATE,
            "period": "2022 public benchmark; no per-query timestamp field",
            "grain": "query ID × preselected product candidate × human relevance judgment",
            "rows": rows.height,
            "examplesSha256": hashes["examples"],
            "productsSha256": hashes["products"],
            "license": "Apache-2.0",
            "publicDataOnly": True,
            "mutableSource": True,
        },
        "validation": {
            "checks": [
                f"the US small-version slice contains {rows.height:,} query-product judgments",
                f"the provided query split contains {len(test_qids):,} held-out test queries and no query IDs overlap train",
                f"field weights were selected using {len(tune_qids):,} training queries after IDF calibration on {len(calibration_qids):,} separate training queries",
                "product metadata is matched using product_locale and product_id",
                "test labels were not used to select tokenization, field weights, or tie-breaking",
                "official full nDCG uses Amazon's TREC gain mapping and query-level macro averaging",
                "nDCG@10 is reported only as a custom local top-10 view",
            ],
            "testResults": results,
            "pairedQueryBootstrapDelta": paired_delta,
            "selectedFieldWeights": dict(zip(FIELDS, tuning["weights"])),
            "productMetadataCoverage": product_coverage,
        },
        "artifacts": artifacts,
        "artifactHashes": artifact_hashes,
        "evidenceBoundary": "Offline reranking of preselected, human-judged candidates does not evaluate full-catalog retrieval, user exposure, CTR, purchases, or sales impact.",
    }
    manifest_path = ROOT / "public" / "data" / "evidence" / "amazon-search-ranking.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    for path in (EXAMPLES, PRODUCTS):
        if not path.is_file():
            raise SystemExit(f"Missing {path}. See the project README for the official data download steps.")
    hashes = {"examples": sha256(EXAMPLES), "products": sha256(PRODUCTS)}
    for name, digest in hashes.items():
        if digest != EXPECTED_SHA256[name]:
            raise SystemExit(f"Amazon ESCI {name} file hash mismatch: expected {EXPECTED_SHA256[name]}, got {digest}")

    print("Loading Amazon Task 1, US query-product judgments")
    rows, query_text, query_split = load_examples()
    calibration_qids, tune_qids, test_qids = split_training_queries(query_split)

    print("Estimating query IDF on calibration queries")
    query_weights = make_query_weights(query_text, calibration_qids)
    print("Joining product text and scoring lexical fields")
    features, product_coverage = product_match_features(rows, query_weights)

    query_ids = rows.get_column("query_id").to_list()
    product_ids = rows.get_column("product_id").to_list()
    labels = rows.get_column("esci_label").to_list()
    invalid_labels = set(labels).difference(LABELS)
    if invalid_labels:
        raise ValueError(f"Unexpected ESCI labels: {sorted(invalid_labels)}")
    groups = groups_by_query(query_ids)
    title_scores = features[:, 0]

    print("Selecting field weights on a held-out subset of train queries")
    tuning = choose_field_weights(features, query_ids, product_ids, labels, groups, tune_qids)
    field_scores = features @ np.asarray(tuning["weights"], dtype=np.float32)
    results = {
        "Title-only token coverage": evaluate_scores(test_qids, groups, title_scores, product_ids, labels),
        "Train-tuned field-weighted lexical": evaluate_scores(test_qids, groups, field_scores, product_ids, labels),
    }
    title_full, _ = query_ndcg_values(test_qids, groups, title_scores, product_ids, labels)
    field_full, _ = query_ndcg_values(test_qids, groups, field_scores, product_ids, labels)
    title_top10, _ = query_ndcg_values(test_qids, groups, title_scores, product_ids, labels, cutoff=TOP_K)
    field_top10, _ = query_ndcg_values(test_qids, groups, field_scores, product_ids, labels, cutoff=TOP_K)
    paired_delta = {
        "official_full_ndcg": paired_query_bootstrap(title_full, field_full),
        "local_ndcg_at_10": paired_query_bootstrap(title_top10, field_top10),
    }
    top10 = {
        "Title-only token coverage": top10_label_counts(test_qids, groups, title_scores, product_ids, labels),
        "Train-tuned field-weighted lexical": top10_label_counts(test_qids, groups, field_scores, product_ids, labels),
    }
    distribution = label_distribution(query_ids, labels, query_split)
    print(json.dumps({"results": results, "weights": tuning["weights"], "product_coverage": product_coverage}, indent=2))
    write_outputs(rows, query_split, hashes, product_coverage, calibration_qids, tune_qids, test_qids,
                  tuning, results, top10, distribution, paired_delta)


if __name__ == "__main__":
    main()
