"""Rebuild charts and evidence manifests for the EIA and College Scorecard cases."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.chart_theme import (  # noqa: E402
    ACCENT,
    BORDER,
    CANVAS,
    DPI,
    GRID,
    HIGHLIGHT,
    INK,
    MUTED,
    SECONDARY,
    add_header,
    add_source,
    style_axis,
    style_figure,
)

RAW = ROOT / "analysis_data" / "raw"
IMAGES = ROOT / "public" / "images"
EVIDENCE = ROOT / "public" / "data" / "evidence"
EIA_FILE = RAW / "eia_commercial_electricity_2019_2025_full.json"
SCORECARD_ZIP = RAW / "Most-Recent-Cohorts-Field-of-Study_06102026.zip"

EIA_SHA256 = "a4214c6405861c1fee3f7eaa074c14354374a8d64ce4e5a415c52a59f4c356f0"
SCORECARD_SHA256 = "9c4339d65f0699a60d6078fe54fc3bf03fded30a65079222d9221952b8578165"
SCORECARD_URL = "https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Field-of-Study_06102026.zip"
ACCESSED = "2026-10-12"

STATE_CODES = set(
    "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS "
    "MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA "
    "WV WI WY DC".split()
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_hash(path: Path, expected: str) -> None:
    actual = sha256(path)
    if actual != expected:
        raise ValueError(
            f"Source snapshot drift for {path.name}: expected {expected}, got {actual}. "
            "Revalidate the reported metrics before changing the recorded snapshot."
        )


def ensure_eia_snapshot() -> None:
    if EIA_FILE.exists():
        return
    api_key = os.environ.get("EIA_API_KEY", "DEMO_KEY")
    rows: list[dict] = []
    total: int | None = None
    offset = 0
    while total is None or offset < total:
        parameters = [
            ("api_key", api_key),
            ("frequency", "monthly"),
            ("data[0]", "sales"),
            ("data[1]", "revenue"),
            ("data[2]", "customers"),
            ("data[3]", "price"),
            ("facets[sectorid][]", "COM"),
            ("start", "2019-01"),
            ("end", "2025-12"),
            ("sort[0][column]", "period"),
            ("sort[0][direction]", "asc"),
            ("offset", str(offset)),
            ("length", "5000"),
        ]
        url = "https://api.eia.gov/v2/electricity/retail-sales/data/?" + urllib.parse.urlencode(parameters)
        request = urllib.request.Request(url, headers={"User-Agent": "portfolio-data-analysis/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            page = json.loads(response.read().decode("utf-8"))
        result = page["response"]
        total = int(result["total"])
        rows.extend(result["data"])
        if not result["data"]:
            raise ValueError(f"EIA pagination stopped at {offset} of {total} rows")
        offset += len(result["data"])

    RAW.mkdir(parents=True, exist_ok=True)
    EIA_FILE.write_text(json.dumps({"rows": rows}, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def ensure_scorecard_snapshot() -> None:
    if SCORECARD_ZIP.exists():
        return
    RAW.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(SCORECARD_URL, headers={"User-Agent": "portfolio-data-analysis/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response, SCORECARD_ZIP.open("wb") as output:
        output.write(response.read())


def save_chart(figure: plt.Figure, filename: str) -> Path:
    path = IMAGES / filename
    figure.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(figure)
    return path


def write_manifest(case_id: str, source: dict, checks: list[str], boundary: str, artifacts: list[Path]) -> None:
    manifest = {
        "schemaVersion": 2,
        "caseId": case_id,
        "status": "verified",
        "source": source,
        "validation": {"checks": checks},
        "artifacts": [f"/images/{path.name}" for path in artifacts],
        "artifactHashes": {f"/images/{path.name}": sha256(path) for path in artifacts},
        "evidenceBoundary": boundary,
    }
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    output = EVIDENCE / f"{case_id}.json"
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def load_eia() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    ensure_eia_snapshot()
    require_hash(EIA_FILE, EIA_SHA256)
    payload = json.loads(EIA_FILE.read_text(encoding="utf-8"))
    data = pd.DataFrame(payload["rows"])
    if len(data) != 5_208:
        raise ValueError(f"Expected 5,208 EIA rows, got {len(data)}")
    if data.duplicated(["period", "stateid"]).any():
        raise ValueError("EIA state-month records are not unique")

    for column in ("sales", "revenue", "customers", "price"):
        data[column] = pd.to_numeric(data[column], errors="raise")
    data["year"] = data["period"].str[:4].astype(int)

    states = data[data["stateid"].isin(STATE_CODES)].copy()
    expected_periods = {f"{year}-{month:02}" for year in range(2019, 2026) for month in range(1, 13)}
    state_periods = states.groupby("stateid")["period"].agg(set)
    if states["stateid"].nunique() != 51 or not state_periods.map(lambda periods: periods == expected_periods).all():
        raise ValueError("EIA state panel does not contain 51 complete state and DC series")

    def annual_prices(frame: pd.DataFrame) -> pd.DataFrame:
        annual = frame.groupby(["stateid", "stateDescription", "year"], as_index=False).agg(
            sales_million_kwh=("sales", "sum"),
            revenue_musd=("revenue", "sum"),
            month_count=("period", "nunique"),
        )
        annual["price_cents_per_kwh"] = 100 * annual["revenue_musd"] / annual["sales_million_kwh"]
        return annual

    state_annual = annual_prices(states)
    us = data[data["stateid"].eq("US")].copy()
    if len(us) != 84:
        raise ValueError(f"Expected 84 U.S. aggregate months, got {len(us)}")
    national = annual_prices(us)
    if not national["month_count"].eq(12).all():
        raise ValueError("The U.S. aggregate is missing a month")

    national_prices = national.set_index("year")["price_cents_per_kwh"]
    state_pivot = state_annual.pivot(index=["stateid", "stateDescription"], columns="year", values="price_cents_per_kwh")
    growth = 100 * (state_pivot[2025] / state_pivot[2019] - 1)
    metrics = {
        "us_2019": float(national_prices.loc[2019]),
        "us_2025": float(national_prices.loc[2025]),
        "us_growth_pct": float(100 * (national_prices.loc[2025] / national_prices.loc[2019] - 1)),
        "median_state_growth_pct": float(growth.median()),
        "hawaii_2025": float(state_pivot.loc[("HI", "Hawaii"), 2025]),
        "california_2025": float(state_pivot.loc[("CA", "California"), 2025]),
        "california_growth_pct": float(growth.loc[("CA", "California")]),
        "maine_growth_pct": float(growth.loc[("ME", "Maine")]),
        "dc_growth_pct": float(growth.loc[("DC", "District of Columbia")]),
    }
    assert round(metrics["us_2019"], 2) == 10.68
    assert round(metrics["us_2025"], 2) == 13.41
    assert round(metrics["us_growth_pct"], 1) == 25.6
    assert round(metrics["median_state_growth_pct"], 1) == 21.7
    assert round(metrics["hawaii_2025"], 1) == 36.4
    assert round(metrics["california_2025"], 1) == 26.4
    return national, state_annual, metrics


def eia_charts() -> tuple[list[Path], dict[str, float]]:
    national, state_annual, metrics = load_eia()
    source_label = "EIA-861M commercial sector, 2019 to 2025"

    fig, ax = plt.subplots(figsize=(10.5, 5.9), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax)
    fig.subplots_adjust(top=0.79, bottom=0.17, left=0.10, right=0.96)
    ax.plot(national["year"], national["price_cents_per_kwh"], color=ACCENT, linewidth=3, marker="o", markersize=6)
    ax.fill_between(national["year"], national["price_cents_per_kwh"], color=ACCENT, alpha=0.10)
    ax.set_xticks(national["year"])
    ax.set_ylabel("Cents per kilowatt-hour, nominal")
    ax.set_ylim(0, max(national["price_cents_per_kwh"]) * 1.22)
    ax.annotate(
        f"{metrics['us_2019']:.2f}¢",
        (2019, metrics["us_2019"]),
        xytext=(5, 12),
        textcoords="offset points",
        color=INK,
        fontweight="bold",
    )
    ax.annotate(
        f"{metrics['us_2025']:.2f}¢",
        (2025, metrics["us_2025"]),
        xytext=(-4, 12),
        textcoords="offset points",
        ha="right",
        color=INK,
        fontweight="bold",
    )
    add_header(
        fig,
        f"Commercial average retail prices rose {metrics['us_growth_pct']:.1f}% from 2019 to 2025",
        "U.S. sales-weighted average retail price; annual revenue divided by annual sales",
    )
    add_source(fig, source_label)
    trend_path = save_chart(fig, "commercial-electricity-price-trend.png")

    state_pivot = state_annual.pivot(index=["stateid", "stateDescription"], columns="year", values="price_cents_per_kwh")
    state = pd.DataFrame(index=state_pivot.index)
    state["price_2025"] = state_pivot[2025]
    state["growth_pct"] = 100 * (state_pivot[2025] / state_pivot[2019] - 1)
    state["high_price_and_growth"] = (
        state["price_2025"].ge(state["price_2025"].quantile(0.75))
        & state["growth_pct"].ge(state["growth_pct"].quantile(0.75))
    )

    fig, ax = plt.subplots(figsize=(10.5, 6.4), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="both")
    fig.subplots_adjust(top=0.78, bottom=0.14, left=0.10, right=0.97)
    ax.axvline(state["growth_pct"].median(), color=BORDER, linestyle="--", linewidth=1)
    ax.axhline(state["price_2025"].median(), color=BORDER, linestyle="--", linewidth=1)
    colors = [HIGHLIGHT if flag else ACCENT for flag in state["high_price_and_growth"]]
    ax.scatter(state["growth_pct"], state["price_2025"], c=colors, s=48, edgecolor=CANVAS, linewidth=0.7, zorder=3)
    labels = ["HI", "CA", "ME", "NY", "DC"]
    for (code, name), row in state.iterrows():
        if code in labels:
            ax.annotate(code, (row["growth_pct"], row["price_2025"]), xytext=(5, 5), textcoords="offset points", fontsize=8, color=INK)
    ax.scatter([], [], color=HIGHLIGHT, s=48, label="Top quartile on both measures")
    ax.legend(frameon=False, loc="upper right")
    ax.set_xlabel("Nominal price change, 2019 to 2025 (%)")
    ax.set_ylabel("Commercial price in 2025 (cents per kWh)")
    ax.set_title(
        "States with both high 2025 average prices and faster growth stand out",
        loc="left",
        color=INK,
        fontsize=12,
        fontweight="bold",
        pad=12,
    )
    add_header(fig, "State cost signals point to different review priorities", "Each point is one state or DC; orange marks the top quartile on both measures, dashed lines mark medians")
    add_source(fig, source_label)
    scatter_path = save_chart(fig, "commercial-electricity-state-priorities.png")

    top = state_pivot[2025].sort_values(ascending=False).head(10).index
    selected = state_pivot.loc[top, [2019, 2025]].copy()
    selected.index = [name for _, name in selected.index]
    selected = selected.sort_values(2025)
    fig, ax = plt.subplots(figsize=(10.5, 6.8), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(top=0.80, bottom=0.12, left=0.20, right=0.95)
    y = range(len(selected))
    for position, (name, row) in enumerate(selected.iterrows()):
        ax.plot([row[2019], row[2025]], [position, position], color=BORDER, linewidth=2, zorder=1)
        ax.scatter(row[2019], position, color=SECONDARY, s=42, zorder=2)
        ax.scatter(row[2025], position, color=HIGHLIGHT if name in {"Hawaii", "California"} else ACCENT, s=48, zorder=3)
    ax.set_yticks(list(y), selected.index)
    ax.set_xlabel("Cents per kilowatt-hour, annual sales-weighted price")
    ax.set_xlim(0, max(selected[2025]) * 1.18)
    ax.set_title("Hawaii and California had the highest commercial average prices in 2025", loc="left", color=INK, fontsize=12, fontweight="bold", pad=12)
    ax.scatter([], [], color=SECONDARY, s=42, label="2019")
    ax.scatter([], [], color=ACCENT, s=48, label="2025")
    ax.legend(frameon=False, loc="lower right")
    add_header(fig, "The most expensive states are not interchangeable", "Top 10 state and DC prices in 2025, with each market's 2019 level for context")
    add_source(fig, source_label)
    top_path = save_chart(fig, "commercial-electricity-top-state-rates.png")

    artifacts = [trend_path, scatter_path, top_path]
    write_manifest(
        "commercial-electricity-costs",
        {
            "name": "Electric power sales and revenue by state and sector, monthly",
            "url": "https://www.eia.gov/electricity/data/eia861m/index.php",
            "publisher": "U.S. Energy Information Administration",
            "accessed": ACCESSED,
            "grain": "state-month-sector record",
            "period": "2019-01 through 2025-12",
            "rows": 5_208,
            "sha256": EIA_SHA256,
            "publicDataOnly": True,
            "mutableSource": True,
        },
        [
            "complete 2019-2025 EIA snapshot has 5,208 unique state-month records",
            "51 state and DC series each contain all 84 months",
            "annual prices recomputed as 100 times summed revenue divided by summed sales",
            "the U.S. aggregate rose from 10.68 to 13.41 cents per kWh, a 25.6% nominal increase",
            "state comparisons exclude EIA census regions and the U.S. aggregate row",
            "all three charts regenerate from the hash-checked local snapshot",
        ],
        "EIA average retail prices include utility revenue from delivered electricity, but do not show an individual site's tariff, load profile, contract price, itemized charges, or realized cost savings.",
        artifacts,
    )
    return artifacts, metrics


def load_scorecard() -> tuple[pd.DataFrame, dict[str, int | float]]:
    ensure_scorecard_snapshot()
    require_hash(SCORECARD_ZIP, SCORECARD_SHA256)
    with zipfile.ZipFile(SCORECARD_ZIP) as archive:
        csv_name = "Most-Recent-Cohorts-Field-of-Study.csv"
        with archive.open(csv_name) as source:
            data = pd.read_csv(
                source,
                usecols=[
                    "UNITID",
                    "OPEID6",
                    "INSTNM",
                    "MAIN",
                    "CONTROL",
                    "CIPCODE",
                    "CIPDESC",
                    "CREDLEV",
                    "CREDDESC",
                    "EARN_MDN_4YR",
                    "DEBT_ALL_STGP_ANY_MDN",
                ],
                low_memory=False,
            )

    if len(data) != 227_980:
        raise ValueError(f"Expected 227,980 College Scorecard rows, got {len(data)}")
    key = data[["OPEID6", "CIPCODE", "CREDLEV"]].astype("string").agg("|".join, axis=1)
    data["program_key"] = key
    metrics = ["EARN_MDN_4YR", "DEBT_ALL_STGP_ANY_MDN"]
    duplicated = data[data.duplicated("program_key", keep=False)]
    for metric in metrics:
        if duplicated.groupby("program_key")[metric].nunique(dropna=False).gt(1).any():
            raise ValueError(f"Repeated branch rows contain different {metric} values")

    # Scorecard outcomes are calculated at OPEID6 level and repeated for branches.
    # Use the row marked MAIN to assign institutional control after collapsing those copies.
    data = data.sort_values(["program_key", "MAIN"], ascending=[True, False]).drop_duplicates("program_key", keep="first")
    if data["program_key"].nunique() != 217_369:
        raise ValueError("Unexpected number of distinct OPEID6, field, and credential records")

    data["earnings"] = pd.to_numeric(data["EARN_MDN_4YR"], errors="coerce")
    data["earnings_reported"] = data["earnings"].notna()
    domestic = data[data["CONTROL"].isin(["Public", "Private, nonprofit", "Private, for-profit"])].copy()
    bachelor = domestic[domestic["CREDLEV"].eq(3)].copy()
    reported = int(bachelor["earnings_reported"].sum())
    total = len(bachelor)
    unreported_values = set(bachelor.loc[~bachelor["earnings_reported"], "EARN_MDN_4YR"].dropna().astype(str).unique())
    if unreported_values != {"PS"}:
        raise ValueError(f"Expected only privacy-suppressed PS values in domestic bachelor's rows, got {unreported_values}")
    control = bachelor.groupby("CONTROL")["earnings_reported"].agg(["count", "sum"])
    control["reporting_pct"] = 100 * control["sum"] / control["count"]

    if total != 67_212 or reported != 25_283:
        raise ValueError(f"Unexpected U.S. bachelor's earnings coverage: {reported}/{total}")
    expected_rates = {
        "Public": 54.2,
        "Private, nonprofit": 24.8,
        "Private, for-profit": 44.5,
    }
    for group, expected in expected_rates.items():
        actual = round(float(control.loc[group, "reporting_pct"]), 1)
        if actual != expected:
            raise ValueError(f"Unexpected {group} earnings coverage: {actual}%")

    stats: dict[str, int | float] = {
        "source_rows": 227_980,
        "unique_program_records": 217_369,
        "duplicate_branch_rows_removed": 10_611,
        "domestic_bachelor_program_records": total,
        "domestic_bachelor_earnings_reported": reported,
        "domestic_bachelor_earnings_privacy_suppressed": total - reported,
        "domestic_bachelor_reporting_rate_pct": 100 * reported / total,
        "public_reporting_rate_pct": float(control.loc["Public", "reporting_pct"]),
        "private_nonprofit_reporting_rate_pct": float(control.loc["Private, nonprofit", "reporting_pct"]),
        "private_forprofit_reporting_rate_pct": float(control.loc["Private, for-profit", "reporting_pct"]),
    }
    return data, stats


def college_charts() -> tuple[list[Path], dict[str, int | float]]:
    data, metrics = load_scorecard()
    domestic = data[data["CONTROL"].isin(["Public", "Private, nonprofit", "Private, for-profit"])].copy()
    credential = domestic[domestic["CREDLEV"].between(1, 8)].copy()
    credential["earnings_reported"] = pd.to_numeric(credential["EARN_MDN_4YR"], errors="coerce").notna()
    coverage = credential.groupby(["CREDLEV", "CREDDESC"], as_index=False).agg(
        program_records=("program_key", "size"), reported=("earnings_reported", "sum")
    )
    coverage["reported_pct"] = 100 * coverage["reported"] / coverage["program_records"]
    coverage = coverage.sort_values("CREDLEV")

    fig, ax = plt.subplots(figsize=(10.5, 6.8), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(top=0.79, bottom=0.13, left=0.34, right=0.94)
    y = range(len(coverage))
    bars = ax.barh(list(y), coverage["reported_pct"], color=ACCENT, height=0.62)
    ax.set_yticks(list(y), coverage["CREDDESC"])
    ax.invert_yaxis()
    ax.set_xlim(0, 75)
    ax.set_xlabel("Program records with a reportable four-year earnings median (%)")
    ax.set_title("Outcome coverage is uneven across credential levels", loc="left", color=INK, fontsize=12, fontweight="bold", pad=12)
    for bar, (_, row) in zip(bars, coverage.iterrows()):
        ax.text(bar.get_width() + 1.1, bar.get_y() + bar.get_height() / 2, f"{row['reported_pct']:.1f}%  n={int(row['program_records']):,}", va="center", color=INK, fontsize=8.5)
    add_header(fig, "A public earnings metric does not cover every program", "Program records are deduplicated at institution system, field of study, and credential level")
    add_source(fig, "U.S. Department of Education College Scorecard, June 10, 2026 file")
    credential_path = save_chart(fig, "college-scorecard-earnings-coverage-credential.png")

    bachelor = domestic[domestic["CREDLEV"].eq(3)].copy()
    bachelor["earnings_reported"] = pd.to_numeric(bachelor["EARN_MDN_4YR"], errors="coerce").notna()
    by_control = bachelor.groupby("CONTROL")["earnings_reported"].agg(["count", "sum"])
    by_control["privacy_suppressed"] = by_control["count"] - by_control["sum"]
    by_control["reported_pct"] = 100 * by_control["sum"] / by_control["count"]
    order = ["Private, for-profit", "Private, nonprofit", "Public"]
    by_control = by_control.loc[order]

    fig, ax = plt.subplots(figsize=(10.5, 5.8), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(top=0.80, bottom=0.24, left=0.28, right=0.96)
    y = range(len(by_control))
    ax.barh(list(y), by_control["reported_pct"], color=ACCENT, height=0.58, label="Reported")
    ax.barh(list(y), 100 - by_control["reported_pct"], left=by_control["reported_pct"], color=BORDER, height=0.58, label="Privacy suppressed (PS)")
    ax.set_yticks(list(y), order)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of distinct bachelor's program records")
    ax.invert_yaxis()
    for position, (group, row) in enumerate(by_control.iterrows()):
        ax.text(row["reported_pct"] + 1.4, position, f"{row['reported_pct']:.1f}% reported, n={int(row['count']):,}", va="center", color=INK, fontsize=9)
    ax.set_title("Public programs are more than twice as likely to report earnings as private nonprofits", loc="left", color=INK, fontsize=11.5, fontweight="bold", pad=12)
    ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.24))
    add_header(fig, "Coverage differs by institution control", "Only distinct U.S. bachelor's program records; privacy-suppressed values are not treated as zero")
    add_source(fig, "U.S. Department of Education College Scorecard, June 10, 2026 file")
    control_path = save_chart(fig, "college-scorecard-earnings-coverage-control.png")

    raw_bachelor = 70_557
    unique_bachelor = 67_212
    repeated = raw_bachelor - unique_bachelor
    if repeated != 3_345:
        raise ValueError(f"Unexpected U.S. bachelor's branch duplicates: {repeated}")
    fig, ax = plt.subplots(figsize=(9.5, 5.4), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax)
    fig.subplots_adjust(top=0.77, bottom=0.18, left=0.12, right=0.96)
    bars = ax.bar(["Raw U.S. rows", "Distinct program records"], [raw_bachelor, unique_bachelor], color=[BORDER, ACCENT], width=0.58)
    ax.set_ylabel("U.S. bachelor's program rows")
    ax.set_ylim(0, raw_bachelor * 1.18)
    ax.set_title("Branch campus rows repeat some program-level outcomes", loc="left", color=INK, fontsize=12, fontweight="bold", pad=12)
    for bar, value in zip(bars, (raw_bachelor, unique_bachelor)):
        ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:,}", ha="center", va="bottom", color=INK, fontweight="bold")
    ax.annotate(
        f"Remove {repeated:,} repeated rows",
        xy=(1, unique_bachelor),
        xytext=(0.45, raw_bachelor * 1.08),
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 1},
        color=MUTED,
        ha="center",
        fontsize=9,
    )
    add_header(fig, "Deduplicate before counting programs", "Scorecard calculates these metrics at OPEID6 and repeats them across branch campuses")
    add_source(fig, "U.S. Department of Education College Scorecard, June 10, 2026 file")
    dedup_path = save_chart(fig, "college-scorecard-branch-deduplication.png")

    artifacts = [credential_path, control_path, dedup_path]
    write_manifest(
        "college-program-outcome-coverage",
        {
            "name": "College Scorecard Most Recent Cohorts: Field of Study",
            "url": "https://collegescorecard.ed.gov/data/",
            "publisher": "U.S. Department of Education",
            "accessed": ACCESSED,
            "releaseDate": "2026-06-10",
            "grain": "institution system, four-digit CIP field, and credential level",
            "rows": 227_980,
            "sha256": SCORECARD_SHA256,
            "publicDataOnly": True,
            "mutableSource": True,
        },
        [
            "source ZIP SHA-256 verified against the checked June 10, 2026 snapshot",
            "227,980 source rows reduced to 217,369 OPEID6, field, and credential records",
            "repeated branch rows have matching earnings and debt values before deduplication",
            "domestic bachelor's coverage is 25,283 reported of 67,212 distinct program records",
            "earnings reporting rates recomputed separately for public, nonprofit, and for-profit programs",
            "every unreported domestic bachelor's earnings cell is source-coded PS",
            "privacy-suppressed cells remain missing and are not imputed",
            "all three charts regenerate from the hash-checked local snapshot",
        ],
        "College Scorecard earnings cover Title IV aid recipients who worked and were not enrolled in the measurement year. Program-level medians are descriptive, privacy-suppressed cells are not zero, and different coverage rates make unqualified rankings unsafe.",
        artifacts,
    )
    return artifacts, metrics


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    eia_artifacts, eia_metrics = eia_charts()
    college_artifacts, college_metrics = college_charts()
    print("Commercial electricity:", {key: round(value, 2) for key, value in eia_metrics.items()})
    print("College program coverage:", college_metrics)
    print("Wrote charts:", *(path.relative_to(ROOT) for path in [*eia_artifacts, *college_artifacts]), sep="\n  ")


if __name__ == "__main__":
    main()
