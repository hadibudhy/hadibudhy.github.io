"""Estimate a weekly MTA crossings event study around congestion pricing.

This is a mobility-policy outcome, not a ride-hailing outcome. Treatment is a
facility-level exposure classification, so interpretation is limited to the
selected crossings and their observed car traffic.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "analysis_data/growth_sources/mta_bridge_daily_car_counts.json"
OUTPUT = ROOT / "analysis_data/growth_sources/mta_bridge_event_study.json"
CHART = ROOT / "public/images/growth-mta-event-study.png"
TREATED_FACILITIES = {22, 27, 28}  # RFK Manhattan, Queens-Midtown Tunnel, Hugh L. Carey Tunnel


def fit(frame: pd.DataFrame, policy_date: pd.Timestamp) -> tuple[dict, pd.DataFrame]:
    grouped = frame.groupby(["week", "treated"], as_index=False).agg(log_traffic=("log_traffic", "mean"))
    treated = grouped[grouped["treated"] == 1].set_index("week")["log_traffic"]
    control = grouped[grouped["treated"] == 0].set_index("week")["log_traffic"]
    sample = pd.DataFrame({"difference": treated - control}).dropna().reset_index()
    sample["days_from_policy"] = (sample["week"] - policy_date).dt.days
    sample["event_week"] = (sample["days_from_policy"] // 7).clip(-26, 26)
    sample["time_index"] = range(len(sample))
    model = smf.ols("difference ~ time_index + C(event_week, Treatment(reference=-1))", data=sample).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    effects = []
    for name in model.params.index:
        if "C(event_week" in name:
            event_week = int(name.split("T.", 1)[1].split("]", 1)[0])
            interval = model.conf_int().loc[name]
            effects.append({"event_week": event_week, "effect": float(model.params[name]), "p_value": float(model.pvalues[name]), "ci95": [float(interval[0]), float(interval[1])]})
    return {"effects": sorted(effects, key=lambda row: row["event_week"]), "n_week_facility": len(frame), "weeks": int(sample["week"].nunique())}, sample


def main() -> None:
    raw = pd.read_json(SOURCE)
    raw["date"] = pd.to_datetime(raw["date"])
    raw["traffic_count"] = pd.to_numeric(raw["traffic_count"], errors="raise")
    raw["facility_id"] = raw["facility_id"].astype(int)
    if raw.duplicated(["date", "facility_id"]).any() or raw.facility_id.nunique() != 10:
        raise ValueError("MTA input must contain one car-count row per facility-day for ten facilities")
    raw["treated"] = raw["facility_id"].isin(TREATED_FACILITIES).astype(int)
    raw["week"] = raw["date"] - pd.to_timedelta((raw["date"].dt.dayofweek + 1) % 7, unit="D")
    panel = raw.groupby(["week", "facility_id", "facility", "treated"], as_index=False).agg(traffic_count=("traffic_count", "sum"))
    panel["log_traffic"] = (panel["traffic_count"] + 1).map(math.log)
    policy = pd.Timestamp("2025-01-05")
    result, fitted = fit(panel, policy)
    placebo_results = []
    for days in [14, 28, 56]:
        placebo, _ = fit(panel, policy - pd.Timedelta(days=days))
        placebo_results.append({"placebo_date": (policy - pd.Timedelta(days=days)).strftime("%Y-%m-%d"), "effects": placebo["effects"]})
    result.update({"policy_date": policy.strftime("%Y-%m-%d"), "source_period": [raw.date.min().strftime("%Y-%m-%d"), raw.date.max().strftime("%Y-%m-%d")], "treated_facilities": sorted(TREATED_FACILITIES), "control_facilities": sorted(set(raw.facility_id) - TREATED_FACILITIES), "grain": "facility-week", "estimand": "treated-minus-control change in log(1 + weekly car crossings), relative to event week -1", "placebo_tests": placebo_results, "limitations": ["Ten facility clusters make clustered uncertainty fragile", "This is all-car bridge/tunnel traffic, not HVFHV demand", "No route-level toll exposure or rider outcomes", "Spillovers and facility-specific shocks remain possible"]})
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    effects = pd.DataFrame(result["effects"])
    figure, axis = plt.subplots(figsize=(7, 4.2))
    axis.axhline(0, color="#a3a3a3", linewidth=1)
    axis.axvline(-0.5, color="#737373", linestyle="--", linewidth=1)
    axis.errorbar(effects.event_week, effects.effect, yerr=[effects.effect - effects.ci95.map(lambda value: value[0]), effects.ci95.map(lambda value: value[1]) - effects.effect], fmt="o", color="#171717", capsize=4)
    axis.set_title("CBD-access crossing traffic changed relative to control facilities")
    axis.set_xlabel("Weeks from 5 January 2025; reference week = -1")
    axis.set_ylabel("Treated minus control log weekly car crossings")
    axis.spines[["top", "right"]].set_visible(False)
    axis.text(0.5, -0.24, "MTA Bridges & Tunnels | 2019–May 2026 | 95% HAC CIs on weekly treated-control differences; not HVFHV demand", ha="center", transform=axis.transAxes, fontsize=8, color="#737373")
    figure.tight_layout()
    figure.savefig(CHART, dpi=160, bbox_inches="tight")
    plt.close(figure)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
