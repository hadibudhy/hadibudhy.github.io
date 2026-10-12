"""Build USDA import-sourcing and FEMA/Census business-continuity case studies."""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from chart_theme import (
    ACCENT,
    BORDER,
    CANVAS,
    HIGHLIGHT,
    INK,
    MUTED,
    SECONDARY,
    WARNING,
    add_header,
    add_source,
    style_axis,
    style_figure,
)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
RAW = ROOT / "analysis_data" / "raw" / "new_business_analyses"
IMAGES = ROOT / "public" / "images"
EVIDENCE = ROOT / "public" / "data" / "evidence"
ACCESSED = "2026-10-12"

FATUS_URL = "https://www.ers.usda.gov/media/5029/csv-comma-separated-values-format-of-all-data.csv?v=47263"
CBP_URL = "https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23co.zip"
FEMA_LAYER = "https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0"

FATUS_FILE = RAW / "fatus_all.csv"
CBP_ZIP = RAW / "cbp23co.zip"
CBP_FILE = RAW / "cbp23co.txt"
FEMA_FILE = RAW / "fema_nri_counties_v120.csv"
EXPECTED_SHA256 = {
    FATUS_FILE.name: "a22959fa9357de564f1503c7300a7e3d8d567041d350eb5a344a9970eaa93ca9",
    CBP_ZIP.name: "e9539e96ceb91608ad44ab1cfc651d7c1ff9b88bddfe7a8ff64134ccde6e9603",
    FEMA_FILE.name: "b427834aade6a4cd3b9967fa7a9d75603046ed6d4b42395ef0e7727ebf73ee5c",
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August"]
PRODUCE = ["Fruits, fresh or frozen", "Vegetables, fresh or frozen"]
PRODUCE_LABELS = {
    "Fruits, fresh or frozen": "Fresh fruit",
    "Vegetables, fresh or frozen": "Fresh vegetables",
}
YEARS = [2025, 2026]

SECTORS = {
    "Retail trade": ["44----", "45----"],
    "Accommodation and food services": ["72----"],
    "Manufacturing": ["31----", "32----", "33----"],
}
HAZARDS = {
    "HRCN_RISKR": "Hurricane",
    "IFLD_RISKR": "Inland flood",
    "WFIR_RISKR": "Wildfire",
}
HIGH_RATINGS = {"Very High", "Relatively High"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_snapshot(path: Path) -> None:
    expected = EXPECTED_SHA256[path.name]
    actual = sha256(path)
    if actual != expected:
        raise ValueError(
            f"Source snapshot changed for {path.name}: expected {expected}, got {actual}. "
            "Review the updated source and findings before refreshing the pinned hash."
        )


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "portfolio-analysis/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response, path.open("wb") as output:
        output.write(response.read())


def ensure_sources() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    if not FATUS_FILE.exists() or FATUS_FILE.stat().st_size < 1000:
        download(FATUS_URL, FATUS_FILE)
    if not CBP_ZIP.exists() or CBP_ZIP.stat().st_size < 1000:
        download(CBP_URL, CBP_ZIP)
    if not CBP_FILE.exists() or CBP_FILE.stat().st_size < 1000:
        with zipfile.ZipFile(CBP_ZIP) as archive:
            member = next(name for name in archive.namelist() if name.lower().endswith("cbp23co.txt"))
            with archive.open(member) as source, CBP_FILE.open("wb") as output:
                output.write(source.read())
    fields = [
        "NRI_ID", "STATE", "STATEABBRV", "COUNTY", "STCOFIPS", "POPULATION",
        "RISK_SCORE", "RISK_RATNG", "RISK_SPCTL", "EAL_SCORE", "EAL_RATNG",
        "EAL_VALT", "EAL_VALB", "BUILDVALUE", "HRCN_RISKR", "IFLD_RISKR", "WFIR_RISKR",
    ]
    existing_fields = set(pd.read_csv(FEMA_FILE, nrows=0).columns) if FEMA_FILE.exists() else set()
    if not set(fields).issubset(existing_fields):
        records: list[dict] = []
        for offset in range(0, 4000, 1000):
            response = requests.get(
                f"{FEMA_LAYER}/query",
                params={
                    "where": "1=1", "outFields": ",".join(fields),
                    "returnGeometry": "false", "resultOffset": offset,
                    "resultRecordCount": 1000, "f": "json",
                },
                timeout=90,
            )
            response.raise_for_status()
            payload = response.json()
            if "error" in payload:
                raise RuntimeError(f"FEMA API error: {payload['error']}")
            records.extend(feature["attributes"] for feature in payload["features"])
            if len(payload["features"]) < 1000:
                break
        nri = pd.DataFrame(records)
        if len(nri) != 3232 or nri["STCOFIPS"].nunique() != 3232:
            raise ValueError("FEMA county layer did not return the expected 3,232 unique records")
        nri.to_csv(FEMA_FILE, index=False)
    for path in [FATUS_FILE, CBP_ZIP, FEMA_FILE]:
        verify_snapshot(path)


def analyze_sourcing() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    frame = pd.read_csv(FATUS_FILE)
    frame.columns = frame.columns.str.strip()
    monthly = frame.loc[
        frame["Source_table"].str.contains("Top 10 sources", na=False)
        & frame["US_Trade"].eq("Imports")
        & frame["Value_type"].eq("Customs value")
        & frame["Commodity"].isin(PRODUCE)
        & frame["Time_period"].isin(MONTHS)
        & pd.to_numeric(frame["Year"], errors="coerce").isin(YEARS)
    ].copy()
    monthly["Year"] = pd.to_numeric(monthly["Year"]).astype(int)
    rows = []
    supplier_shares = []
    for (commodity, year, month), group in monthly.groupby(["Commodity", "Year", "Time_period"], sort=False):
        total_rows = group.loc[group["Country"].eq("World total")]
        suppliers = group.loc[~group["Country"].eq("World total")].copy()
        if len(total_rows) != 1 or len(suppliers) != 10:
            raise ValueError(f"Unexpected top-source rows for {commodity}, {year} {month}")
        world = float(total_rows["Value"].iloc[0])
        suppliers["share"] = suppliers["Value"] / world
        coverage = float(suppliers["share"].sum())
        hhi_lower = float(suppliers["share"].pow(2).sum())
        hhi_upper = hhi_lower + (1.0 - coverage) ** 2
        rows.append({
            "commodity": commodity,
            "category": PRODUCE_LABELS[commodity],
            "year": int(year),
            "month": month,
            "month_num": MONTHS.index(month) + 1,
            "world_imports_million_usd": world,
            "top10_coverage_share": coverage,
            "largest_partner": suppliers.loc[suppliers["share"].idxmax(), "Country"],
            "largest_partner_share": float(suppliers["share"].max()),
            "hhi_lower": hhi_lower,
            "hhi_upper": hhi_upper,
        })
        for item in suppliers.itertuples(index=False):
            supplier_shares.append({
                "commodity": commodity,
                "category": PRODUCE_LABELS[commodity],
                "year": int(year),
                "month": month,
                "month_num": MONTHS.index(month) + 1,
                "country": item.Country,
                "share": float(item.share),
            })
    monthly_metrics = pd.DataFrame(rows)
    supplier_metrics = pd.DataFrame(supplier_shares)
    top_origin_by_panel = monthly_metrics.groupby(["category", "year"])["largest_partner"].agg(set)
    if any(origins != {"Mexico"} for origins in top_origin_by_panel):
        raise ValueError("The pinned sourcing findings require Mexico to lead every category-month panel")
    counts = monthly_metrics.groupby(["category", "year"]).size()
    if len(counts) != 4 or not counts.eq(8).all():
        raise ValueError("FATUS comparison must contain Jan-Aug observations for both years and categories")

    summary = []
    for (category, year), group in monthly_metrics.groupby(["category", "year"]):
        mexico = supplier_metrics.loc[
            supplier_metrics["category"].eq(category)
            & supplier_metrics["year"].eq(year)
            & supplier_metrics["country"].eq("Mexico")
        ]
        if len(mexico) != 8:
            raise ValueError(f"Mexico is not present in every monthly top-ten extract for {category}, {year}")
        summary.append({
            "category": category,
            "year": int(year),
            "months": int(len(group)),
            "jan_aug_imports_million_usd": float(group["world_imports_million_usd"].sum()),
            "mean_monthly_top10_coverage_pct": 100 * float(group["top10_coverage_share"].mean()),
            "mean_monthly_hhi_lower": float(group["hhi_lower"].mean()),
            "mean_monthly_hhi_upper": float(group["hhi_upper"].mean()),
            "mean_top_partner_share_pct": 100 * float(group["largest_partner_share"].mean()),
            "top_partner": str(group["largest_partner"].mode().iloc[0]),
            "mexico_share_mean_pct": 100 * float(mexico["share"].mean()),
            "mexico_share_min_pct": 100 * float(mexico["share"].min()),
            "mexico_share_max_pct": 100 * float(mexico["share"].max()),
        })
    result = pd.DataFrame(summary)
    year_2025 = result.loc[result["year"].eq(2025)].set_index("category")
    year_2026 = result.loc[result["year"].eq(2026)].set_index("category")
    for category in PRODUCE_LABELS.values():
        change = 100 * (
            year_2026.loc[category, "jan_aug_imports_million_usd"]
            / year_2025.loc[category, "jan_aug_imports_million_usd"] - 1
        )
        result.loc[result["category"].eq(category) & result["year"].eq(2026), "jan_aug_import_value_change_pct_yoy"] = change

    findings = {
        "source_rows": int(len(frame)),
        "comparison_period": "January-August 2025 versus January-August 2026",
        "monthly_rows": int(len(monthly_metrics)),
        "categories": result.astype(object).where(pd.notna(result), None).to_dict(orient="records"),
        "concentration_method": "Monthly HHI lower bound sums squared top-10 source shares; upper bound assigns the residual share to one unobserved source.",
        "interpretation": "Origin-market screening, not supplier-level exposure or a forecast of procurement disruption.",
    }
    return monthly_metrics, supplier_metrics, findings


def analyze_network_risk() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    nri = pd.read_csv(FEMA_FILE, dtype={"STCOFIPS": str})
    cbp = pd.read_csv(
        CBP_FILE,
        dtype={"fipstate": str, "fipscty": str, "naics": str},
        usecols=["fipstate", "fipscty", "naics", "est"],
    )
    cbp["fips"] = cbp["fipstate"].str.zfill(2) + cbp["fipscty"].str.zfill(3)
    cbp["est"] = pd.to_numeric(cbp["est"], errors="coerce")
    parts = []
    for sector, codes in SECTORS.items():
        data = cbp.loc[cbp["naics"].isin(codes) & cbp["fipscty"].ne("999")]
        county = data.groupby("fips", as_index=False, sort=True)["est"].sum(min_count=1)
        county = county.dropna(subset=["est"]).merge(
            nri, left_on="fips", right_on="STCOFIPS", how="left", validate="one_to_one"
        )
        if county["RISK_SCORE"].isna().any():
            raise ValueError(f"Unmatched FEMA counties remain for {sector}")
        county["sector"] = sector
        county["risk_top_quartile"] = county["RISK_SCORE"].ge(county["RISK_SCORE"].quantile(.75))
        parts.append(county)
    sector_counties = pd.concat(parts, ignore_index=True)

    summary = []
    for sector, group in sector_counties.groupby("sector", sort=False):
        high = group["RISK_RATNG"].isin(HIGH_RATINGS)
        entry = {
            "sector": sector,
            "county_count": int(len(group)),
            "establishments": int(group["est"].sum()),
            "high_or_very_high_counties": int(high.sum()),
            "establishments_high_or_very_high": int(group.loc[high, "est"].sum()),
            "high_or_very_high_establishment_share_pct": 100 * float(group.loc[high, "est"].sum() / group["est"].sum()),
            "top_quartile_establishment_share_pct": 100 * float(group.loc[group["risk_top_quartile"], "est"].sum() / group["est"].sum()),
            "risk_score_q75": float(group["RISK_SCORE"].quantile(.75)),
        }
        for field, hazard in HAZARDS.items():
            valid_rating = group[field].isin({"Very Low", "Relatively Low", "Relatively Moderate", "Relatively High", "Very High"})
            exposure = group[field].isin(HIGH_RATINGS)
            prefix = hazard.lower().replace(" ", "_")
            entry[f"{prefix}_high_counties"] = int(exposure.sum())
            entry[f"{prefix}_rated_establishment_coverage_pct"] = 100 * float(group.loc[valid_rating, "est"].sum() / group["est"].sum())
            entry[f"{prefix}_high_among_rated_establishment_pct"] = 100 * float(group.loc[exposure, "est"].sum() / group.loc[valid_rating, "est"].sum())
        summary.append(entry)
    result = pd.DataFrame(summary)
    top_counties = (
        sector_counties.loc[sector_counties["RISK_RATNG"].isin(HIGH_RATINGS)]
        .sort_values(["sector", "est"], ascending=[True, False])
        .groupby("sector", sort=False)
        .head(6)
        .copy()
    )
    top_counties["county_label"] = top_counties["COUNTY"] + ", " + top_counties["STATEABBRV"]

    for sector, group in sector_counties.groupby("sector"):
        if group["STCOFIPS"].duplicated().any():
            raise ValueError(f"Duplicate county-sector rows found for {sector}")
    findings = {
        "fema_record_count": int(len(nri)),
        "fema_unique_counties": int(nri["STCOFIPS"].nunique()),
        "cbp_rows_read": int(len(cbp)),
        "sector_summary": result.to_dict(orient="records"),
        "priority_counties": top_counties[["sector", "STATE", "COUNTY", "est", "RISK_SCORE", "RISK_RATNG", "RISK_SPCTL", "HRCN_RISKR", "IFLD_RISKR", "WFIR_RISKR"]].to_dict(orient="records"),
        "interpretation": "County-sector screen using local establishment counts as a footprint proxy and FEMA's relative community risk ratings.",
    }
    return sector_counties, top_counties, findings


def save_sourcing_charts(monthly: pd.DataFrame, suppliers: pd.DataFrame) -> list[str]:
    colors = {"Fresh fruit": ACCENT, "Fresh vegetables": HIGHLIGHT}
    paths = [
        "/images/produce-source-concentration.png",
        "/images/produce-mexico-share.png",
        "/images/produce-import-value-yoy.png",
    ]

    fig, ax = plt.subplots(figsize=(12, 6.75)); style_figure(fig); style_axis(ax, "x")
    summary = monthly.groupby(["category", "year"], as_index=False).agg(
        hhi_lower=("hhi_lower", "mean"), hhi_upper=("hhi_upper", "mean")
    )
    labels = [("Fresh fruit", 2025), ("Fresh fruit", 2026), ("Fresh vegetables", 2025), ("Fresh vegetables", 2026)]
    y = np.arange(len(labels))
    for i, (category, year) in enumerate(labels):
        row = summary.loc[summary.category.eq(category) & summary.year.eq(year)].iloc[0]
        ax.plot([row.hhi_lower, row.hhi_upper], [i, i], color=colors[category], linewidth=8, solid_capstyle="round")
        ax.scatter([row.hhi_lower, row.hhi_upper], [i, i], color=INK, s=20, zorder=3)
        ax.text(row.hhi_upper + .012, i, f"{row.hhi_lower:.4f} to {row.hhi_upper:.4f}", va="center", fontsize=9, color=MUTED)
    ax.set_yticks(y, [f"{c}, {yr}" for c, yr in labels])
    ax.set_xlim(0, .51); ax.set_xlabel("Mean monthly HHI bound, Jan-Aug; 0 to 1")
    add_header(fig, "Fresh vegetable sourcing is more concentrated", "Monthly country-share HHI bounds use the top ten origins and disclose the unreported remainder.")
    add_source(fig, "USDA ERS FATUS, monthly import customs values, 2025 and 2026")
    fig.tight_layout(rect=(.05, .07, .95, .82)); fig.savefig(ROOT / "public" / paths[0].lstrip("/"), dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 6.75)); style_figure(fig); style_axis(ax)
    mex = suppliers.loc[suppliers.country.eq("Mexico")]
    for category in PRODUCE_LABELS.values():
        for year, marker, line in [(2025, "o", "--"), (2026, "o", "-")]:
            g = mex.loc[mex.category.eq(category) & mex.year.eq(year)].sort_values("month_num")
            ax.plot(g.month_num, g.share * 100, marker=marker, linestyle=line, color=colors[category],
                    linewidth=2.2 if year == 2026 else 1.4,
                    label=f"{category}, {year}")
    ax.set_xticks(range(1, 9), MONTHS); ax.set_ylabel("Mexico share of reported total imports (%)")
    ax.set_xlabel("Month")
    ax.legend(frameon=False, ncol=2)
    add_header(fig, "Mexico remains the largest fresh-produce origin", "Monthly shares fluctuate, so a single annual concentration figure can hide sourcing seasonality.")
    add_source(fig, "USDA ERS FATUS, top ten import origins by value")
    fig.tight_layout(rect=(.05, .07, .95, .82)); fig.savefig(ROOT / "public" / paths[1].lstrip("/"), dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 6.75)); style_figure(fig); style_axis(ax)
    for category in PRODUCE_LABELS.values():
        for year, line in [(2025, "--"), (2026, "-")]:
            g = monthly.loc[monthly.category.eq(category) & monthly.year.eq(year)].sort_values("month_num")
            ax.plot(g.month_num, g.world_imports_million_usd, marker="o", linestyle=line,
                    color=colors[category], linewidth=2 if year == 2026 else 1.4,
                    label=f"{category}, {year}")
    ax.set_xticks(range(1, 9), MONTHS); ax.set_ylabel("Monthly customs value (million U.S. dollars)")
    ax.set_xlabel("Month")
    ax.legend(frameon=False, ncol=2)
    add_header(fig, "Import value changes are seasonal and nominal", "Compare the same months across years; dollar values can move with price and product mix.")
    add_source(fig, "USDA ERS FATUS, customs value, not physical quantity")
    fig.tight_layout(rect=(.05, .07, .95, .82)); fig.savefig(ROOT / "public" / paths[2].lstrip("/"), dpi=160); plt.close(fig)
    return paths


def save_risk_charts(sector_counties: pd.DataFrame, summary: pd.DataFrame, top: pd.DataFrame) -> list[str]:
    colors = {"Retail trade": ACCENT, "Accommodation and food services": SECONDARY, "Manufacturing": HIGHLIGHT}
    paths = [
        "/images/business-risk-rating-establishment-share.png",
        "/images/business-risk-hazard-exposure.png",
        "/images/business-risk-priority-counties.png",
    ]

    ratings = ["Very Low", "Relatively Low", "Relatively Moderate", "Relatively High", "Very High", "Insufficient Data"]
    sector_counties = sector_counties.copy()
    sector_counties["RISK_RATNG"] = sector_counties["RISK_RATNG"].fillna("Insufficient Data")
    grouped = sector_counties.groupby(["sector", "RISK_RATNG"], as_index=False)["est"].sum()
    totals = grouped.groupby("sector")["est"].sum()
    fig, ax = plt.subplots(figsize=(12, 6.75)); style_figure(fig); style_axis(ax, "x")
    y = np.arange(len(SECTORS)); left = np.zeros(len(SECTORS))
    palette = ["#B7CFDA", "#7FA3B2", "#E0C685", "#D68765", "#A94637"]
    for rating, color in zip(ratings, palette):
        values = []
        for sector in SECTORS:
            amount = grouped.loc[grouped.sector.eq(sector) & grouped.RISK_RATNG.eq(rating), "est"].sum()
            values.append(100 * amount / totals[sector])
        ax.barh(y, values, left=left, label=rating, color=color, height=.55)
        left += np.array(values)
    ax.set_yticks(y, list(SECTORS)); ax.invert_yaxis(); ax.set_xlim(0, 100)
    ax.set_xlabel("")
    ax.legend(frameon=False, ncol=5, loc="lower center", bbox_to_anchor=(.5, -.18))
    add_header(fig, "High-risk counties contain about half of tracked establishments", "Bars show establishment share across FEMA's relative composite risk classes.")
    add_source(fig, "U.S. Census County Business Patterns 2023 and FEMA National Risk Index v1.20")
    fig.tight_layout(rect=(.05, .2, .95, .82)); fig.savefig(ROOT / "public" / paths[0].lstrip("/"), dpi=160); plt.close(fig)

    hazard_cols = {
        "Overall multi-hazard": "high_or_very_high_establishment_share_pct",
        "Hurricane": "hurricane_high_among_rated_establishment_pct",
        "Inland flood": "inland_flood_high_among_rated_establishment_pct",
        "Wildfire": "wildfire_high_among_rated_establishment_pct",
    }
    fig, ax = plt.subplots(figsize=(12, 6.75)); style_figure(fig); style_axis(ax)
    x = np.arange(len(SECTORS)); width = .19
    for j, (label, field) in enumerate(hazard_cols.items()):
        ax.bar(x + (j - 1.5) * width, summary[field], width, label=label,
               color=[ACCENT, SECONDARY, WARNING, HIGHLIGHT][j])
    ax.set_xticks(x, ["Retail", "Accommodation + food", "Manufacturing"])
    ax.set_ylabel("Establishments in high or very-high risk counties (%)")
    ax.set_ylim(0, 100); ax.legend(frameon=False, ncol=2)
    add_header(fig, "Risk priorities change by hazard", "Hazard shares use only counties with an applicable rating; composite risk uses all county-sector rows.")
    add_source(fig, "FEMA National Risk Index v1.20; Census County Business Patterns 2023")
    fig.tight_layout(rect=(.05, .07, .95, .82)); fig.savefig(ROOT / "public" / paths[1].lstrip("/"), dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 6.75)); style_figure(fig); style_axis(ax, "x")
    plotted = top.sort_values(["sector", "est"], ascending=[True, True]).reset_index(drop=True)
    yvals = np.arange(len(plotted))
    for i, row in plotted.iterrows():
        ax.barh(i, row.est, color=colors[row.sector], alpha=.9)
        ax.text(row.est + 160, i, f"Risk {row.RISK_SCORE:.1f}", va="center", fontsize=8, color=MUTED)
    ax.set_xlabel("County establishments, 2023")
    ax.set_yticks(yvals, [f"{r.county_label}  |  {r.sector}" for r in plotted.itertuples()])
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=colors[s]) for s in SECTORS],
              labels=list(SECTORS), frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(.5, -.19))
    add_header(fig, "Dense operating markets can rank high on FEMA risk", "Six largest county-sector footprints within FEMA's high or very-high composite risk classes.")
    add_source(fig, "U.S. Census County Business Patterns 2023; FEMA National Risk Index v1.20")
    fig.tight_layout(rect=(.05, .11, .95, .82)); fig.savefig(ROOT / "public" / paths[2].lstrip("/"), dpi=160); plt.close(fig)
    return paths


def main() -> None:
    ensure_sources()
    IMAGES.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)

    source_monthly, supplier_shares, sourcing_findings = analyze_sourcing()
    county_panel, priority_counties, risk_findings = analyze_network_risk()
    sourcing_artifacts = save_sourcing_charts(source_monthly, supplier_shares)
    risk_artifacts = save_risk_charts(county_panel, pd.DataFrame(risk_findings["sector_summary"]), priority_counties)

    source_monthly.to_csv(RAW / "produce_monthly_metrics.csv", index=False)
    supplier_shares.to_csv(RAW / "produce_supplier_shares.csv", index=False)
    county_panel.to_csv(RAW / "county_sector_risk.csv", index=False)
    priority_counties.to_csv(RAW / "priority_counties.csv", index=False)
    (RAW / "produce_findings.json").write_text(json.dumps(sourcing_findings, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (RAW / "network_risk_findings.json").write_text(json.dumps(risk_findings, indent=2, allow_nan=False) + "\n", encoding="utf-8")

    sourcing_manifest = {
        "schemaVersion": 2,
        "caseId": "fresh-produce-import-sourcing-risk",
        "status": "verified",
        "source": {
            "name": "Foreign Agricultural Trade of the United States, top fresh-produce import origins",
            "url": "https://www.ers.usda.gov/data-products/foreign-agricultural-trade-of-the-united-states-fatus/us-agricultural-trade-data-update",
            "publisher": "U.S. Department of Agriculture, Economic Research Service",
            "accessed": ACCESSED,
            "grain": "month × FATUS produce category × reported source",
            "period": "January-August 2025 and January-August 2026",
            "rows": int(len(source_monthly)),
            "sha256": sha256(FATUS_FILE),
            "publicDataOnly": True,
            "mutableSource": True,
        },
        "validation": {"checks": [
            "two fresh-produce categories each include eight monthly comparisons for 2025 and 2026",
            "each category-month has ten reported origins and one World total row",
            "monthly top-10 origin shares are divided by the corresponding World total",
            "monthly HHI results are bounded for the unreported residual origin share",
            "all three charts regenerate from the local USDA CSV snapshot",
        ]},
        "artifacts": sourcing_artifacts,
        "artifactHashes": {path: sha256(ROOT / "public" / path.lstrip("/")) for path in sourcing_artifacts},
        "evidenceBoundary": "FATUS reports origin markets by aggregated fresh-produce group and customs value. It does not identify importer-specific suppliers, contracts, quantities, product-level substitutions, or disruption outcomes.",
        "findings": sourcing_findings,
    }
    risk_manifest = {
        "schemaVersion": 2,
        "caseId": "business-network-hazard-screen",
        "status": "verified",
        "source": {
            "name": "County Business Patterns 2023 and National Risk Index county layer v1.20",
            "url": "https://www.census.gov/data/datasets/2023/econ/cbp/2023-cbp.html",
            "publisher": "U.S. Census Bureau and Federal Emergency Management Agency",
            "femaUrl": FEMA_LAYER,
            "accessed": ACCESSED,
            "grain": "county × NAICS sector with FEMA county risk attributes",
            "period": "CBP 2023; FEMA NRI v1.20, December 2025",
            "rows": int(len(county_panel)),
            "cbpSha256": sha256(CBP_ZIP),
            "femaSha256": sha256(FEMA_FILE),
            "publicDataOnly": True,
            "mutableSource": True,
        },
        "validation": {"checks": [
            "CBP sector records aggregate only non-overlapping NAICS groups before joining county risk",
            "unknown county FIPS records are excluded and each county-sector join is one-to-one",
            "all matched county-sector records have a FEMA composite risk score",
            "risk-band exposure shares use establishments, not county counts, as the denominator",
            "hazard-specific high risk shares are reported separately from composite multi-hazard risk",
            "all three charts regenerate from the local CBP and FEMA snapshots",
        ]},
        "artifacts": risk_artifacts,
        "artifactHashes": {path: sha256(ROOT / "public" / path.lstrip("/")) for path in risk_artifacts},
        "evidenceBoundary": "County establishment counts are sector footprint proxies, not a company's locations. FEMA's relative community risk ratings do not estimate a particular site's loss, insurance premium, interruption duration, or mitigation return.",
        "findings": risk_findings,
    }
    for name, manifest in [
        ("fresh-produce-import-sourcing-risk.json", sourcing_manifest),
        ("business-network-hazard-screen.json", risk_manifest),
    ]:
        (EVIDENCE / name).write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"sourcing": sourcing_findings, "network_risk": risk_findings}, indent=2))


if __name__ == "__main__":
    main()
