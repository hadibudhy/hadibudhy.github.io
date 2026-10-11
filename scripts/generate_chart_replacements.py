import hashlib
import io
import json
import shutil
import sys
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.chart_theme import ACCENT, BORDER, CANVAS, DPI, FONT, GRID, HIGHLIGHT, INK, MUTED, PAPER, SECONDARY, WARNING, WARNING_FILL, WIDE_SIZE, add_header, add_source, style_axis, style_figure


OUT = ROOT / "public" / "images"

SOURCE_SNAPSHOTS = {
    "Online Retail.xlsx": "43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d",
    "nyc_restaurants.csv": "a02bf468aaf826c64a78b6ad17e038908d643e769dcb4ee8257b5a6282519bb1",
    "sec_microsoft_companyfacts.json": "f8aae2965b20ad0df44bdf7ccbedf797d275b6b8dc030154a7a311361bb7246f",
    "airbnb_nyc_june_2026.csv": "e42f8f897a4ed89d489e703dc462d314f5aa98912cca6637c988c99f5490caba",
    "bank_marketing.zip": "e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4",
    "clickstream.zip": "de43f67460aeb49fd879cb7db3d7d654a5f83e8d6ec466820573ef8a6255a7c6",
    "credit_default.zip": "56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602",
    "world_happiness_2026.xlsx": "576e382655cec3ae704a0b41cd2c04465b87cd84b7f131a0c4fa26d41f6d8028",
    "nyc_taxi_january_2025.parquet": "9af277e4c0d3f9deb30644da822981e1e7df6af58313170fd3aa8a474485488a",
    "bls_jolts_2025.json": "8045da8715b2ebca3f44d02810a9dc116c60cb6240ed66147aef26408886ee15",
    "netflix_titles.csv": "df1f4ad2027a5a14c3a33932ef0d4054565ff88adf92b7f263601b70fdc6f3f3",
}


def require_source_snapshot(path: Path) -> None:
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = SOURCE_SNAPSHOTS[path.name]
    if actual != expected:
        raise ValueError(
            f"Source snapshot drift for {path}: expected SHA-256 {expected}, got {actual}. "
            "Revalidate the published metrics before replacing the recorded snapshot."
        )


def annual_microsoft_metrics() -> dict[str, dict[str, float]]:
    source = ROOT / "analysis_data" / "raw" / "sec_microsoft_companyfacts.json"
    require_source_snapshot(source)
    facts = json.loads(source.read_text(encoding="utf-8"))["facts"]["us-gaap"]
    year_ends = {2023: "2023-06-30", 2024: "2024-06-30", 2025: "2025-06-30"}
    revenue_tags = ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax")
    output: dict[str, dict[str, float]] = {"revenue": {}, "net_income": {}, "net_margin": {}}

    for year, period_end in year_ends.items():
        period_start = f"{year - 1}-07-01"
        selected_revenue = None
        for tag in revenue_tags:
            fact = facts.get(tag, {})
            candidates = [
                row for row in fact.get("units", {}).get("USD", [])
                if row.get("form") in {"10-K", "10-K/A"}
                and row.get("start") == period_start
                and row.get("end") == period_end
            ]
            if candidates:
                selected_revenue = max(candidates, key=lambda row: (row.get("filed", ""), row.get("accn", "")))
                break

        income_candidates = [
            row for row in facts["NetIncomeLoss"].get("units", {}).get("USD", [])
            if row.get("form") in {"10-K", "10-K/A"}
            and row.get("start") == period_start
            and row.get("end") == period_end
        ]
        if not selected_revenue or not income_candidates:
            raise ValueError(f"Missing selected annual SEC facts for FY{year}")
        selected_income = max(income_candidates, key=lambda row: (row.get("filed", ""), row.get("accn", "")))
        output["revenue"][year] = selected_revenue["val"] / 1_000_000_000
        output["net_income"][year] = selected_income["val"] / 1_000_000_000
        output["net_margin"][year] = 100 * selected_income["val"] / selected_revenue["val"]

    assert [round(output["revenue"][year], 1) for year in year_ends] == [211.9, 245.1, 281.7]
    assert [round(output["net_income"][year], 1) for year in year_ends] == [72.4, 88.1, 101.8]
    assert [round(output["net_margin"][year], 1) for year in year_ends] == [34.1, 36.0, 36.1]
    return output


def save_fake_job_model_comparison() -> None:
    labels = ["Text model\n(Logistic regression)", "Profile details\n(LightGBM)", "Combined model\n(default)", "Combined model\n(tuned threshold)"]
    f1 = [0.819, 0.828, 0.831, 0.850]
    recall = [0.913, 0.723, 0.711, 0.751]
    pr_auc = [0.927, 0.915, 0.901, 0.901]
    x = np.arange(len(labels))
    width = 0.24

    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    fig.subplots_adjust(top=0.80, bottom=0.19, left=0.09, right=0.97)
    style_axis(ax)
    bars = [
        ax.bar(x - width, f1, width, label="F1", color=ACCENT),
        ax.bar(x, recall, width, label="Recall", color=SECONDARY),
        ax.bar(x + width, pr_auc, width, label="PR-AUC", color=HIGHLIGHT),
    ]
    for group in bars:
        for bar in group:
            ax.annotate(f"{bar.get_height():.3f}", (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 5), textcoords="offset points", ha="center", va="bottom",
                        color=INK, fontsize=9, fontweight="bold")
    add_header(fig, "Text features catch more scams; the tuned model has the highest F1",
               "Employment Scam Aegean held-out test set, 17,880 labeled posts; higher scores are better")
    ax.set_ylabel("Model score")
    ax.set_ylim(0, 1.05)
    ax.set_xticks(x, labels)
    ax.legend(frameon=False, ncols=3, loc="upper left", labelcolor=INK, fontsize=9)
    add_source(fig, "Employment Scam Aegean Dataset; held-out test metrics")
    fig.savefig(OUT / "fake-job-all-models.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_jolts_signals() -> None:
    source = ROOT / "analysis_data" / "raw" / "bls_jolts_2025.json"
    require_source_snapshot(source)
    response = json.loads(source.read_text(encoding="utf-8"))
    series = {item["seriesID"][-3:]: item for item in response["Results"]["series"]}
    december = {key: float(next(row["value"] for row in item["data"] if row["year"] == "2025" and row["period"] == "M12"))
                for key, item in series.items()}
    assert december["JOL"] == 6550 and december["TSL"] == 5203
    assert december["HIR"] == 3.3 and december["QUR"] == 2.0
    fig, axes = plt.subplots(1, 2, figsize=WIDE_SIZE, facecolor=CANVAS, gridspec_kw={"wspace": 0.28})
    style_figure(fig)
    fig.subplots_adjust(top=0.81, bottom=0.17, left=0.08, right=0.97)
    for ax in axes:
        style_axis(ax)

    counts = [december["JOL"] / 1000, december["TSL"] / 1000]
    count_bars = axes[0].bar(["Open positions\n(stock)", "Separations\n(monthly flow)"], counts, color=[ACCENT, SECONDARY], width=0.58)
    axes[0].set_title("Counts use different time bases", loc="left", color=INK, fontsize=12, fontweight="bold", pad=12)
    axes[0].set_ylabel("People (millions; definitions differ)")
    axes[0].set_ylim(0, 7.2)
    for bar, value in zip(count_bars, counts):
        axes[0].annotate(f"{value:.3f}M", (bar.get_x() + bar.get_width() / 2, value), xytext=(0, 7),
                         textcoords="offset points", ha="center", color=INK, fontsize=10, fontweight="bold")

    rates = [december["HIR"], december["QUR"]]
    rate_bars = axes[1].bar(["Hires", "Quits"], rates, color=[ACCENT, SECONDARY], width=0.58)
    axes[1].set_title("Hires and quits are rates, not counts", loc="left", color=INK, fontsize=12, fontweight="bold", pad=12)
    axes[1].set_ylabel("Rate (%)")
    axes[1].set_ylim(0, 4.2)
    for bar, value in zip(rate_bars, rates):
        axes[1].annotate(f"{value:.1f}%", (bar.get_x() + bar.get_width() / 2, value), xytext=(0, 7),
                         textcoords="offset points", ha="center", color=INK, fontsize=10, fontweight="bold")

    add_header(fig, "December workforce signals need separate units",
               "U.S. BLS JOLTS: openings are a point-in-time stock; hires, quits, and separations are monthly measures")
    add_source(fig, "U.S. Bureau of Labor Statistics, JOLTS, December 2025")
    fig.savefig(OUT / "jolts-december-signals.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    figure, axis = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis)
    figure.subplots_adjust(left=0.14, right=0.95, top=0.80, bottom=0.18)
    labels = ["Open positions", "Total separations"]
    values = counts
    bars = axis.bar(labels, values, color=[ACCENT, SECONDARY], width=0.58)
    axis.set_ylabel("People (millions)")
    axis.set_ylim(0, 7.2)
    for bar, value in zip(bars, values):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 0.12, f"{value:.3f}M",
                  ha="center", color=INK, fontsize=10, fontweight="bold")
    add_header(figure, "Openings exceeded monthly separations in December",
               "Openings are a point-in-time stock; separations are a monthly flow")
    add_source(figure, "U.S. Bureau of Labor Statistics, JOLTS, December 2025")
    figure.savefig(OUT / "jolts-openings-separations.png", dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def save_sec_revenue_net_income(metrics: dict[str, dict[str, float]]) -> None:
    years = [2023, 2024, 2025]
    labels = [f"FY{year}" for year in years]
    revenue = [metrics["revenue"][year] for year in years]
    net_income = [metrics["net_income"][year] for year in years]
    x = np.arange(len(years))
    width = 0.28
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis)
    figure.subplots_adjust(left=0.09, right=0.97, top=0.80, bottom=0.14)
    revenue_bars = axis.bar(x - width / 2, revenue, width, color=ACCENT)
    income_bars = axis.bar(x + width / 2, net_income, width, color=SECONDARY)
    axis.bar_label(revenue_bars, labels=[f"${value:.1f}" for value in revenue], padding=4, fontsize=10, color=INK)
    axis.bar_label(income_bars, labels=[f"${value:.1f}" for value in net_income], padding=4, fontsize=10, color=INK)
    axis.set_xticks(x, labels)
    axis.set_ylabel("Reported value (US$ billions)")
    axis.set_ylim(0, max(revenue) * 1.2)
    axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:.0f}"))
    axis.legend([revenue_bars, income_bars], ["Revenue", "Net income"], frameon=False,
                ncols=2, loc="upper left", bbox_to_anchor=(0.01, 0.99), fontsize=10,
                labelcolor=INK)
    add_header(figure, "Revenue and net income rose in each reported year",
               "Microsoft annual results, FY2023 to FY2025; US dollars, billions")
    add_source(figure, "SEC Company Facts, Microsoft Corporation; values selected from annual filings")
    figure.savefig(OUT / "sec-revenue-net-income.png", dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def save_sec_net_margin(metrics: dict[str, dict[str, float]]) -> None:
    years = [2023, 2024, 2025]
    labels = [f"FY{year}" for year in years]
    margins = [metrics["net_margin"][year] for year in years]
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis)
    figure.subplots_adjust(left=0.09, right=0.96, top=0.80, bottom=0.14)
    axis.plot(labels, margins, color=ACCENT, marker="o", linewidth=2.5, markersize=7)
    for label, value in zip(labels, margins):
        axis.annotate(f"{value:.1f}%", (label, value), xytext=(0, 9), textcoords="offset points",
                      ha="center", color=INK, fontsize=10, fontweight="bold")
    axis.set_ylabel("Net margin (%)")
    axis.set_ylim(0, 40)
    axis.set_yticks(range(0, 41, 10))
    add_header(figure, "Net margin rose 2.0 percentage points over three years",
               "Microsoft net income divided by revenue; zero-based 0% to 40% scale")
    add_source(figure, "SEC Company Facts, Microsoft Corporation; annual reported values")
    figure.savefig(OUT / "sec-net-margin.png", dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def save_sec_charts() -> None:
    metrics = annual_microsoft_metrics()
    save_sec_revenue_net_income(metrics)
    save_sec_net_margin(metrics)


def save_taxi_completed_trips() -> None:
    source = ROOT / "analysis_data" / "raw" / "nyc_taxi_january_2025.parquet"
    require_source_snapshot(source)
    trips = pd.read_parquet(source)
    trips["duration_minutes"] = (trips["tpep_dropoff_datetime"] - trips["tpep_pickup_datetime"]).dt.total_seconds() / 60
    january = trips["tpep_pickup_datetime"].between("2025-01-01", "2025-01-31 23:59:59.999999")
    valid = trips[january & (trips["trip_distance"] > 0) & (trips["total_amount"] > 0)
                  & trips["duration_minutes"].between(1, 120)].copy()
    assert len(trips) == 3_475_226 and len(valid) == 3_312_701
    hourly_counts = valid.groupby(valid["tpep_pickup_datetime"].dt.hour).size().reindex(range(24), fill_value=0)
    assert hourly_counts.loc[18] == 241_585
    hourly = hourly_counts / 1000
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.16)
    style_axis(ax)
    ax.bar(hourly.index, hourly.values, color=ACCENT, width=0.8)
    for hour in (17, 18, 19):
        ax.bar(hour, hourly.loc[hour], color=HIGHLIGHT if hour == 18 else SECONDARY, width=0.8)
    ax.annotate("18:00  |  241,585", (18, hourly.loc[18]), xytext=(18, hourly.loc[18] + 14),
                ha="center", color=INK, fontsize=9, fontweight="bold",
                arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8})
    add_header(fig, "Valid yellow-taxi trips peaked at 18:00",
               "Valid completed trips by pickup hour, NYC, January 2025; trip counts do not measure unmet demand")
    ax.set_xlabel("Pickup hour")
    ax.set_ylabel("Completed trips (thousands)")
    ax.set_xticks(range(24))
    ax.set_ylim(0, max(hourly.max() * 1.1, 250))
    add_source(fig, "NYC TLC yellow taxi trip records; 3,312,701 valid January trips")
    fig.savefig(OUT / "taxi-demand-by-hour.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    zones = pd.read_csv(ROOT / "analysis_data" / "raw" / "nyc_taxi_zones.csv")
    by_zone = valid.merge(zones, left_on="PULocationID", right_on="LocationID", how="left")
    boroughs = by_zone.groupby("Borough").agg(
        trips=("total_amount", "size"), duration=("duration_minutes", "mean"), fare=("total_amount", "mean")
    )
    airport = by_zone.groupby("Zone").agg(
        trips=("total_amount", "size"), duration=("duration_minutes", "mean"), fare=("total_amount", "mean")
    )
    assert int(boroughs.loc["Manhattan", "trips"]) == 2_962_526
    assert round(boroughs.loc["Queens", "duration"], 1) == 32.0
    assert round(boroughs.loc["Queens", "fare"], 2) == 72.12
    assert int(airport.loc["JFK Airport", "trips"]) == 133_337
    assert round(airport.loc["JFK Airport", "fare"], 2) == 81.10

    borough_labels = ["Manhattan", "Queens", "Brooklyn", "Bronx", "Staten Island"]
    borough_counts = boroughs.loc[borough_labels, "trips"] / 1_000_000
    fig, axes = plt.subplots(1, 2, figsize=WIDE_SIZE, facecolor=CANVAS, gridspec_kw={"wspace": 0.34})
    style_figure(fig)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.79, bottom=0.17)
    for axis in axes:
        style_axis(axis, grid_axis="x")
    bars = axes[0].barh(borough_labels, borough_counts.values, color=[ACCENT] + [SECONDARY] * 4, height=0.58)
    axes[0].invert_yaxis()
    axes[0].set_xlim(0, 3.45)
    axes[0].set_xlabel("Valid pickups (millions)")
    for bar, value, label in zip(bars, borough_counts.values, borough_labels):
        count = int(boroughs.loc[label, "trips"])
        axes[0].text(value + 0.04, bar.get_y() + bar.get_height() / 2, f"{count:,}",
                     va="center", color=INK, fontsize=8.5)
    selected = [
        ("Manhattan average", boroughs.loc["Manhattan", "duration"], boroughs.loc["Manhattan", "fare"], int(boroughs.loc["Manhattan", "trips"]), ACCENT),
        ("Queens average", boroughs.loc["Queens", "duration"], boroughs.loc["Queens", "fare"], int(boroughs.loc["Queens", "trips"]), SECONDARY),
        ("JFK Airport zone", airport.loc["JFK Airport", "duration"], airport.loc["JFK Airport", "fare"], int(airport.loc["JFK Airport", "trips"]), HIGHLIGHT),
    ]
    label_offsets = {"Manhattan average": (8, 7), "Queens average": (8, -18), "JFK Airport zone": (8, 8)}
    for label, duration, fare, count, color in selected:
        axes[1].scatter(duration, fare, s=55, color=color, zorder=3)
        axes[1].annotate(f"{label}\n{duration:.1f} min, ${fare:.2f}\nn={count:,}",
                         (duration, fare), xytext=label_offsets[label], textcoords="offset points",
                         color=INK, fontsize=8)
    axes[1].set_xlim(0, 46)
    axes[1].set_ylim(0, 100)
    axes[1].set_xlabel("Average trip duration (minutes)")
    axes[1].set_ylabel("Average total amount per trip (US$)")
    add_header(fig, "Manhattan led volume; JFK trips ran longer and cost more",
               "NYC yellow taxi trips in January 2025; total amount is not driver profit or incremental demand")
    add_source(fig, "NYC TLC trip records and zone lookup; only positive-distance, positive-total trips lasting 1 to 120 minutes")
    fig.savefig(OUT / "taxi-zone-economics.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def load_retail_data() -> tuple[pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    source = ROOT / "analysis_data" / "extracted" / "Online Retail.xlsx"
    require_source_snapshot(source)
    raw = pd.read_excel(source)
    sales = raw[~raw["InvoiceNo"].astype(str).str.startswith("C")]
    sales = sales[(sales["Quantity"] > 0) & (sales["UnitPrice"] > 0) & sales["CustomerID"].notna()].copy()
    sales["revenue"] = sales["Quantity"] * sales["UnitPrice"]
    customer_revenue = sales.groupby("CustomerID")["revenue"].sum().sort_values(ascending=False)
    customer_orders = sales.groupby("CustomerID")["InvoiceNo"].nunique()
    top_decile = int(np.ceil(len(customer_revenue) * 0.1))
    assert len(raw) == 541_909
    assert raw["InvoiceNo"].astype(str).str.startswith("C").sum() == 9_288
    assert raw["CustomerID"].isna().sum() == 135_080
    assert len(customer_revenue) == 4_338 and sales["InvoiceNo"].nunique() == 18_532
    assert np.isclose(sales["revenue"].sum(), 8_911_407.904)
    assert np.isclose(customer_orders.ge(2).mean(), 0.6558321807)
    assert np.isclose(customer_revenue.iloc[:top_decile].sum() / customer_revenue.sum(), 0.6137506575)
    monthly_revenue = sales.set_index("InvoiceDate").resample("ME")["revenue"].sum()
    assert round(monthly_revenue.loc["2011-11-30"] / 1_000_000, 2) == 1.16
    orders = sales[["InvoiceNo", "CustomerID", "InvoiceDate"]].drop_duplicates("InvoiceNo")
    orders = orders.sort_values(["CustomerID", "InvoiceDate", "InvoiceNo"]).copy()
    orders["returning"] = orders.groupby("CustomerID").cumcount().gt(0)
    returning_share = orders.set_index("InvoiceDate").resample("ME")["returning"].mean()
    assert [round(value * 100, 1) for value in returning_share] == [36.8, 57.8, 61.9, 65.8, 73.9, 81.7, 82.6, 85.9, 86.8, 83.0, 81.4, 87.8, 94.7]
    country = sales.groupby("Country")["revenue"].sum().sort_values(ascending=False).head(8) / 1_000_000
    assert np.isclose(country["United Kingdom"] * 1_000_000 / customer_revenue.sum(), 0.8201163759)
    return monthly_revenue, returning_share, country, sales


def save_retail_growth_patterns(monthly_revenue: pd.Series, returning_share: pd.Series) -> None:
    figure, axes = plt.subplots(2, 1, figsize=WIDE_SIZE, sharex=True, facecolor=CANVAS)
    style_figure(figure)
    figure.subplots_adjust(left=0.10, right=0.97, top=0.80, bottom=0.17, hspace=0.34)
    for axis in axes:
        style_axis(axis)

    dates = monthly_revenue.index
    revenue_millions = monthly_revenue / 1_000_000
    axes[0].plot(dates, revenue_millions, color=ACCENT, marker="o", linewidth=2.2, markersize=5)
    axes[0].set_title("Recorded revenue (£ millions)", loc="left", color=INK, fontsize=11, fontweight="bold", pad=8)
    axes[0].set_ylim(0, 1.3)
    axes[0].yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"£{value:.1f}"))
    november = pd.Timestamp("2011-11-30")
    november_value = revenue_millions.loc[november]
    axes[0].annotate("£1.16m", (november, november_value), xytext=(0, 10),
                     textcoords="offset points", ha="center", color=INK,
                     fontsize=10, fontweight="bold")

    axes[1].plot(dates, returning_share * 100, color=SECONDARY, marker="o", linewidth=2.2, markersize=5)
    axes[1].set_title("Share of monthly orders from returning customers", loc="left", color=INK,
                      fontsize=11, fontweight="bold", pad=8)
    axes[1].set_ylim(0, 100)
    axes[1].yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
    tick_indices = range(0, len(dates), 2)
    axes[1].set_xticks([dates[index] for index in tick_indices])
    axes[1].set_xticklabels([dates[index].strftime("%b '%y") for index in tick_indices])

    add_header(figure, "Revenue peaked in November as repeat orders grew",
               "Cleaned customer-identified orders, 1 Dec 2010 to 9 Dec 2011; December is partial")
    add_source(figure, "UCI Online Retail; positive, non-cancelled lines with CustomerID")
    figure.savefig(OUT / "retail-growth-patterns.png", dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def save_retail_market_opportunity(country: pd.Series) -> None:
    labels = list(country.index)
    values = country.to_numpy()
    colors = [ACCENT if label == "United Kingdom" else SECONDARY for label in labels]
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis, grid_axis="x")
    figure.subplots_adjust(left=0.20, right=0.90, top=0.80, bottom=0.16)
    bars = axis.barh(labels, values, color=colors, height=0.58)
    axis.invert_yaxis()
    axis.set_xlim(0, 8.5)
    axis.set_xticks(range(0, 9, 2))
    axis.set_xlabel("Recorded revenue (£ millions)")
    for bar, label, value in zip(bars, labels, values):
        note = f"£{value:.2f}m"
        if label == "United Kingdom":
            note += "  |  82% of total"
        axis.text(value + 0.08, bar.get_y() + bar.get_height() / 2, note,
                  va="center", color=INK, fontsize=10, fontweight="bold" if label == "United Kingdom" else "normal")
    add_header(figure, "The UK generated 82% of recorded revenue",
               "Top eight countries, 1 Dec 2010 to 9 Dec 2011; recorded sales are not market demand or profit")
    add_source(figure, "UCI Online Retail; positive, non-cancelled lines with CustomerID")
    figure.savefig(OUT / "retail-market-opportunity.png", dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def save_retail_charts() -> None:
    monthly_revenue, returning_share, country, _ = load_retail_data()
    save_retail_growth_patterns(monthly_revenue, returning_share)
    save_retail_market_opportunity(country)


def save_restaurant_risk_by_borough() -> None:
    source = ROOT / "analysis_data" / "raw" / "nyc_restaurants.csv"
    require_source_snapshot(source)
    inspections = pd.read_csv(source, low_memory=False)
    assert len(inspections) == 295_473
    assert inspections["GRADE"].isna().sum() == 150_352
    assert inspections["GRADE DATE"].isna().sum() == 160_593
    assert inspections["SCORE"].isna().sum() == 17_179
    inspections["date"] = pd.to_datetime(inspections["INSPECTION DATE"], errors="coerce")
    inspections = inspections[inspections["date"].dt.year.between(2022, 2025)]
    assert len(inspections) == 227_520
    grouped = inspections.groupby(["CAMIS", "INSPECTION DATE", "INSPECTION TYPE"], dropna=False).agg(
        borough=("BORO", "first"),
        grade=("GRADE", "first"),
        score=("SCORE", "max"),
        critical=("CRITICAL FLAG", lambda values: (values == "Critical").any()),
    ).reset_index()
    assert len(grouped) == 73_211 and np.isclose(grouped["critical"].mean(), 0.7730942072)
    assert grouped["grade"].value_counts().loc[["A", "B", "C"]].to_dict() == {"A": 35_555, "B": 3_856, "C": 2_040}
    assert grouped["grade"].isna().sum() == 30_037
    grade_shares = grouped["grade"].value_counts().loc[["A", "B", "C"]] / grouped["grade"].isin(["A", "B", "C"]).sum()
    assert [round(value * 100, 1) for value in grade_shares] == [85.8, 9.3, 4.9]
    grade_counts = grouped["grade"].value_counts().reindex(["A", "B", "C"]).astype(int)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.24, right=0.92, top=0.80, bottom=0.17)
    grade_labels = ["A", "B", "C", "No grade recorded"]
    values = [*grade_counts.values.tolist(), 30_037]
    bars = ax.barh(grade_labels, values, color=[SECONDARY, ACCENT, HIGHLIGHT, WARNING], height=0.58)
    ax.invert_yaxis()
    ax.set_xlim(0, 42_000)
    ax.set_xlabel("Rolled-up inspection records")
    for bar, value in zip(bars, values):
        ax.text(value + 500, bar.get_y() + bar.get_height() / 2, f"{value:,}", va="center", color=INK, fontsize=10)
    add_header(fig, "30,037 inspections have no recorded grade",
               "73,211 inspection records from 2022 to 2025; grade shares exclude records without A, B, or C")
    add_source(fig, "NYC Restaurant Inspection Results; violation rows rolled up to inspection grain")
    fig.savefig(OUT / "restaurant-grades.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    grouped = grouped[grouped["borough"].isin(["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"])]
    assert len(grouped) == 73_109
    summary = []
    rng = np.random.default_rng(42)
    for borough, frame in grouped.groupby("borough"):
        n = len(frame)
        rate = frame["critical"].mean()
        clusters = [cluster["critical"].to_numpy() for _, cluster in frame.groupby("CAMIS")]
        draws = [np.concatenate([clusters[index] for index in rng.integers(0, len(clusters), len(clusters))]).mean() for _ in range(2000)]
        lower, upper = np.quantile(draws, [0.025, 0.975]) * 100
        summary.append((borough, rate * 100, n, lower, upper))
    summary.sort(key=lambda row: row[1])
    expected = {"Manhattan": (75.9, 27_825), "Brooklyn": (77.1, 18_758), "Queens": (78.2, 17_285), "Bronx": (79.7, 6_771), "Staten Island": (81.7, 2_470)}
    assert all(round(rate, 1) == expected[borough][0] and n == expected[borough][1] for borough, rate, n, _, _ in summary)
    labels = [row[0] for row in summary]
    rates = [row[1] for row in summary]
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.80, bottom=0.15)
    style_axis(ax)
    y = np.arange(len(labels))
    ax.barh(y, rates, color=ACCENT, height=0.56)
    for index, (_, rate, n, lower, upper) in enumerate(summary):
        ax.errorbar(rate, index, xerr=[[rate - lower], [upper - rate]], fmt="none", ecolor=INK, capsize=4, linewidth=1.4)
        ax.text(rate + 1.0, index, f"{rate:.1f}%  | n={n:,} | 95% CI {lower:.1f} to {upper:.1f}%", va="center", color=INK, fontsize=8.5)
    add_header(fig, "Borough differences are descriptive, not a ranking",
               "NYC restaurant inspections, 2022 to 2025; restaurant-cluster bootstrap intervals")
    ax.set_xlabel("Inspections with at least one critical violation (%)")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 100)
    add_source(fig, "NYC Restaurant Inspection Results; unknown borough records excluded; intervals resample restaurants")
    fig.savefig(OUT / "restaurant-risk-by-borough.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_airbnb_charts() -> None:
    source = ROOT / "analysis_data" / "raw" / "airbnb_nyc_june_2026.csv"
    require_source_snapshot(source)
    listings = pd.read_csv(source)
    assert len(listings) == 30_555 and not listings["id"].duplicated().any()
    room_counts = listings["room_type"].value_counts().reindex(
        ["Entire home/apt", "Private room", "Hotel room", "Shared room"], fill_value=0
    )
    assert room_counts.to_dict() == {
        "Entire home/apt": 16_808, "Private room": 13_009, "Hotel room": 520, "Shared room": 218
    }

    labels = ["Entire home", "Private room", "Hotel room", "Shared room"]
    counts = room_counts.to_numpy()
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.21, right=0.92, top=0.80, bottom=0.15)
    bars = ax.barh(labels, counts, color=[ACCENT, SECONDARY, MUTED, BORDER], height=0.58)
    ax.invert_yaxis()
    ax.set_xlim(0, 20_000)
    ax.set_xlabel("Visible listings")
    for bar, count in zip(bars, counts):
        ax.text(count + 350, bar.get_y() + bar.get_height() / 2,
                f"{count:,}  |  {count / len(listings):.1%}", va="center", color=INK, fontsize=10)
    main_share = room_counts.iloc[:2].sum() / len(listings)
    assert round(main_share * 100, 1) == 97.6
    add_header(fig, "Entire homes and private rooms make up 97.6% of visible supply",
               "Inside Airbnb New York snapshot, 14 June 2026; listings are not bookings")
    add_source(fig, "Inside Airbnb New York, June 2026 snapshot")
    fig.savefig(OUT / "airbnb-room-supply.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    host_counts = listings.groupby("host_id", dropna=True).size().sort_values(ascending=False)
    top_host_count = int(np.ceil(len(host_counts) * 0.01))
    top_listings = int(host_counts.iloc[:top_host_count].sum())
    share = top_listings / len(listings)
    assert len(host_counts) == 16_474 and top_host_count == 165 and top_listings == 7_566
    assert round(share * 100, 1) == 24.8
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.25, right=0.88, top=0.79, bottom=0.18)
    labels = ["Top 1% of observed hosts", "All other listings"]
    values = [share * 100, 100 - share * 100]
    bars = ax.barh(labels, values, color=[HIGHLIGHT, SECONDARY], height=0.55)
    ax.invert_yaxis()
    ax.set_xlim(0, 85)
    ax.set_xlabel("Share of all listings (%)")
    for bar, value, count in zip(bars, values, [top_listings, len(listings) - top_listings]):
        ax.text(value + 1, bar.get_y() + bar.get_height() / 2,
                f"{value:.1f}%  |  {count:,} listings", va="center", color=INK, fontsize=10)
    add_header(fig, "The top 1% of observed hosts hold 24.8% of listings",
               "165 of 16,474 observed host IDs; share uses all 30,555 listings as denominator")
    add_source(fig, "Inside Airbnb New York, June 2026 snapshot; concentration is not booking share")
    fig.savefig(OUT / "airbnb-host-concentration.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def load_bank_marketing() -> pd.DataFrame:
    archive = ROOT / "analysis_data" / "raw" / "bank_marketing.zip"
    require_source_snapshot(archive)
    with zipfile.ZipFile(archive) as outer:
        with zipfile.ZipFile(io.BytesIO(outer.read("bank.zip"))) as bank:
            data = pd.read_csv(bank.open("bank-full.csv"), sep=";")
    assert data.shape == (45_211, 17) and not data.isna().any().any()
    assert data["y"].eq("yes").sum() == 5_289
    return data


def save_bank_marketing_charts() -> None:
    data = load_bank_marketing()
    data["positive"] = data["y"].eq("yes")
    summaries = [
        ("contact", ["cellular", "telephone", "unknown"], "Bank-channel response differs sharply by recorded contact type",
         "Share of contacts with a positive outcome; rates do not measure incremental profit"),
        ("poutcome", ["success", "failure", "other", "unknown"], "Prior campaign success is the strongest recorded response signal",
         "Historical response by previous campaign outcome; selection and contact cost are unknown"),
    ]
    for column, order, title, subtitle in summaries:
        grouped = data.groupby(column)["positive"].agg(["mean", "size"]).reindex(order)
        assert grouped["size"].notna().all()
        if column == "contact":
            assert [round(x * 100, 1) for x in grouped["mean"]] == [14.9, 13.4, 4.1]
        else:
            assert round(grouped.loc["success", "mean"] * 100, 1) == 64.7
            assert round(grouped.loc["unknown", "mean"] * 100, 1) == 9.2
        labels = [label.title() for label in order]
        rates = grouped["mean"].to_numpy() * 100
        fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
        style_figure(fig)
        style_axis(ax, grid_axis="x")
        fig.subplots_adjust(left=0.20, right=0.90, top=0.80, bottom=0.16)
        bars = ax.barh(labels, rates, color=[ACCENT if x != "unknown" else HIGHLIGHT for x in order], height=0.58)
        ax.invert_yaxis()
        ax.set_xlim(0, max(rates) * 1.32)
        ax.set_xlabel("Positive response rate (%)")
        for bar, rate, n in zip(bars, rates, grouped["size"]):
            ax.text(rate + max(rates) * 0.025, bar.get_y() + bar.get_height() / 2,
                    f"{rate:.1f}%  |  n={n:,}", va="center", color=INK, fontsize=9.5)
        add_header(fig, title, subtitle)
        add_source(fig, "UCI Bank Marketing, 45,211 contacts; response is not incremental value")
        filename = "bank-channel-response.png" if column == "contact" else "bank-prior-outcome-response.png"
        fig.savefig(OUT / filename, dpi=DPI, facecolor=fig.get_facecolor())
        plt.close(fig)


def save_clickstream_charts() -> None:
    source = ROOT / "analysis_data" / "raw" / "clickstream.zip"
    require_source_snapshot(source)
    events = pd.read_csv(ROOT / "analysis_data" / "extracted" / "e-shop clothing 2008.csv", sep=";")
    assert len(events) == 165_474 and not events.isna().any().any()
    stage_counts = events["page"].value_counts().reindex(range(1, 6), fill_value=0)
    assert stage_counts.tolist() == [93_452, 41_037, 19_301, 8_861, 2_823]
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.80, bottom=0.16)
    bars = ax.bar(stage_counts.index, stage_counts.values, color=[ACCENT, SECONDARY, SECONDARY, SECONDARY, HIGHLIGHT], width=0.68)
    ax.set_xlabel("Page stage")
    ax.set_ylabel("Recorded events")
    ax.set_xticks(range(1, 6))
    ax.set_ylim(0, 108_000)
    for bar, count in zip(bars, stage_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, count + 2200, f"{count:,}", ha="center", color=INK, fontsize=9)
    add_header(fig, "Recorded events fall from 93,452 to 2,823 across five page stages",
               "UCI online-shopping clickstream sample from 2008; stage counts do not identify purchases")
    add_source(fig, "UCI Clickstream Data for Online Shopping; one row per recorded event")
    fig.savefig(OUT / "clickstream-stage-volume.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    depth = events.groupby("session ID").size()
    assert len(depth) == 24_026 and round(depth.gt(1).mean() * 100, 1) == 79.0 and depth.median() == 4
    counts = [int(depth.eq(1).sum()), int(depth.gt(1).sum())]
    shares = np.array(counts) / len(depth) * 100
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax)
    fig.subplots_adjust(left=0.14, right=0.96, top=0.80, bottom=0.19)
    bars = ax.bar(["One event", "More than one event"], shares, color=[MUTED, ACCENT], width=0.58)
    ax.set_ylabel("Share of sessions (%)")
    ax.set_ylim(0, 100)
    for bar, count, share_value in zip(bars, counts, shares):
        ax.text(bar.get_x() + bar.get_width() / 2, share_value + 3,
                f"{share_value:.1f}%  |  {count:,}", ha="center", color=INK, fontsize=10)
    add_header(fig, "79.0% of sessions contain more than one recorded event",
               "24,026 session IDs; the file does not contain confirmed orders")
    add_source(fig, "UCI Clickstream Data for Online Shopping; session depth is not conversion")
    fig.savefig(OUT / "clickstream-session-depth.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_credit_default_chart() -> None:
    source = ROOT / "analysis_data" / "raw" / "credit_default.zip"
    require_source_snapshot(source)
    clients = pd.read_excel(ROOT / "analysis_data" / "extracted" / "default of credit card clients.xls", header=1)
    outcome = clients["default payment next month"]
    assert len(clients) == 30_000 and outcome.value_counts().to_dict() == {0: 23_364, 1: 6_636}
    assert not clients.isna().any().any()
    counts = outcome.value_counts().reindex([0, 1])
    labels = ["No observed default", "Default next month"]
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax)
    fig.subplots_adjust(left=0.14, right=0.96, top=0.80, bottom=0.19)
    bars = ax.bar(labels, counts.values, color=[SECONDARY, HIGHLIGHT], width=0.58)
    ax.set_ylabel("Clients in the 2005 sample")
    ax.set_ylim(0, 28_000)
    for bar, count in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, count + 500,
                f"{count:,}  |  {count / len(clients):.1%}", ha="center", color=INK, fontsize=10)
    add_header(fig, "22.1% of clients defaulted in the following month",
               "Historical Taiwan credit-client sample, 30,000 accounts from 2005; descriptive, not a current score")
    add_source(fig, "UCI Default of Credit Card Clients; outcome is next-month default")
    fig.savefig(OUT / "credit-default-balance.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    clients["limit_quartile"] = pd.qcut(
        clients["LIMIT_BAL"], 4, labels=["Q1 lowest", "Q2", "Q3", "Q4 highest"]
    )
    exposure = clients.groupby("limit_quartile", observed=True)["default payment next month"].agg(["mean", "size"])
    assert [round(value * 100, 1) for value in exposure["mean"]] == [31.8, 24.7, 17.3, 14.0]
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax)
    fig.subplots_adjust(left=0.13, right=0.96, top=0.80, bottom=0.18)
    rates = exposure["mean"].to_numpy() * 100
    ax.plot(range(4), rates, color=HIGHLIGHT, marker="o", linewidth=2.5, markersize=7)
    for index, (rate, count) in enumerate(zip(rates, exposure["size"])):
        ax.annotate(f"{rate:.1f}%  | n={count:,}", (index, rate), xytext=(0, 9),
                    textcoords="offset points", ha="center", color=INK, fontsize=8.5)
    ax.set_xticks(range(4), exposure.index.astype(str))
    ax.set_ylabel("Next-month default rate (%)")
    ax.set_ylim(0, max(rates) + 8)
    add_header(fig, "Observed default rates declined across credit-limit quartiles",
               "Historical Taiwan sample; descriptive group rates, not an automatic lending score")
    add_source(fig, "UCI Default of Credit Card Clients; credit-limit quartiles")
    fig.savefig(OUT / "credit-default-by-exposure.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_airfare_chart() -> None:
    years = ["2024", "2025"]
    current = np.array([384, 387])
    adjusted = np.array([394, 387])
    assert current.tolist() == [384, 387] and adjusted.tolist() == [394, 387]
    x = np.arange(len(years))
    width = 0.30
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax)
    fig.subplots_adjust(left=0.12, right=0.96, top=0.80, bottom=0.18)
    a = ax.bar(x - width / 2, current, width, label="Current dollars", color=ACCENT)
    b = ax.bar(x + width / 2, adjusted, width, label="Inflation-adjusted dollars", color=SECONDARY)
    for bars in (a, b):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                    f"${bar.get_height():.0f}", ha="center", color=INK, fontsize=10)
    ax.set_xticks(x, years)
    ax.set_ylim(0, 460)
    ax.set_ylabel("Annual average domestic itinerary fare (US$)")
    ax.legend(frameon=False, ncols=2, loc="upper right", labelcolor=INK, fontsize=9)
    add_header(fig, "Nominal fare rose; inflation-adjusted fare fell",
               "2024 to 2025 annual U.S. domestic average itinerary fare; annual 2025 combines two ticket-sampling regimes")
    add_source(fig, "U.S. Bureau of Transportation Statistics, 2024 and 2025 annual fare releases")
    fig.savefig(OUT / "airfare-current-adjusted.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def load_happiness_panel() -> tuple[pd.DataFrame, pd.DataFrame]:
    source = ROOT / "analysis_data" / "raw" / "world_happiness_2026.xlsx"
    require_source_snapshot(source)
    data = pd.read_excel(source, sheet_name=0)
    score = "Life evaluation (3-year average)"
    pivot = data.pivot(index="Country name", columns="Year", values=score)
    balanced = pivot.dropna(axis=0, how="any")
    years = list(balanced.columns)
    assert years == [2011, 2012, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    assert len(balanced) == 129
    assert round(balanced[2011].mean(), 2) == 5.47 and round(balanced[2025].mean(), 2) == 5.74
    assert round((balanced[2011].max() - balanced[2011].min()), 1) == 4.8
    assert round((balanced[2025].max() - balanced[2025].min()), 1) == 6.3
    return data, balanced


def save_happiness_charts() -> None:
    data, balanced = load_happiness_panel()
    score = "Life evaluation (3-year average)"
    years = list(balanced.columns)
    means = balanced.mean(axis=0)

    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.16)
    style_axis(ax)
    ax.plot(years, means, color=ACCENT, marker="o", markersize=5, linewidth=2.4)
    ax.axvspan(2021, 2022, color=WARNING_FILL, zorder=0)
    ax.set_xlim(2010.7, 2025.3)
    ax.set_ylim(5.2, 5.95)
    ax.set_xticks(years, [str(y) for y in years], rotation=45, ha="right")
    ax.set_ylabel("Mean life evaluation (0 to 10)")
    for year in (2011, 2025):
        ax.annotate(f"{means.loc[year]:.2f}", (year, means.loc[year]), xytext=(0, 9),
                    textcoords="offset points", ha="center", color=INK, fontsize=10, fontweight="bold")
    add_header(fig, "The balanced-country average recovered after the 2021 to 2022 dip",
               "129 countries present in all 14 measured years; unweighted national averages, not a population-weighted global estimate")
    add_source(fig, "World Happiness Report 2026, Figure 2.1; country life evaluations")
    fig.savefig(OUT / "happiness-beat01.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    shutil.copyfile(OUT / "happiness-beat01.png", OUT / "happiness-drivers-trend.png")

    change = balanced[2025] - balanced[2011]
    top_gains = change.nlargest(8).sort_values()
    largest_losses = change.nsmallest(4).sort_values()
    labels = list(largest_losses.index) + list(top_gains.index)
    values = list(largest_losses.values) + list(top_gains.values)
    colors = [HIGHLIGHT] * len(largest_losses) + [SECONDARY] * len(top_gains)
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.23, right=0.93, top=0.80, bottom=0.14)
    bars = ax.barh(labels, values, color=colors, height=0.62)
    ax.axvline(0, color=BORDER, linewidth=1)
    for bar, value in zip(bars, values):
        offset = 0.05 if value >= 0 else -0.05
        ax.text(value + offset, bar.get_y() + bar.get_height() / 2, f"{value:+.2f}",
                va="center", ha="left" if value >= 0 else "right", color=INK, fontsize=9)
    ax.set_xlim(-3.2, 2.65)
    ax.set_xlabel("Change in life evaluation, 2011 to 2025 (points)")
    add_header(fig, "Country scores moved in both directions across the balanced panel",
               "Largest gains and losses among 129 countries measured in both 2011 and 2025")
    add_source(fig, "World Happiness Report 2026, Figure 2.1; change is descriptive, not a policy effect")
    fig.savefig(OUT / "happiness-beat02.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    shutil.copyfile(OUT / "happiness-beat02.png", OUT / "happiness-drivers-movers.png")

    year_data = data[data["Year"].eq(2025)].copy()
    top = year_data.nlargest(10, score)
    bottom = year_data.nsmallest(10, score)
    components = [
        ("GDP per person", "Explained by: Log GDP per capita"),
        ("Social support", "Explained by: Social support"),
        ("Life expectancy", "Explained by: Healthy life expectancy"),
    ]
    gaps = [top[column].mean() - bottom[column].mean() for _, column in components]
    assert [round(value, 2) for value in gaps] == [0.83, 0.83, 0.62]
    labels = [label for label, _ in components]
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.25, right=0.92, top=0.78, bottom=0.18)
    bars = ax.barh(labels, gaps, color=[ACCENT, SECONDARY, HIGHLIGHT], height=0.58)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Average component gap (points)")
    for bar, gap in zip(bars, gaps):
        ax.text(gap + 0.025, bar.get_y() + bar.get_height() / 2, f"{gap:.2f}", va="center", color=INK, fontsize=10)
    add_header(fig, "Largest top-bottom gaps: income, support, health",
               "Average component differences between the top 10 and bottom 10 countries in 2025")
    add_source(fig, "World Happiness Report 2026, Figure 2.1; descriptive group comparison")
    fig.savefig(OUT / "happiness-beat03.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    factor_columns = [
        ("Social support", "Explained by: Social support"),
        ("GDP per person", "Explained by: Log GDP per capita"),
        ("Life expectancy", "Explained by: Healthy life expectancy"),
        ("Freedom", "Explained by: Freedom to make life choices"),
        ("Low corruption", "Explained by: Perceptions of corruption"),
        ("Generosity", "Explained by: Generosity"),
    ]
    recent = data[data["Year"].between(2019, 2025)]
    correlations = [recent[score].corr(recent[column]) for _, column in factor_columns]
    assert [round(x, 2) for x in correlations if np.isfinite(x)][:3] == [0.70, 0.68, 0.66]
    order = np.argsort(correlations)
    labels = [factor_columns[i][0] for i in order]
    values = [correlations[i] for i in order]
    colors = [HIGHLIGHT if x < 0.1 else ACCENT for x in values]
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.22, right=0.92, top=0.80, bottom=0.16)
    bars = ax.barh(labels, values, color=colors, height=0.58)
    ax.set_xlim(0, 0.85)
    ax.set_xlabel("Correlation with life evaluation (r)")
    for bar, value in zip(bars, values):
        ax.text(value + 0.02, bar.get_y() + bar.get_height() / 2, f"{value:.2f}", va="center", color=INK, fontsize=9)
    add_header(fig, "Social support, income, and health relate most strongly",
               "Country-year relationships from 2019 to 2025; factors are correlated and are not causal levers")
    add_source(fig, "World Happiness Report 2026, Figure 2.1; Pearson correlation")
    fig.savefig(OUT / "happiness-beat04.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    shutil.copyfile(OUT / "happiness-beat04.png", OUT / "happiness-drivers-correlations.png")
    teaser = OUT / "world-happiness-drivers-2005-2025" / "teaser.png"
    teaser.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT / "happiness-beat04.png", teaser)

    ranges = balanced.max(axis=0) - balanced.min(axis=0)
    assert round(ranges.loc[2011], 1) == 4.8 and round(ranges.loc[2025], 1) == 6.3
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.16)
    style_axis(ax)
    ax.plot(years, ranges, color=HIGHLIGHT, marker="o", markersize=5, linewidth=2.2)
    ax.set_xticks(years, [str(y) for y in years], rotation=45, ha="right")
    ax.set_ylabel("Highest minus lowest country score (points)")
    for year in (2011, 2025):
        ax.annotate(f"{ranges.loc[year]:.1f}", (year, ranges.loc[year]), xytext=(0, 9),
                    textcoords="offset points", ha="center", color=INK, fontsize=10, fontweight="bold")
    add_header(fig, "The highest-to-lowest country score gap widened",
               "Range within the same 129-country panel, 2011 to 2025; dispersion alone does not show how the bottom group changed")
    add_source(fig, "World Happiness Report 2026, Figure 2.1; max-minus-min country score")
    fig.savefig(OUT / "happiness-drivers-inequality.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def load_netflix_data() -> pd.DataFrame:
    source = ROOT / "analysis_data" / "raw" / "netflix_titles.csv"
    require_source_snapshot(source)
    data = pd.read_csv(source)
    assert len(data) == 8_807 and data["show_id"].is_unique
    assert data.duplicated(["title", "type"]).sum() == 0
    data["date_added_parsed"] = pd.to_datetime(data["date_added"].str.strip(), format="%B %d, %Y", errors="coerce")
    data["year_added"] = data["date_added_parsed"].dt.year
    data["acquisition_lag"] = data["year_added"] - data["release_year"]
    data.loc[data["acquisition_lag"] < 0, "acquisition_lag"] = np.nan
    data["primary_country"] = data["country"].str.split(",").str[0].str.strip()
    countries = {"United States": "US", "United Kingdom": "UK", "India": "India", "South Korea": "South Korea",
                 "Japan": "Japan", "France": "France", "Canada": "Canada", "Spain": "Spain"}
    data["country_bucket"] = data["primary_country"].map(countries)
    data.loc[data["primary_country"].isna(), "country_bucket"] = "Unknown"
    data["country_bucket"] = data["country_bucket"].fillna("Other")

    def rating_tier(value: str | float) -> str:
        if pd.isna(value):
            return "Unknown"
        if value in {"TV-Y", "TV-Y7", "TV-Y7-FV", "TV-G", "G"}:
            return "Kids"
        if value in {"TV-14", "PG-13", "PG"}:
            return "Teen"
        if value in {"TV-MA", "R", "NC-17", "NR", "UR"}:
            return "Adult"
        return "Unknown"

    def lag_bucket(value: float) -> str:
        if pd.isna(value):
            return "Unknown"
        if value == 0:
            return "Fresh (0)"
        if value <= 2:
            return "Recent (1-2)"
        if value <= 5:
            return "Mid (3-5)"
        return "Library (6+)"

    data["rating_tier"] = data["rating"].map(rating_tier)
    data["lag_bucket"] = data["acquisition_lag"].map(lag_bucket)
    return data


def save_netflix_charts() -> None:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import LabelEncoder, StandardScaler

    data = load_netflix_data()
    us = data[(data["country_bucket"] == "US") & data["year_added"].between(2015, 2021)].copy()
    us["is_fresh"] = us["acquisition_lag"].eq(0.0)
    fresh = us.groupby(["year_added", "type"])["is_fresh"].mean().unstack() * 100
    overall = us.groupby("year_added")["is_fresh"].mean() * 100
    assert round(fresh.loc[2015, "TV Show"]) == 40
    assert round(fresh.loc[2021, "TV Show"]) == 61
    assert round(overall.loc[2015]) == 72 and round(overall.loc[2021]) == 28
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    fig.subplots_adjust(left=0.08, right=0.90, top=0.80, bottom=0.16)
    style_axis(ax)
    ax.plot(fresh.index, fresh["TV Show"], color=ACCENT, marker="o", linewidth=2.4, label="TV shows")
    ax.plot(fresh.index, fresh["Movie"], color=SECONDARY, marker="o", linewidth=2.1, label="Movies")
    ax.set_xlim(2015, 2021.8)
    ax.set_ylim(0, 100)
    ax.set_xticks(range(2015, 2022))
    ax.set_ylabel("Same-year acquisitions (%)")
    for content_type, color in [("TV Show", ACCENT), ("Movie", SECONDARY)]:
        ax.annotate(f"{fresh.loc[2021, content_type]:.0f}%", (2021, fresh.loc[2021, content_type]),
                    xytext=(8, 0), textcoords="offset points", va="center", color=color, fontweight="bold")
    add_header(fig, "US TV additions grew fresher as movies shifted to the library",
               "Share of US titles added in their release year, 2015 to 2021; freshness is not content quality")
    add_source(fig, "Netflix Movies and TV Shows dataset by Shivam Bansal; Kaggle snapshot preserved via Zenodo")
    fig.savefig(OUT / "netflix-beat01.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    clustered = data.dropna(subset=["year_added", "acquisition_lag"]).copy().reset_index(drop=True)
    top_genres = clustered["listed_in"].str.split(", ").explode().value_counts().head(15).index.tolist()
    genre_columns = []
    for genre in top_genres:
        safe = genre.replace(" ", "_").replace("&", "and").replace("'", "")
        column = f"g_{safe}"
        clustered[column] = clustered["listed_in"].str.contains(genre, regex=False).fillna(False).astype(int)
        genre_columns.append(column)
    for column, encoded in [("type", "type_enc"), ("rating_tier", "rating_enc"), ("lag_bucket", "lag_enc")]:
        clustered[encoded] = LabelEncoder().fit_transform(clustered[column])
    features = genre_columns + ["type_enc", "rating_enc", "lag_enc"]
    scaled = StandardScaler().fit_transform(clustered[features].values.astype(float))
    clustered["cluster"] = KMeans(n_clusters=5, random_state=42, n_init=10).fit_predict(scaled)
    dominant_genres = {}
    for cluster_id in range(5):
        block = clustered[clustered["cluster"] == cluster_id]
        counts = pd.Series({g: block["listed_in"].str.contains(g, regex=False).sum() for g in top_genres})
        dominant_genres[cluster_id] = counts.sort_values(ascending=False).index.tolist()[:2]
    assert set(dominant_genres[0]) == {"International Movies", "Dramas"}
    assert dominant_genres[2][0] == "Documentaries"
    assert dominant_genres[3][0] == "Children & Family Movies"
    labels = {0: "International drama", 2: "Documentaries", 3: "Children and family"}
    us_movies = clustered[(clustered["country_bucket"] == "US")
                          & clustered["year_added"].between(2015, 2021)
                          & clustered["type"].eq("Movie")].copy()
    us_movies["deep_library"] = us_movies["acquisition_lag"] > 5
    us_movies["period"] = np.where(us_movies["year_added"] <= 2017, "2015 to 2017", "2018 to 2021")
    us_movies["group"] = us_movies["cluster"].map(labels)
    library = us_movies[us_movies["group"].notna()].groupby(["group", "period"])["deep_library"].mean().unstack() * 100
    changes = library["2018 to 2021"] - library["2015 to 2017"]
    assert round(library.loc["International drama", "2015 to 2017"], 1) == 5.5
    assert round(library.loc["International drama", "2018 to 2021"], 1) == 47.4
    assert round(library.loc["Children and family", "2015 to 2017"], 1) == 16.4
    assert round(library.loc["Children and family", "2018 to 2021"], 1) == 48.0
    plot_labels = ["International drama", "Children and family", "Documentaries"]
    plot_values = [changes[label] for label in plot_labels]
    fig, ax = plt.subplots(figsize=(9, 5.5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.27, right=0.91, top=0.80, bottom=0.16)
    colors = [ACCENT if value >= 0 else MUTED for value in plot_values]
    bars = ax.barh(plot_labels, plot_values, color=colors, height=0.58)
    ax.axvline(0, color=BORDER, linewidth=1)
    for bar, value in zip(bars, plot_values):
        offset = 0.6 if value >= 0 else -0.6
        ax.text(value + offset, bar.get_y() + bar.get_height() / 2, f"{value:+.1f} pp",
                va="center", ha="left" if value >= 0 else "right", color=INK, fontsize=9)
    ax.set_xlim(-10, 50)
    ax.set_xlabel("Change in deep-library share (percentage points)")
    ax.invert_yaxis()
    add_header(fig, "Deep-library share rose most in drama and family films",
               "US movie additions; acquisition lag over 5 years, comparing 2015 to 2017 with 2018 to 2021")
    add_source(fig, "Netflix Movies and TV Shows dataset by Shivam Bansal; KMeans segment labels use dominant genre")
    fig.savefig(OUT / "netflix-beat03.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    uk = data[data["country_bucket"].eq("UK")].copy()
    uk["completeness"] = uk[["director", "cast", "country"]].notna().sum(axis=1) / 3
    uk["is_sparse"] = uk["completeness"] < 0.34
    vintage_order = ["Pre-2000s", "2000s", "2010s", "2020s"]
    uk["vintage_label"] = pd.cut(
        uk["release_year"], bins=[0, 1999, 2009, 2019, 2030], labels=vintage_order
    )
    sparse = uk.groupby("vintage_label")["is_sparse"].agg(["mean", "size"]).reindex(vintage_order)
    assert int(sparse.loc["2020s", "size"]) == 86 and round(sparse.loc["2020s", "mean"] * 100, 1) == 12.8
    assert round(sparse.loc["2010s", "mean"] * 100, 1) == 6.3
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.80, bottom=0.16)
    style_axis(ax)
    x = np.arange(len(vintage_order))
    values = sparse["mean"].to_numpy() * 100
    ax.plot(x, values, color=HIGHLIGHT, marker="o", markersize=7, linewidth=2.5)
    for index, value in enumerate(values):
        ax.annotate(f"{value:.1f}%", (index, value), xytext=(0, 10), textcoords="offset points",
                    ha="center", color=INK, fontweight="bold")
    ax.set_xticks(x, vintage_order)
    ax.set_ylim(0, max(values) + 5)
    ax.set_ylabel("Titles with sparse core metadata (%)")
    add_header(fig, "Sparse metadata rose for newer UK releases",
               "Release vintage; sparse means at least 2 of director, cast, and country are missing")
    add_source(fig, "Netflix Movies and TV Shows dataset by Shivam Bansal; 86 UK titles released in the 2020s")
    fig.savefig(OUT / "netflix-beat05.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    movies_us = us[us["type"].eq("Movie")].copy()
    def lag_band(value: float) -> str:
        if pd.isna(value):
            return "Unknown"
        if value == 0:
            return "Fresh (0)"
        if value <= 2:
            return "Recent (1 to 2)"
        if value <= 5:
            return "Mid (3 to 5)"
        return "Library (6+)"
    movies_us["lag_band"] = movies_us["acquisition_lag"].map(lag_band)
    bands = ["Fresh (0)", "Recent (1 to 2)", "Mid (3 to 5)", "Library (6+)", "Unknown"]
    lag_mix = movies_us.groupby(["year_added", "lag_band"]).size().unstack(fill_value=0).reindex(columns=bands, fill_value=0)
    lag_share = lag_mix.div(lag_mix.sum(axis=1), axis=0) * 100
    assert round(lag_share.loc[2015, "Library (6+)"]) == 0
    assert round(lag_share.loc[2021, "Library (6+)"]) == 65
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.16)
    style_axis(ax)
    palette = {"Fresh (0)": BORDER, "Recent (1 to 2)": SECONDARY, "Mid (3 to 5)": MUTED,
               "Library (6+)": ACCENT, "Unknown": WARNING}
    bottom = np.zeros(len(lag_share))
    for band in bands:
        values = lag_share[band].to_numpy()
        ax.bar(lag_share.index, values, bottom=bottom, width=0.72, color=palette[band], label=band)
        if band == "Library (6+)":
            for index, value in enumerate(values):
                if value >= 8:
                    ax.text(lag_share.index[index], bottom[index] + value / 2, f"{value:.0f}%",
                            ha="center", va="center", color=PAPER, fontsize=8, fontweight="bold")
        bottom += values
    ax.set_ylim(0, 100)
    ax.set_xticks(lag_share.index)
    ax.set_ylabel("Share of US movie additions (%)")
    ax.legend(frameon=False, ncols=5, loc="upper center", bbox_to_anchor=(0.5, -0.13), fontsize=8, labelcolor=INK)
    add_header(fig, "Deep-library movies made up a growing share of US additions",
               "Acquisition lag by year added, 2015 to 2021; deep library means more than five years")
    add_source(fig, "Netflix Movies and TV Shows dataset by Shivam Bansal")
    fig.savefig(OUT / "netflix-beat02.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    movie_directors = data[(data["type"].eq("Movie")) & data["director"].notna()].merge(
        clustered[["show_id", "cluster"]], on="show_id", how="inner"
    )
    movie_directors["group"] = movie_directors["cluster"].map(labels)
    base_share = movie_directors["group"].value_counts(normalize=True) * 100
    director_counts = movie_directors.groupby("director").size()
    top_directors = director_counts.nlargest(50).index
    top_share = movie_directors[movie_directors["director"].isin(top_directors)]["group"].value_counts(normalize=True) * 100
    compare = pd.DataFrame({"All attributed movies": base_share, "Top 50 directors": top_share}).fillna(0)
    groups = ["International drama", "Documentaries", "Children and family"]
    compare = compare.reindex(groups)
    assert len(movie_directors) == 5_941 and int(movie_directors["director"].nunique()) > 50
    assert round(compare.loc["Documentaries", "All attributed movies"], 1) == 13.4
    assert round(compare.loc["Documentaries", "Top 50 directors"], 1) == 1.4
    y = np.arange(len(groups))
    height = 0.34
    fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax, grid_axis="x")
    fig.subplots_adjust(left=0.22, right=0.95, top=0.80, bottom=0.16)
    bars_a = ax.barh(y - height / 2, compare["All attributed movies"], height, color=ACCENT, label="All attributed movies")
    bars_b = ax.barh(y + height / 2, compare["Top 50 directors"], height, color=SECONDARY, label="Top 50 directors")
    for bars in (bars_a, bars_b):
        for bar in bars:
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f"{bar.get_width():.1f}%",
                    va="center", color=INK, fontsize=8)
    ax.set_yticks(y, groups)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of movie titles with a recorded director (%)")
    ax.legend(frameon=False, loc="lower right", labelcolor=INK, fontsize=9)
    add_header(fig, "Top directors contributed fewer documentaries than the catalog mix",
               "5,941 movies have a recorded director; the top 50 directors account for 421 titles")
    add_source(fig, "Netflix Movies and TV Shows dataset; director concentration is descriptive")
    fig.savefig(OUT / "netflix-beat04.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    tv = data[(data["type"].eq("TV Show")) & data["duration"].notna()].copy()
    tv["seasons"] = pd.to_numeric(tv["duration"].str.extract(r"(\d+)")[0], errors="coerce")
    tv["one_season"] = tv["seasons"].eq(1)
    tv["cohort"] = np.where(tv["year_added"].between(2015, 2018), "2015 to 2018",
                            np.where(tv["year_added"].eq(2021), "2021", "Exclude"))
    tv["region"] = np.where(tv["country_bucket"].eq("US"), "US",
                           np.where(tv["country_bucket"].isin(["Unknown", "Multiple"]), "Exclude", "International"))
    tv = tv[(tv["cohort"] != "Exclude") & (tv["region"] != "Exclude")]
    season_share = tv.groupby(["cohort", "region"])["one_season"].agg(["mean", "size"]).unstack("region")
    assert round(season_share.loc["2015 to 2018", ("mean", "International")] * 100, 1) == 76.6
    assert round(season_share.loc["2021", ("mean", "International")] * 100, 1) == 49.5
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=CANVAS)
    style_figure(fig)
    style_axis(ax)
    fig.subplots_adjust(left=0.13, right=0.96, top=0.80, bottom=0.18)
    x = np.arange(2)
    width = 0.32
    regions = ["US", "International"]
    for offset, region, color in [(-width / 2, "US", ACCENT), (width / 2, "International", SECONDARY)]:
        values = season_share.loc[["2015 to 2018", "2021"], ("mean", region)].to_numpy() * 100
        counts = season_share.loc[["2015 to 2018", "2021"], ("size", region)].to_numpy()
        bars = ax.bar(x + offset, values, width, label=region, color=color)
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 2, f"{value:.1f}%",
                    ha="center", color=INK, fontsize=8)
    ax.set_xticks(x, ["2015 to 2018", "2021"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("One-season share of TV shows (%)")
    ax.legend(frameon=False, ncols=2, loc="upper right", labelcolor=INK, fontsize=9)
    add_header(fig, "One-season TV share fell in both regions",
               "Share of TV additions with one season in two cohorts; catalog length is not completion or viewing")
    add_source(fig, "Netflix Movies and TV Shows dataset by Shivam Bansal")
    fig.savefig(OUT / "netflix-beat06.png", dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    tasks = {
        "airbnb": save_airbnb_charts,
        "airfare": save_airfare_chart,
        "bank": save_bank_marketing_charts,
        "clickstream": save_clickstream_charts,
        "credit": save_credit_default_chart,
        "fake-job": save_fake_job_model_comparison,
        "happiness": save_happiness_charts,
        "jolts": save_jolts_signals,
        "netflix": save_netflix_charts,
        "sec": save_sec_charts,
        "taxi": save_taxi_completed_trips,
        "retail": save_retail_charts,
        "restaurant": save_restaurant_risk_by_borough,
    }
    requested = sys.argv[1:] or list(tasks)
    unknown = sorted(set(requested) - tasks.keys())
    if unknown:
        raise SystemExit(f"Unknown task(s): {', '.join(unknown)}. Choose from: {', '.join(tasks)}")
    for name in requested:
        tasks[name]()
        print(f"validated: {name}")
