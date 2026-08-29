"""Fetch the bounded official HVFHV Open Data slice and regenerate its chart."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[4]
OUTPUT = ROOT / "analysis_data" / "growth_sources" / "hvf_hourly_2019.json"
CHART = ROOT / "public" / "images" / "growth-hvf-hourly.png"
API = "https://data.cityofnewyork.us/resource/4p5c-cbgn.json"
PARAMS = {
    "$select": "date_extract_hh(pickup_datetime) as hour,count(*) as trips",
    "$where": "pickup_datetime between '2019-02-01T00:00:00' and '2019-02-08T00:00:00'",
    "$group": "hour",
    "$order": "hour",
    "$limit": "100",
}


def main() -> None:
    url = f"{API}?{urllib.parse.urlencode(PARAMS)}"
    request = urllib.request.Request(url, headers={"User-Agent": "Hadi Budhy marketplace analysis"})
    with urllib.request.urlopen(request, timeout=120) as response:
        rows = json.load(response)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    hours = [int(row["hour"]) for row in rows]
    trips = [int(row["trips"]) for row in rows]
    figure, axis = plt.subplots(figsize=(7, 4.2))
    axis.plot(hours, trips, marker="o", color="#171717", linewidth=2)
    axis.fill_between(hours, trips, color="#e5e7eb")
    axis.set_title("Completed HVFHV trips were highest at 18:00 in the observed week")
    axis.set_xlabel("Pickup hour")
    axis.set_ylabel("Dispatched trips")
    axis.set_xticks(range(0, 24, 3))
    axis.spines[["top", "right"]].set_visible(False)
    axis.text(0.5, -0.23, "Official NYC Open Data | 1–7 February 2019 | recorded trips are not total demand", ha="center", transform=axis.transAxes, fontsize=8, color="#737373")
    figure.tight_layout()
    CHART.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(CHART, dpi=160, bbox_inches="tight")
    plt.close(figure)
    print(json.dumps({"rows": sum(trips), "peak_hour": hours[trips.index(max(trips))], "peak_trips": max(trips), "output": str(OUTPUT), "chart": str(CHART)}, indent=2))


if __name__ == "__main__":
    main()
