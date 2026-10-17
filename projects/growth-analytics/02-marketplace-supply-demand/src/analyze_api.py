"""Fetch the bounded official HVFHV Open Data slice and regenerate its chart."""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.chart_theme import ACCENT, BORDER, CANVAS, DPI, HIGHLIGHT, INK, MUTED, WIDE_SIZE, add_header, add_source, style_axis, style_figure


OUTPUT = ROOT / "analysis_data" / "growth_sources" / "hvf_hourly_2019.json"
WEEKDAY_OUTPUT = ROOT / "analysis_data" / "growth_sources" / "hvf_weekday_2019.json"
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
WEEKDAY_PARAMS = {
    "$select": "date_extract_dow(pickup_datetime) as weekday,count(*) as trips",
    "$where": "pickup_datetime >= '2019-02-01T00:00:00' and pickup_datetime < '2019-02-08T00:00:00'",
    "$group": "weekday",
    "$order": "weekday",
    "$limit": "20",
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

    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    axis.axis("off")
    add_header(figure, "Trips rose 2%; reported driver totals were almost unchanged",
               "Annual average of 12 monthly TLC High Volume FHV values, 2024 vs 2025")
    table = axis.table(
        cellText=rows,
        colLabels=["Measure", "2024 average", "2025 average", "Change"],
        cellLoc="center",
        colLoc="center",
        colWidths=[0.40, 0.20, 0.20, 0.16],
        bbox=[0.02, 0.20, 0.96, 0.54],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor(BORDER)
        cell.set_linewidth(0.6)
        cell.set_facecolor("#EAF0F2" if row == 0 else CANVAS)
        cell.get_text().set_color(INK if row == 0 else MUTED)
        cell.get_text().set_fontfamily("Arial")
        if row == 0:
            cell.get_text().set_fontweight("bold")
    figure.text(0.065, 0.105,
                "Driver counts are monthly totals, not hourly online supply. Changes compare unrounded annual means.",
                ha="left", color=MUTED, fontsize=9, fontfamily="Arial")
    add_source(figure, "NYC Taxi and Limousine Commission")
    output = ROOT / "public" / "images" / "growth-hvf-monthly-supply.png"
    figure.savefig(output, dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def render_monthly_matched_change(monthly: pd.DataFrame) -> dict:
    frame = monthly.copy()
    frame["year"] = pd.to_datetime(frame["month"]).dt.year
    frame["month_number"] = pd.to_datetime(frame["month"]).dt.month
    changes = {}
    for metric in ("Trips Per Day", "Unique Drivers"):
        pivot = frame.pivot(index="month_number", columns="year", values=metric)
        if list(pivot.columns) != [2024, 2025] or len(pivot) != 12 or pivot.isna().any().any():
            raise ValueError(f"Expected 12 complete matched months for {metric}")
        changes[metric] = (pivot[2025] / pivot[2024] - 1) * 100
    jan_jun = slice(1, 6)
    jul_dec = slice(7, 12)
    summary = {
        metric: {
            "mean_paired_change_pct": float(values.mean()),
            "jan_jun_mean_change_pct": float(values.loc[jan_jun].mean()),
            "jul_dec_mean_change_pct": float(values.loc[jul_dec].mean()),
        }
        for metric, values in changes.items()
    }
    assert round(summary["Trips Per Day"]["jan_jun_mean_change_pct"], 1) == 0.7
    assert round(summary["Trips Per Day"]["jul_dec_mean_change_pct"], 1) == 3.3
    assert round(summary["Unique Drivers"]["jan_jun_mean_change_pct"], 1) == -4.2
    assert round(summary["Unique Drivers"]["jul_dec_mean_change_pct"], 1) == 4.0

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis)
    figure.subplots_adjust(left=0.10, right=0.97, top=0.80, bottom=0.16)
    axis.axhline(0, color=BORDER, linewidth=1.2)
    axis.axvline(5.5, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    axis.plot(months, changes["Trips Per Day"].values, color=ACCENT, marker="o", linewidth=2.2,
              label="Trips per day")
    axis.plot(months, changes["Unique Drivers"].values, color=HIGHLIGHT, marker="o", linewidth=2.2,
              label="Unique drivers")
    axis.set_ylabel("Change from same month in 2024 (%)")
    axis.set_ylim(-7, 9)
    axis.legend(frameon=False, ncols=2, loc="upper left", labelcolor=INK, fontsize=9)
    add_header(figure, "Flat annual driver averages hide a first-half decline and late-year recovery",
               "Monthly 2025 values versus the same month in 2024; 12 matched pairs, not hourly online supply")
    add_source(figure, "NYC Taxi and Limousine Commission monthly High Volume FHV reports")
    output = ROOT / "public" / "images" / "growth-hvf-monthly-matched.png"
    figure.savefig(output, dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)
    return summary


def render_hourly_chart(rows: list[dict]) -> None:
    hours = [int(row["hour"]) for row in rows]
    trips = [int(row["trips"]) for row in rows]
    if hours != list(range(24)) or sum(trips) != 4_965_012:
        raise ValueError(f"Unexpected hourly source: hours={hours}, total={sum(trips)}")
    peak_index = trips.index(max(trips))
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis)
    figure.subplots_adjust(left=0.09, right=0.97, top=0.80, bottom=0.15)
    axis.plot(hours, trips, marker="o", color=ACCENT, linewidth=2.2, markersize=4.5)
    axis.fill_between(hours, trips, color=ACCENT, alpha=0.08)
    axis.scatter([hours[peak_index]], [trips[peak_index]], color=HIGHLIGHT, s=46, zorder=3)
    axis.annotate(f"18:00  {trips[peak_index]:,}", (hours[peak_index], trips[peak_index]),
                  xytext=(-8, -24), textcoords="offset points", ha="right", color=INK,
                  fontsize=10, fontweight="bold")
    add_header(figure, "Recorded HVFHV trips peaked at 18:00",
               "Pickup hour, 1 to 7 February 2019; dispatched trip records are not total demand")
    axis.set_xlabel("Pickup hour")
    axis.set_ylabel("Recorded trips")
    axis.set_xticks(range(0, 24, 2))
    axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:.0f}k"))
    add_source(figure, "NYC TLC High Volume FHV Open Data, bounded Open Data API query")
    figure.savefig(CHART, dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def render_weekday_chart(rows: list[dict]) -> None:
    weekdays = [int(row["weekday"]) for row in rows]
    trips = [int(row["trips"]) for row in rows]
    if weekdays != list(range(7)) or sum(trips) != 4_965_012:
        raise ValueError(f"Unexpected weekday source: weekdays={weekdays}, total={sum(trips)}")
    labels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    colors = [HIGHLIGHT if day in (5, 6) else ACCENT for day in weekdays]
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis, grid_axis="y")
    figure.subplots_adjust(left=0.09, right=0.97, top=0.80, bottom=0.17)
    bars = axis.bar(labels, trips, color=colors, width=0.66)
    for bar, count in zip(bars, trips):
        axis.text(bar.get_x() + bar.get_width() / 2, count + 12_000, f"{count:,}",
                  ha="center", color=INK, fontsize=8.5)
    axis.set_ylim(0, max(trips) * 1.16)
    axis.set_ylabel("Recorded trips")
    axis.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:.0f}k"))
    axis.tick_params(axis="x", labelrotation=20)
    add_header(figure, "Saturday and Friday had the most recorded trips in this week",
               "Pickup day, 1–7 February 2019; Friday and Saturday are highlighted, and trips do not show unmet demand")
    add_source(figure, "NYC TLC High Volume FHV Open Data, bounded API query")
    figure.savefig(ROOT / "public" / "images" / "growth-hvf-weekday.png", dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def download_weekday_summary() -> None:
    url = f"{API}?{urllib.parse.urlencode(WEEKDAY_PARAMS)}"
    request = urllib.request.Request(url, headers={"User-Agent": "Hadi Budhy marketplace analysis"})
    with urllib.request.urlopen(request, timeout=120) as response:
        rows = json.load(response)
    WEEKDAY_OUTPUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    render_weekday_chart(rows)


def main() -> None:
    monthly_json = ROOT / "analysis_data" / "growth_sources" / "tlc_hvfhv_monthly_2024_2025.json"
    if sys.argv[1:] == ["--weekday"]:
        download_weekday_summary()
        return
    if sys.argv[1:] == ["--hourly-chart-only"]:
        render_hourly_chart(json.loads(OUTPUT.read_text(encoding="utf-8")))
        return
    if sys.argv[1:] == ["--monthly-chart-only"]:
        monthly = pd.read_json(monthly_json)
        render_monthly_summary(monthly)
        print(json.dumps(render_monthly_matched_change(monthly), indent=2))
        return

    url = f"{API}?{urllib.parse.urlencode(PARAMS)}"
    request = urllib.request.Request(url, headers={"User-Agent": "Hadi Budhy marketplace analysis"})
    with urllib.request.urlopen(request, timeout=120) as response:
        rows = json.load(response)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    render_hourly_chart(rows)
    CHART.parent.mkdir(parents=True, exist_ok=True)
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
    matched_change = render_monthly_matched_change(monthly_2024_25)
    monthly_chart = ROOT / "public" / "images" / "growth-hvf-monthly-supply.png"
    print(json.dumps({"rows": sum(trips), "peak_hour": hours[trips.index(max(trips))], "peak_trips": max(trips), "output": str(OUTPUT), "chart": str(CHART), "monthly_rows": len(monthly_2024_25), "monthly_chart": str(monthly_chart), "matched_month_change": matched_change}, indent=2))


if __name__ == "__main__":
    main()
