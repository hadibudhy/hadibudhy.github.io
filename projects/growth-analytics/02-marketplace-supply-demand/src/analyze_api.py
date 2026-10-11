"""Fetch the bounded official HVFHV Open Data slice and regenerate its chart."""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[4]
OUTPUT = ROOT / "analysis_data" / "growth_sources" / "hvf_hourly_2019.json"
CHART = ROOT / "public" / "images" / "growth-hvf-hourly.png"
MONTHLY = ROOT / "analysis_data" / "growth_sources" / "data_reports_monthly.csv"
API = "https://data.cityofnewyork.us/resource/4p5c-cbgn.json"
PARAMS = {
    "$select": "date_extract_hh(pickup_datetime) as hour,count(*) as trips",
    "$where": "pickup_datetime >= '2019-02-01T00:00:00' and pickup_datetime < '2019-02-08T00:00:00'",
    "$group": "hour",
    "$order": "hour",
    "$limit": "100",
}


def render_monthly_summary(monthly: pd.DataFrame) -> None:
    monthly = monthly.copy()
    monthly["year"] = pd.to_datetime(monthly["month"]).dt.year
    averages = monthly.groupby("year")[["Trips Per Day", "Unique Drivers", "Avg Hours Per Day Per Driver"]].mean()
    rows = [
        ["Average trips per day", f"{int(averages.loc[2024, 'Trips Per Day'] + 0.5):,}", f"{int(averages.loc[2025, 'Trips Per Day'] + 0.5):,}"],
        ["Unique drivers per month", f"{int(averages.loc[2024, 'Unique Drivers'] + 0.5):,}", f"{int(averages.loc[2025, 'Unique Drivers'] + 0.5):,}"],
        ["Hours per driver per day", f"{averages.loc[2024, 'Avg Hours Per Day Per Driver']:.2f}", f"{averages.loc[2025, 'Avg Hours Per Day Per Driver']:.2f}"],
    ]
    changes = [
        (averages.loc[2025, metric] / averages.loc[2024, metric] - 1) * 100
        for metric in ("Trips Per Day", "Unique Drivers", "Avg Hours Per Day Per Driver")
    ]
    rows = [row + [f"{change:+.1f}%"] for row, change in zip(rows, changes)]

    figure, axis = plt.subplots(figsize=(10, 4.8), facecolor="#07111f")
    axis.set_facecolor("#07111f")
    axis.axis("off")
    figure.suptitle(
        "Trips rose 2%; reported driver totals stayed flat",
        color="#f3f6fb", fontsize=18, fontweight="bold", y=0.94,
    )
    figure.text(
        0.5, 0.84, "TLC High Volume FHV monthly reports | average of 12 monthly values in each year",
        ha="center", color="#9fb0c6", fontsize=11,
    )
    table = axis.table(
        cellText=rows,
        colLabels=["Measure", "2024 average", "2025 average", "Change"],
        cellLoc="center",
        colLoc="center",
        colWidths=[0.40, 0.20, 0.20, 0.16],
        bbox=[0.02, 0.22, 0.96, 0.52],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#334155")
        cell.set_linewidth(0.8)
        cell.set_facecolor("#132238" if row == 0 else "#0b1728")
        cell.get_text().set_color("#f3f6fb" if row == 0 else "#d5dfed")
        if row == 0:
            cell.get_text().set_fontweight("bold")
    figure.text(
        0.5, 0.08,
        "Reported driver counts are monthly totals, not hourly online supply. Changes compare annual averages.",
        ha="center", color="#9fb0c6", fontsize=10,
    )
    figure.text(0.5, 0.035, "Source: NYC Taxi and Limousine Commission", ha="center", color="#9fb0c6", fontsize=9)
    output = ROOT / "public" / "images" / "growth-hvf-monthly-supply.png"
    figure.savefig(output, dpi=160, facecolor=figure.get_facecolor(), bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    monthly_json = ROOT / "analysis_data" / "growth_sources" / "tlc_hvfhv_monthly_2024_2025.json"
    if sys.argv[1:] == ["--monthly-chart-only"]:
        render_monthly_summary(pd.read_json(monthly_json))
        return

    url = f"{API}?{urllib.parse.urlencode(PARAMS)}"
    request = urllib.request.Request(url, headers={"User-Agent": "Hadi Budhy marketplace analysis"})
    with urllib.request.urlopen(request, timeout=120) as response:
        rows = json.load(response)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    hours = [int(row["hour"]) for row in rows]
    trips = [int(row["trips"]) for row in rows]
    if hours != list(range(24)) or sum(trips) != 4_965_012:
        raise ValueError(f"Unexpected API result: hours={hours}, total={sum(trips)}")
    figure, axis = plt.subplots(figsize=(7, 4.2))
    axis.plot(hours, trips, marker="o", color="#171717", linewidth=2)
    axis.fill_between(hours, trips, color="#e5e7eb")
    axis.set_title("Recorded HVFHV trips were highest at 18:00 in the observed week")
    axis.set_xlabel("Pickup hour")
    axis.set_ylabel("Dispatched trips")
    axis.set_xticks(range(0, 24, 3))
    axis.spines[["top", "right"]].set_visible(False)
    axis.text(0.5, -0.23, "Official NYC Open Data | 1–7 February 2019 | recorded trips are not total demand", ha="center", transform=axis.transAxes, fontsize=8, color="#737373")
    figure.tight_layout()
    CHART.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(CHART, dpi=160, bbox_inches="tight")
    plt.close(figure)
    monthly = pd.read_csv(MONTHLY)
    monthly = monthly[monthly["License Class"].eq("FHV - High Volume")].copy()
    numeric = ["Trips Per Day", "Unique Drivers", "Unique Vehicles", "Vehicles Per Day", "Avg Hours Per Day Per Vehicle", "Avg Hours Per Day Per Driver", "Avg Minutes Per Trip"]
    for column in numeric:
        monthly[column] = pd.to_numeric(monthly[column].astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False), errors="coerce")
    monthly["month"] = pd.to_datetime(monthly["Month/Year"], format="%Y-%m")
    monthly = monthly.sort_values("month")
    monthly_2024_25 = monthly[monthly.month.dt.year.isin([2024, 2025])]
    MONTHLY.parent.mkdir(parents=True, exist_ok=True)
    monthly_2024_25.to_json(monthly_json, orient="records", date_format="iso", indent=2)
    render_monthly_summary(monthly_2024_25)
    monthly_chart = ROOT / "public" / "images" / "growth-hvf-monthly-supply.png"
    print(json.dumps({"rows": sum(trips), "peak_hour": hours[trips.index(max(trips))], "peak_trips": max(trips), "output": str(OUTPUT), "chart": str(CHART), "monthly_rows": len(monthly_2024_25), "monthly_chart": str(monthly_chart)}, indent=2))


if __name__ == "__main__":
    main()
