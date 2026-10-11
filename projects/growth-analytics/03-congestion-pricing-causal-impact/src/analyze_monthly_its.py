"""Run an aggregate TLC High Volume FHV interrupted-series sensitivity analysis.

This is an aggregate benchmark, not a causal estimate: it has no untreated
market and cannot isolate route-level exposure or spillovers.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.chart_theme import ACCENT, HIGHLIGHT, MUTED, WIDE_SIZE, add_header, add_source, style_axis, style_figure

SOURCE = ROOT / "analysis_data/growth_sources/data_reports_monthly.csv"
OUTPUT = ROOT / "analysis_data/growth_sources/tlc_hvfhv_monthly_its.json"
CHART = ROOT / "public/images/growth-hvf-monthly-its.png"


def main() -> None:
    frame = pd.read_csv(SOURCE)
    frame = frame[frame["License Class"].eq("FHV - High Volume")].copy()
    numeric = ["Trips Per Day", "Unique Drivers", "Unique Vehicles", "Vehicles Per Day", "Avg Hours Per Day Per Vehicle", "Avg Hours Per Day Per Driver", "Avg Minutes Per Trip"]
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column].astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False), errors="coerce")
    frame["month"] = pd.to_datetime(frame["Month/Year"], format="%Y-%m")
    frame = frame.sort_values("month").reset_index(drop=True)
    if frame[numeric].isna().any().any() or frame["month"].duplicated().any():
        raise ValueError("Monthly source has missing metrics or duplicate months")
    assert len(frame) == 137
    assert frame["month"].min() == pd.Timestamp("2015-01-01")
    assert frame["month"].max() == pd.Timestamp("2026-05-01")
    frame["time_index"] = range(len(frame))
    frame["post_policy"] = (frame["month"] >= pd.Timestamp("2025-01-01")).astype(int)
    first_post = frame.loc[frame["post_policy"].eq(1), "time_index"].min()
    frame["post_trend"] = frame["post_policy"] * (frame["time_index"] - first_post + 1).clip(lower=0)
    frame["log_trips"] = (frame["Trips Per Day"] + 1).map(math.log)
    model = smf.ols("log_trips ~ time_index + post_policy + post_trend + C(month.dt.month)", data=frame).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
    result = {"rows": len(frame), "period": [frame.month.min().strftime("%Y-%m"), frame.month.max().strftime("%Y-%m")], "estimand": "aggregate level/trend change in log(1 + reported HVFHV trips per day), not a causal policy effect", "post_level_effect": float(model.params.get("post_policy", float("nan"))), "post_level_p_value": float(model.pvalues.get("post_policy", float("nan"))), "post_trend_effect": float(model.params.get("post_trend", float("nan"))), "post_trend_p_value": float(model.pvalues.get("post_trend", float("nan"))), "covariance": "HAC maxlags=6", "limitations": ["No untreated market", "No route-level toll exposure", "Aggregate monthly outcome", "COVID and other shocks require sensitivity checks"]}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    figure, axis = plt.subplots(figsize=WIDE_SIZE)
    style_figure(figure)
    figure.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.16)
    style_axis(axis)
    axis.plot(frame.month, frame["Trips Per Day"], color=ACCENT, linewidth=2.1)
    policy_date = pd.Timestamp("2025-01-01")
    axis.axvline(policy_date, color=HIGHLIGHT, linestyle="--", linewidth=1.3)
    axis.annotate("Policy start", (policy_date, axis.get_ylim()[1]), xytext=(5, -16),
                  textcoords="offset points", color=HIGHLIGHT, fontsize=9, va="top")
    axis.set_ylabel("Reported trips per day")
    axis.set_xlabel("Month")
    add_header(figure, "Reported HVFHV activity needs a longer counterfactual",
               "Aggregate monthly series, January 2015 to May 2026; descriptive only, with no untreated comparison")
    add_source(figure, "NYC TLC monthly reports; High Volume For-Hire Vehicle category")
    figure.savefig(CHART, dpi=160, facecolor=figure.get_facecolor())
    plt.close(figure)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
