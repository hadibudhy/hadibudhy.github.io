"""Estimate a transparent zone-day event study from a prepared, validated panel.

The input must contain one row per zone-day with recorded_trips, pickup_zone,
service_date, and is_policy_exposed. The script deliberately refuses to infer
policy exposure from pickup zone alone.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


REQUIRED = {"service_date", "pickup_zone", "is_policy_exposed", "recorded_trips"}


def estimate(source: Path, policy_date: str = "2025-01-05") -> dict:
    frame = pd.read_parquet(source) if source.suffix == ".parquet" else pd.read_csv(source)
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    frame["service_date"] = pd.to_datetime(frame["service_date"], errors="raise")
    if frame.duplicated(["service_date", "pickup_zone"]).any():
        raise ValueError("Input must contain one row per zone-day")
    if not bool(frame["is_policy_exposed"].isin([0, 1]).all()):
        raise ValueError("is_policy_exposed must be a binary, precomputed exposure flag")
    frame["days_from_policy"] = (frame["service_date"] - pd.Timestamp(policy_date)).dt.days
    frame["event_week"] = (frame["days_from_policy"] // 7).clip(-8, 8)
    frame["post_policy"] = (frame["days_from_policy"] >= 0).astype(int)
    frame["log_recorded_trips"] = (frame["recorded_trips"].clip(lower=0) + 1).map(__import__("math").log)
    if frame["pickup_zone"].nunique() < 10:
        raise ValueError("At least 10 zone clusters are required before clustered inference")
    model = smf.ols("log_recorded_trips ~ is_policy_exposed * post_policy + C(pickup_zone) + C(service_date)", data=frame).fit(cov_type="cluster", cov_kwds={"groups": frame["pickup_zone"]})
    coefficient = "is_policy_exposed:post_policy"
    return {"policy_date": policy_date, "rows": len(frame), "zones": int(frame["pickup_zone"].nunique()), "estimand": "change in log(1 + recorded trips) for policy-exposed zone-days relative to zone and date effects", "effect": float(model.params.get(coefficient, float("nan"))), "standard_error": float(model.bse.get(coefficient, float("nan"))), "p_value": float(model.pvalues.get(coefficient, float("nan"))), "confidence_interval_95": [float(value) for value in model.conf_int().loc[coefficient].tolist()]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("analysis_data/growth_sources/congestion-event-study.json"))
    args = parser.parse_args()
    result = estimate(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
