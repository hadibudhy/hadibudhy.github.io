import hashlib
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "images"

SOURCE_SNAPSHOTS = {
    "Online Retail.xlsx": "43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d",
    "nyc_restaurants.csv": "a02bf468aaf826c64a78b6ad17e038908d643e769dcb4ee8257b5a6282519bb1",
}


def require_source_snapshot(path: Path) -> None:
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = SOURCE_SNAPSHOTS[path.name]
    if actual != expected:
        raise ValueError(
            f"Source snapshot drift for {path}: expected SHA-256 {expected}, got {actual}. "
            "Revalidate the published metrics before replacing the recorded snapshot."
        )


def style_axis(ax):
    ax.set_facecolor("#0b1728")
    ax.grid(axis="y", color="#334155", alpha=0.55, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color("#475569")
    ax.tick_params(colors="#a7b5ca", labelsize=12)
    ax.xaxis.label.set_color("#c7d2e1")
    ax.yaxis.label.set_color("#c7d2e1")


def save_fake_job_model_comparison() -> None:
    labels = ["Text model\n(Logistic regression)", "Profile details\n(LightGBM)", "Combined model\n(default)", "Combined model\n(tuned threshold)"]
    f1 = [0.819, 0.828, 0.831, 0.850]
    recall = [0.913, 0.723, 0.711, 0.751]
    pr_auc = [0.927, 0.915, 0.901, 0.901]
    x = np.arange(len(labels))
    width = 0.24

    fig, ax = plt.subplots(figsize=(16, 8.5), facecolor="#07111f")
    fig.subplots_adjust(top=0.78, bottom=0.2, left=0.09, right=0.97)
    style_axis(ax)
    bars = [
        ax.bar(x - width, f1, width, label="F1", color="#4f78b8"),
        ax.bar(x, recall, width, label="Recall", color="#4db07f"),
        ax.bar(x + width, pr_auc, width, label="PR-AUC", color="#df8150"),
    ]
    for group in bars:
        for bar in group:
            ax.annotate(f"{bar.get_height():.3f}", (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 5), textcoords="offset points", ha="center", va="bottom",
                        color="#e5edf8", fontsize=10, fontweight="bold")
    ax.set_title("Text-first screening catches more scams; the tuned model has the highest F1", color="#f3f6fb", fontsize=20, fontweight="bold", pad=28)
    ax.text(0.5, 1.025, "Employment Scam Aegean Dataset | 17,880 labeled posts | held-out test metrics | higher is better",
            transform=ax.transAxes, ha="center", color="#9fb0c6", fontsize=12)
    ax.set_ylabel("Model score")
    ax.set_ylim(0.6, 1.02)
    ax.set_xticks(x, labels)
    ax.legend(frameon=False, ncols=3, loc="upper left", labelcolor="#e5edf8", fontsize=11)
    fig.savefig(OUT / "fake-job-all-models.png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_jolts_signals() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(16, 8.5), facecolor="#07111f", gridspec_kw={"wspace": 0.28})
    fig.subplots_adjust(top=0.76, bottom=0.18, left=0.08, right=0.97)
    for ax in axes:
        style_axis(ax)

    counts = [6.55, 5.203]
    count_bars = axes[0].bar(["Open positions\n(stock)", "Separations\n(monthly flow)"], counts, color=["#5e9bea", "#f36d72"], width=0.58)
    axes[0].set_title("Counts use different time bases", color="#f3f6fb", fontsize=17, fontweight="bold", pad=20)
    axes[0].set_ylabel("People (millions; definitions differ)")
    axes[0].set_ylim(0, 7.2)
    for bar, value in zip(count_bars, counts):
        axes[0].annotate(f"{value:.3f}M", (bar.get_x() + bar.get_width() / 2, value), xytext=(0, 7),
                         textcoords="offset points", ha="center", color="#e5edf8", fontsize=12, fontweight="bold")

    rates = [3.3, 2.0]
    rate_bars = axes[1].bar(["Hires", "Quits"], rates, color=["#5e9bea", "#f36d72"], width=0.58)
    axes[1].set_title("Hires and quits are rates, not counts", color="#f3f6fb", fontsize=17, fontweight="bold", pad=20)
    axes[1].set_ylabel("Rate (%)")
    axes[1].set_ylim(0, 4.2)
    for bar, value in zip(rate_bars, rates):
        axes[1].annotate(f"{value:.1f}%", (bar.get_x() + bar.get_width() / 2, value), xytext=(0, 7),
                         textcoords="offset points", ha="center", color="#e5edf8", fontsize=12, fontweight="bold")

    fig.suptitle("December 2025 workforce signals need separate units", color="#f3f6fb", fontsize=21, fontweight="bold")
    fig.text(0.5, 0.03, "U.S. BLS JOLTS aggregate | openings are a point-in-time stock; separations are a monthly flow; hires and quits are rates",
             ha="center", color="#9fb0c6", fontsize=12)
    fig.savefig(OUT / "jolts-december-signals.png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_sec_net_margin() -> None:
    years = ["FY2023", "FY2024", "FY2025"]
    margins = [34.14, 35.96, 36.15]
    fig, ax = plt.subplots(figsize=(16, 8.5), facecolor="#07111f")
    fig.subplots_adjust(top=0.82, bottom=0.16, left=0.10, right=0.97)
    style_axis(ax)
    ax.plot(years, margins, color="#ff963d", marker="o", linewidth=3, markersize=9)
    for year, value in zip(years, margins):
        ax.annotate(f"{value:.1f}%", (year, value), xytext=(0, 10), textcoords="offset points",
                    ha="center", color="#e5edf8", fontsize=12, fontweight="bold")
    ax.set_title("Reported net margin rose from 34.1% to 36.1%", color="#f3f6fb", fontsize=20, fontweight="bold", pad=24)
    ax.text(0.5, 1.025, "Microsoft reported results | FY2023–FY2025 | net income ÷ revenue | full percentage scale",
            transform=ax.transAxes, ha="center", color="#9fb0c6", fontsize=12)
    ax.set_ylabel("Net margin (%)")
    ax.set_ylim(0, 40)
    ax.set_yticks(range(0, 41, 10))
    fig.savefig(OUT / "sec-net-margin.png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_taxi_completed_trips() -> None:
    source = ROOT / "analysis_data" / "raw" / "nyc_taxi_january_2025.parquet"
    trips = pd.read_parquet(source)
    trips["duration_minutes"] = (trips["tpep_dropoff_datetime"] - trips["tpep_pickup_datetime"]).dt.total_seconds() / 60
    valid = trips[(trips["trip_distance"] > 0) & (trips["fare_amount"] > 0) & trips["duration_minutes"].between(1, 120)]
    hourly = valid.groupby(valid["tpep_pickup_datetime"].dt.hour).size().reindex(range(24), fill_value=0) / 1000
    fig, ax = plt.subplots(figsize=(16, 8.5), facecolor="#07111f")
    fig.subplots_adjust(top=0.82, bottom=0.16, left=0.10, right=0.97)
    style_axis(ax)
    ax.bar(hourly.index, hourly.values, color="#5e9bea", width=0.8)
    ax.set_title("Completed-trip activity peaked between 17:00 and 19:00", color="#f3f6fb", fontsize=20, fontweight="bold", pad=24)
    ax.text(0.5, 1.025, "NYC yellow taxi | January 2025 | 3.31M valid completed trips | trips per pickup hour",
            transform=ax.transAxes, ha="center", color="#9fb0c6", fontsize=12)
    ax.set_xlabel("Pickup hour")
    ax.set_ylabel("Completed trips (thousands)")
    ax.set_xticks(range(24))
    ax.set_ylim(0, max(hourly.max() * 1.1, 250))
    fig.savefig(OUT / "taxi-demand-by-hour.png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)


def save_retail_market_opportunity() -> None:
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
    country = sales.groupby("Country")["revenue"].sum().sort_values(ascending=False).head(8) / 1_000_000
    assert np.isclose(country["United Kingdom"] * 1_000_000 / customer_revenue.sum(), 0.8201163759)
    fig, axes = plt.subplots(1, 2, figsize=(16, 8.5), facecolor="#07111f", gridspec_kw={"width_ratios": [1, 1.15]})
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.12, right=0.97, wspace=0.34)
    for ax in axes:
        style_axis(ax)
    axes[0].barh(["United Kingdom"], [country["United Kingdom"]], color="#22c7df", height=0.5)
    axes[0].set_title("The UK is the revenue base", color="#f3f6fb", fontsize=17, fontweight="bold", pad=20)
    axes[0].set_xlabel("Recorded revenue (£ millions)")
    axes[0].set_xlim(0, country["United Kingdom"] * 1.12)
    axes[0].invert_yaxis()
    axes[0].text(country["United Kingdom"] / 2, 0, f"£{country['United Kingdom']:.2f}m", ha="center", va="center", color="#07111f", fontweight="bold")
    other = country.drop("United Kingdom").sort_values()
    axes[1].barh(other.index, other.values, color="#22c7df", height=0.55)
    axes[1].set_title("Smaller markets require validation", color="#f3f6fb", fontsize=17, fontweight="bold", pad=20)
    axes[1].set_xlabel("Recorded revenue (£ millions)")
    axes[1].invert_yaxis()
    for label, value in other.items():
        axes[1].text(value + 0.01, label, f"£{value:.2f}m", va="center", color="#e5edf8", fontsize=10)
    fig.suptitle("Historical revenue concentration identifies test markets, not expansion attractiveness", color="#f3f6fb", fontsize=21, fontweight="bold")
    fig.text(0.5, 0.03, "UCI Online Retail | 1 Dec 2010–9 Dec 2011 | cleaned positive, non-cancelled lines with CustomerID | revenue, not margin",
             ha="center", color="#9fb0c6", fontsize=12)
    fig.savefig(OUT / "retail-market-opportunity.png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)


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
    fig, ax = plt.subplots(figsize=(16, 8.5), facecolor="#07111f")
    fig.subplots_adjust(top=0.78, bottom=0.20, left=0.10, right=0.97)
    style_axis(ax)
    y = np.arange(len(labels))
    ax.barh(y, rates, color="#f36d72", height=0.56)
    for index, (_, rate, n, lower, upper) in enumerate(summary):
        ax.errorbar(rate, index, xerr=[[rate - lower], [upper - rate]], fmt="none", ecolor="#f3f6fb", capsize=5, linewidth=2)
        ax.text(rate + 1.0, index, f"{rate:.1f}%  | n={n:,} | 95% CI {lower:.1f}–{upper:.1f}%", va="center", color="#e5edf8", fontsize=10)
    ax.set_title("Borough differences are descriptive, not a ranking", color="#f3f6fb", fontsize=20, fontweight="bold", pad=24)
    ax.text(0.5, 1.025, "NYC restaurant inspections | 2022–2025 | inspection-level roll-up | restaurant-cluster bootstrap intervals",
            transform=ax.transAxes, ha="center", color="#9fb0c6", fontsize=12)
    ax.set_xlabel("Inspections with at least one critical violation (%)")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 100)
    fig.text(0.5, 0.04, "Unknown borough records excluded; 95% intervals resample restaurants, not individual inspection rows",
             ha="center", color="#9fb0c6", fontsize=12)
    fig.savefig(OUT / "restaurant-risk-by-borough.png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    tasks = {
        "fake-job": save_fake_job_model_comparison,
        "jolts": save_jolts_signals,
        "sec": save_sec_net_margin,
        "taxi": save_taxi_completed_trips,
        "retail": save_retail_market_opportunity,
        "restaurant": save_restaurant_risk_by_borough,
    }
    requested = sys.argv[1:] or list(tasks)
    unknown = sorted(set(requested) - tasks.keys())
    if unknown:
        raise SystemExit(f"Unknown task(s): {', '.join(unknown)}. Choose from: {', '.join(tasks)}")
    for name in requested:
        tasks[name]()
        print(f"validated: {name}")
