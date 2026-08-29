"""Run an aggregate TLC High Volume FHV interrupted-series sensitivity analysis.

This is an aggregate benchmark, not a causal estimate: it has no untreated
market and cannot isolate route-level exposure or spillovers.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[4]
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
    frame["time_index"] = range(len(frame))
    frame["post_policy"] = (frame["month"] >= pd.Timestamp("2025-01-01")).astype(int)
    first_post = frame.loc[frame["post_policy"].eq(1), "time_index"].min()
    frame["post_trend"] = frame["post_policy"] * (frame["time_index"] - first_post + 1).clip(lower=0)
    frame["log_trips"] = (frame["Trips Per Day"] + 1).map(math.log)
    model = smf.ols("log_trips ~ time_index + post_policy + post_trend + C(month.dt.month)", data=frame).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
    result = {"rows": len(frame), "period": [frame.month.min().strftime("%Y-%m"), frame.month.max().strftime("%Y-%m")], "estimand": "aggregate level/trend change in log(1 + reported HVFHV trips per day), not a causal policy effect", "post_level_effect": float(model.params.get("post_policy", float("nan"))), "post_level_p_value": float(model.pvalues.get("post_policy", float("nan"))), "post_trend_effect": float(model.params.get("post_trend", float("nan"))), "post_trend_p_value": float(model.pvalues.get("post_trend", float("nan"))), "covariance": "HAC maxlags=6", "limitations": ["No untreated market", "No route-level toll exposure", "Aggregate monthly outcome", "COVID and other shocks require sensitivity checks"]}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    figure, axis = plt.subplots(figsize=(7, 4.2))
    axis.plot(frame.month, frame["Trips Per Day"], color="#171717", linewidth=2)
    axis.axvline(pd.Timestamp("2025-01-01"), color="#737373", linestyle="--", linewidth=1)
    axis.set_title("Reported HVFHV activity around the policy date needs a longer counterfactual")
    axis.set_ylabel("Reported trips per day")
    axis.set_xlabel("Month")
    axis.spines[["top", "right"]].set_visible(False)
    axis.text(0.5, -0.24, "TLC monthly report | Jan 2010–May 2026 | aggregate interrupted series, not causal evidence", ha="center", transform=axis.transAxes, fontsize=8, color="#737373")
    figure.tight_layout()
    figure.savefig(CHART, dpi=160, bbox_inches="tight")
    plt.close(figure)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
