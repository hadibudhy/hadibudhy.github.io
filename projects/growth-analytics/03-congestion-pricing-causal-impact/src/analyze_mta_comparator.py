"""Describe the weekly MTA treated-comparison gap around congestion pricing.

This is a mobility-policy outcome, not a ride-hailing outcome. Treatment is a
facility-level exposure classification. This comparator audit deliberately
reports no causal estimate or pointwise inference.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.chart_theme import ACCENT, BORDER, CANVAS, DPI, HIGHLIGHT, INK, MUTED, WIDE_SIZE, add_header, add_source, style_axis, style_figure


SOURCE = ROOT / "analysis_data/growth_sources/mta_bridge_daily_car_counts.json"
OUTPUT = ROOT / "analysis_data/growth_sources/mta_comparator_audit.json"
CHART = ROOT / "public/images/growth-mta-event-study.png"
PRETREND_CHART = ROOT / "public/images/growth-mta-pretrend-test.png"
TREATED_FACILITIES = {22, 27, 28}  # RFK Manhattan, Queens-Midtown Tunnel, Hugh L. Carey Tunnel


def pretrend_slope(sample: pd.DataFrame, policy_date: pd.Timestamp) -> dict:
    pre = sample[sample["week"] < policy_date].copy().sort_values("week")
    pre["years_since_start"] = (pre["week"] - pre["week"].min()).dt.days / 365.25
    fit = sm.OLS(pre["difference"], sm.add_constant(pre["years_since_start"])).fit(
        cov_type="HAC", cov_kwds={"maxlags": 26}
    )
    interval = fit.conf_int().loc["years_since_start"]
    return {
        "weeks": len(pre),
        "slope_log_points_per_year": float(fit.params["years_since_start"]),
        "ci95_log_points_per_year": [float(interval.iloc[0]), float(interval.iloc[1])],
        "p_value": float(fit.pvalues["years_since_start"]),
        "standard_error": "HAC with 26 weekly lags",
        "interpretation": "Descriptive linear trend in the pre-policy treated-minus-comparison log gap; not a policy-effect estimate or proof of parallel trends",
    }


def describe(frame: pd.DataFrame, policy_date: pd.Timestamp) -> tuple[dict, pd.DataFrame]:
    grouped = frame.groupby(["week", "treated"], as_index=False).agg(log_traffic=("log_traffic", "mean"))
    treated = grouped[grouped["treated"] == 1].set_index("week")["log_traffic"]
    control = grouped[grouped["treated"] == 0].set_index("week")["log_traffic"]
    sample = pd.DataFrame({"difference": treated - control}).dropna().reset_index()
    sample["days_from_policy"] = (sample["week"] - policy_date).dt.days
    sample["event_week"] = sample["days_from_policy"] // 7
    reference = sample.loc[sample["event_week"] == -1, "difference"]
    if len(reference) != 1:
        raise ValueError("MTA panel must contain exactly one reference week")
    window = sample[sample["event_week"].between(-26, 26)].copy()
    window["effect"] = window["difference"] - reference.iloc[0]
    effects = [{"event_week": int(row.event_week), "effect": float(row.effect)} for row in window.itertuples()]
    pre_policy = window[window["event_week"] < -1]["effect"]
    return {"effects": effects, "n_week_facility": len(frame), "weeks": int(sample["week"].nunique()), "pre_policy_effect_range": [float(pre_policy.min()), float(pre_policy.max())], "pretrend_test": pretrend_slope(sample, policy_date)}, sample


def render_chart(result: dict) -> None:
    effects = pd.DataFrame(result["effects"])
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis, grid_axis="y")
    figure.subplots_adjust(left=0.12, right=0.97, top=0.80, bottom=0.15)
    axis.axhline(0, color=BORDER, linewidth=1.2)
    axis.axvline(-0.5, color=HIGHLIGHT, linestyle=(0, (4, 3)), linewidth=1.4)
    axis.plot(effects.event_week, effects.effect, marker="o", color=ACCENT, linewidth=1.8, markersize=4.5)
    axis.text(-0.5, axis.get_ylim()[1], "Policy starts", ha="center", va="top", color=HIGHLIGHT,
              fontsize=9, fontweight="bold")
    axis.set_xlim(-27, 27)
    axis.set_xticks(range(-24, 25, 6))
    axis.set_xlabel("Event week relative to 5 January 2025")
    axis.set_ylabel("Change in affected-minus-comparison log gap vs week -1")
    add_header(figure, "The comparison gap varied before the policy date",
               "Weekly affected-minus-comparison log traffic change, relative to event week -1; ±26-week window")
    add_source(figure, "MTA Bridges and Tunnels, 2019 to May 2026; descriptive audit, no causal estimate or pointwise interval")
    figure.savefig(CHART, dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def render_pretrend_chart(result: dict) -> None:
    test = result["pretrend_test"]
    estimate = test["slope_log_points_per_year"]
    lower, upper = test["ci95_log_points_per_year"]
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis)
    figure.subplots_adjust(left=0.12, right=0.97, top=0.80, bottom=0.17)
    axis.axvline(0, color=BORDER, linewidth=1.4, linestyle="--")
    axis.errorbar(estimate, 0, xerr=[[estimate - lower], [upper - estimate]], fmt="o",
                  color=ACCENT, ecolor=ACCENT, capsize=7, markersize=8, linewidth=2)
    axis.set_xlim(-0.015, 0.045)
    axis.set_ylim(-0.6, 0.6)
    axis.set_yticks([])
    axis.set_xlabel("Pre-policy slope in log points per year (95% HAC interval)")
    axis.annotate(f"{estimate:+.4f}; p={test['p_value']:.3f}", (estimate, 0),
                  xytext=(0, 22), textcoords="offset points", ha="center", color=INK,
                  fontsize=10, fontweight="bold")
    add_header(figure, "The pre-policy slope estimate is inconclusive",
               f"{test['weeks']} weekly gaps; HAC standard errors with 26 lags; interval includes zero")
    add_source(figure, "MTA Bridges and Tunnels; descriptive pre-policy trend check, not a causal test")
    figure.savefig(PRETREND_CHART, dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def main() -> None:
    if sys.argv[1:] == ["--chart-only"]:
        render_chart(json.loads(OUTPUT.read_text(encoding="utf-8")))
        return

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
    result, _ = describe(panel, policy)
    trend = result["pretrend_test"]
    if trend["weeks"] != 314 or not math.isclose(trend["slope_log_points_per_year"], 0.0155100594, abs_tol=1e-9):
        raise ValueError(f"Unexpected pre-policy slope diagnostic: {trend}")
    result.update({"policy_date": policy.strftime("%Y-%m-%d"), "source_period": [raw.date.min().strftime("%Y-%m-%d"), raw.date.max().strftime("%Y-%m-%d")], "treated_facilities": sorted(TREATED_FACILITIES), "control_facilities": sorted(set(raw.facility_id) - TREATED_FACILITIES), "grain": "facility-week", "estimand": "descriptive treated-minus-control change in log(1 + weekly car crossings), relative to event week -1", "limitations": ["Each event week is one treated-control weekly difference, so no pointwise inference is reported", "This is all-car bridge/tunnel traffic, not HVFHV demand", "No route-level toll exposure or rider outcomes", "Spillovers, seasonality, and facility-specific shocks remain possible"]})
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    render_chart(result)
    render_pretrend_chart(result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
