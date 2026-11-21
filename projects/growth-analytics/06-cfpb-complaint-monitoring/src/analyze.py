"""Build a privacy-minimal complaint monitoring snapshot from the CFPB API."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import requests
from matplotlib.ticker import FuncFormatter, PercentFormatter


ROOT = Path(__file__).resolve().parents[4]
IMAGES = ROOT / "public" / "images"
METRICS_PATH = ROOT / "public" / "data" / "cfpb-complaint-monitoring-metrics.json"
MANIFEST_PATH = ROOT / "public" / "data" / "evidence" / "cfpb-complaint-monitoring.json"
API_URL = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
COMPANY = "TRANSUNION INTERMEDIATE HOLDINGS, INC."
PRODUCT = "Credit reporting or other personal consumer reports"
START_YEAR, START_MONTH = 2025, 1
# The October 2026 form update changed product/issue options on October 29.
END_YEAR, END_MONTH = 2026, 9
ACCESS_DATE = date.today().isoformat()

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


def month_bounds(year: int, month: int) -> tuple[str, str]:
    start = f"{year:04d}-{month:02d}-01"
    if month == 12:
        end = f"{year + 1:04d}-01-01"
    else:
        end = f"{year:04d}-{month + 1:02d}-01"
    return start, end


def month_range() -> list[tuple[int, int]]:
    values = []
    year, month = START_YEAR, START_MONTH
    while (year, month) <= (END_YEAR, END_MONTH):
        values.append((year, month))
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return values


def facet_counts(payload: dict, name: str, total: int) -> dict[str, int]:
    buckets = payload.get("aggregations", {}).get(name, {}).get(name, {}).get("buckets", [])
    counts = {str(bucket["key"]): int(bucket["doc_count"]) for bucket in buckets}
    remainder = total - sum(counts.values())
    if remainder != 0:
        raise ValueError(f"{name} facet leaves {remainder:,} complaint counts unexplained")
    return counts


def fetch_month(session: requests.Session, year: int, month: int) -> tuple[dict, dict]:
    start, end = month_bounds(year, month)
    response = session.get(
        API_URL,
        params={
            "size": 1,
            "date_received_min": start,
            "date_received_max": end,
            "company": COMPANY,
            "product": PRODUCT,
        },
        timeout=90,
    )
    response.raise_for_status()
    payload = response.json()
    if payload["hits"]["total"].get("relation") != "eq":
        raise ValueError(f"CFPB API returned an approximate total for {start}")
    total = int(payload["hits"]["total"]["value"])
    if total <= 0:
        raise ValueError(f"No matching complaints for {start}")

    month_row = {
        "month": start[:7],
        "complaints": total,
        "issues": facet_counts(payload, "issue", total),
        "timely_responses": facet_counts(payload, "timely", total),
        "company_responses": facet_counts(payload, "company_response", total),
    }
    source_meta = payload.get("_meta", {})
    metadata = {
        "last_updated": source_meta.get("last_updated"),
        "last_indexed": source_meta.get("last_indexed"),
        "is_data_stale": source_meta.get("is_data_stale"),
        "has_data_issue": source_meta.get("has_data_issue"),
        "total_record_count": source_meta.get("total_record_count"),
    }
    return month_row, metadata


def month_total(month: dict, field: str) -> int:
    return sum(month[field].values())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def save_volume_chart(months: list[dict]) -> str:
    from scripts.chart_theme import FIGSIZE

    path = IMAGES / "cfpb-transunion-monthly-volume.png"
    x = list(range(len(months)))
    counts = [month["complaints"] for month in months]
    rolling = [
        sum(counts[max(0, index - 2):index + 1]) / len(counts[max(0, index - 2):index + 1])
        for index in x
    ]
    fig = plt.figure(figsize=FIGSIZE)
    style_figure(fig)
    ax = fig.add_subplot(111)
    style_axis(ax)
    ax.plot(x, counts, color=ACCENT, linewidth=1.7, marker="o", markersize=3.2, label="Monthly count")
    ax.plot(x, rolling, color=HIGHLIGHT, linewidth=2.2, linestyle="--", label="Trailing 3-month mean")
    for index in (0, len(months) - 1):
        ax.annotate(f"{counts[index]:,}", (index, counts[index]), xytext=(0, 9),
                    textcoords="offset points", ha="center", color=ACCENT, fontsize=9)
    ticks = list(range(0, len(months), 3))
    if ticks[-1] != len(months) - 1:
        ticks.append(len(months) - 1)
    ax.set_xticks(ticks, [months[index]["month"] for index in ticks])
    ax.set_ylabel("Published complaints received by month")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:.0f}k"))
    ax.legend(frameon=False, loc="upper left")
    add_header(fig, "Complaint volume is a useful review signal", "TransUnion · credit-reporting product · monthly CFPB records, Jan 2025–Sep 2026")
    add_source(fig, "CFPB Consumer Complaint Database; counts are not normalized by customers or market share")
    fig.subplots_adjust(left=0.10, right=0.97, top=0.80, bottom=0.16)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return "/images/" + path.name


def issue_share(months: list[dict]) -> tuple[list[str], dict[str, list[float]]]:
    totals = Counter()
    for month in months:
        totals.update(month["issues"])
    top = [name for name, _ in totals.most_common(3)]
    series: dict[str, list[float]] = {name: [] for name in top}
    series["Other issues"] = []
    for month in months:
        selected = 0
        for name in top:
            count = month["issues"].get(name, 0)
            selected += count
            series[name].append(count / month["complaints"])
        series["Other issues"].append(max(0, month["complaints"] - selected) / month["complaints"])
    return top, series


def save_issue_chart(months: list[dict], series: dict[str, list[float]]) -> str:
    from scripts.chart_theme import FIGSIZE

    path = IMAGES / "cfpb-transunion-issue-mix.png"
    fig = plt.figure(figsize=FIGSIZE)
    style_figure(fig)
    ax = fig.add_subplot(111)
    style_axis(ax)
    colors = [ACCENT, SECONDARY, HIGHLIGHT, "#87939A"]
    x = list(range(len(months)))
    display_names = {
        "Incorrect information on your report": "Incorrect report information",
        "Improper use of your report": "Improper report use",
        "Problem with a company's investigation into an existing problem": "Investigation problems",
        "Other issues": "Other issues",
    }
    for (name, values), color in zip(series.items(), colors):
        ax.plot(x, values, color=color, linewidth=2, marker="o", markersize=2.7,
                label=display_names.get(name, name))
    ticks = list(range(0, len(months), 3))
    if ticks[-1] != len(months) - 1:
        ticks.append(len(months) - 1)
    ax.set_xticks(ticks, [months[index]["month"] for index in ticks])
    ax.set_ylabel("Share of monthly complaints")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.legend(frameon=False, fontsize=8.5, loc="center left", bbox_to_anchor=(1.01, 0.5))
    add_header(fig, "Three issue themes dominate the complaint mix", "Monthly share of CFPB complaints for TransUnion's credit-reporting product")
    add_source(fig, "CFPB Consumer Complaint Database; issue options remained on the 2023 form through Sep 2026")
    fig.subplots_adjust(left=0.10, right=0.72, top=0.80, bottom=0.16)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return "/images/" + path.name


def save_response_chart(months: list[dict], response_labels: list[str]) -> str:
    from scripts.chart_theme import FIGSIZE

    path = IMAGES / "cfpb-transunion-response-mix.png"
    colors = [ACCENT, SECONDARY, HIGHLIGHT, WARNING, "#87939A"]
    fig = plt.figure(figsize=FIGSIZE)
    style_figure(fig)
    ax = fig.add_subplot(111)
    style_axis(ax)
    x = list(range(len(months)))
    selected = response_labels[:2]
    series = {
        label: [month["company_responses"].get(label, 0) / month["complaints"] for month in months]
        for label in selected
    }
    series["Other / in progress"] = [
        max(0, month["complaints"] - sum(month["company_responses"].get(label, 0) for label in selected))
        / month["complaints"]
        for month in months
    ]
    for index, (label, values) in enumerate(series.items()):
        ax.plot(x, values, color=colors[index], linewidth=2, marker="o", markersize=2.7, label=label)
    ticks = list(range(0, len(months), 3))
    if ticks[-1] != len(months) - 1:
        ticks.append(len(months) - 1)
    ax.set_xticks(ticks, [months[index]["month"] for index in ticks])
    ax.set_ylabel("Share of monthly complaints")
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    ax.legend(frameon=False, fontsize=8.5, loc="center left", bbox_to_anchor=(1.01, 0.5))
    add_header(fig, "Published response codes changed over time", "Company-selected response categories · monthly share of filtered complaints")
    add_source(fig, "CFPB Consumer Complaint Database; response codes do not measure satisfaction or resolution quality")
    fig.subplots_adjust(left=0.10, right=0.72, top=0.80, bottom=0.16)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return "/images/" + path.name


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    months = []
    api_metadata = []
    with requests.Session() as session:
        session.headers.update({"User-Agent": "portfolio-research/1.0 (aggregate public-data analysis)"})
        for year, month in month_range():
            row, metadata = fetch_month(session, year, month)
            for field in ("issues", "timely_responses", "company_responses"):
                if month_total(row, field) != row["complaints"]:
                    raise ValueError(f"{field} counts do not reconcile for {row['month']}")
            if metadata.get("is_data_stale") or metadata.get("has_data_issue"):
                raise ValueError(f"CFPB API reports stale or problematic data: {metadata}")
            months.append(row)
            api_metadata.append(metadata)
            print(f"{row['month']}: {row['complaints']:,} complaints")

    issue_totals = Counter()
    response_totals = Counter()
    timely_totals = Counter()
    for month in months:
        issue_totals.update(month["issues"])
        response_totals.update(month["company_responses"])
        timely_totals.update(month["timely_responses"])
    required_metadata = ("last_updated", "last_indexed", "total_record_count")
    if any(not all(metadata.get(field) for field in required_metadata) for metadata in api_metadata):
        raise ValueError("CFPB API did not return complete snapshot metadata for every month")
    snapshot_versions = {
        tuple(metadata[field] for field in required_metadata)
        for metadata in api_metadata
    }
    if len(snapshot_versions) != 1:
        raise ValueError("CFPB API index changed during the monthly queries; rerun for one consistent snapshot")
    snapshot_metadata = api_metadata[-1]
    top_issues = issue_totals.most_common(3)
    total = sum(month["complaints"] for month in months)
    first_total, last_total = months[0]["complaints"], months[-1]["complaints"]
    _, issue_series = issue_share(months)
    response_labels = [name for name, _ in response_totals.most_common(4)]
    visuals = [
        save_volume_chart(months),
        save_issue_chart(months, issue_series),
        save_response_chart(months, response_labels),
    ]

    monthly_digest = hashlib.sha256(
        json.dumps(months, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    metrics = {
        "schemaVersion": 1,
        "caseId": "cfpb-complaint-monitoring",
        "source": {
            "name": "CFPB Consumer Complaint Database",
            "url": "https://www.consumerfinance.gov/data-research/consumer-complaints/",
            "apiUrl": API_URL,
            "publisher": "Consumer Financial Protection Bureau",
            "accessed": ACCESS_DATE,
            "apiLastUpdated": snapshot_metadata["last_updated"],
            "apiLastIndexed": snapshot_metadata["last_indexed"],
            "apiTotalRecordCount": snapshot_metadata["total_record_count"],
            "period": f"{months[0]['month']} through {months[-1]['month']}; complaint receipt date",
            "company": COMPANY,
            "product": PRODUCT,
            "grain": "month × CFPB issue/response facet for a filtered company-product cohort",
            "license": "CFPB states published complaint data are freely available for anyone to use, analyze, and build on",
            "publicDataOnly": True,
            "rawComplaintRecordsStored": False,
            "mutableSource": True,
            "apiSnapshotSha256": monthly_digest,
        },
        "totals": {
            "complaints": total,
            "firstMonth": months[0]["month"],
            "firstMonthComplaints": first_total,
            "lastMonth": months[-1]["month"],
            "lastMonthComplaints": last_total,
            "firstToLastMonthChangePct": (last_total / first_total - 1) * 100,
            "topIssues": [
                {"issue": name, "complaints": count, "share": count / total}
                for name, count in top_issues
            ],
            "topThreeIssueShare": sum(count for _, count in top_issues) / total,
            "timelyResponses": dict(timely_totals),
            "companyResponses": dict(response_totals),
            "responseMixByPeriod": {
                "Jan-Jun 2025": response_mix(months[:6]),
                "Jul-Dec 2025": response_mix(months[6:12]),
                "Jan-Sep 2026": response_mix(months[12:]),
            },
        },
        "monthly": months,
        "artifacts": visuals,
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    artifact_hashes = {path: sha256(ROOT / "public" / path.lstrip("/")) for path in visuals}
    manifest = {
        "schemaVersion": 2,
        "caseId": "cfpb-complaint-monitoring",
        "status": "verified",
        "source": metrics["source"],
        "validation": {
            "checks": [
                f"the official CFPB API returned {len(months)} monthly aggregates for the fixed company-product cohort",
                "all issue, timeliness, and company-response facets reconcile to the monthly complaint total",
                "only aggregate facets were retained; complaint records and narratives were not stored",
                "the cutoff ends before the CFPB form update effective 2026-10-29",
                "all monthly queries share one CFPB index timestamp and record count",
                "the data snapshot reports no stale-data or data-quality flags",
            ],
            "results": metrics["totals"],
            "testResults": {"apiMonths": len(months), "complaints": total, "timelyResponseCounts": dict(timely_totals)},
        },
        "artifacts": visuals,
        "artifactHashes": artifact_hashes,
        "evidenceBoundary": "Complaint counts are not complaint rates because customer denominators are unavailable. CFPB says complaints are not representative of all consumers. Response codes and timely flags do not establish satisfaction, resolution quality, legal violations, or company-wide service performance.",
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"total complaints: {total:,}")
    print(f"monthly snapshot sha256: {monthly_digest}")
    print(f"saved metrics: {METRICS_PATH}")


def response_mix(months: list[dict]) -> dict[str, float]:
    counts = Counter()
    total = 0
    for month in months:
        counts.update(month["company_responses"])
        total += month["complaints"]
    return {name: count / total for name, count in counts.items()} if total else {}


if __name__ == "__main__":
    main()
