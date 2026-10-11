"""Stream the Criteo unbiased release and calculate the primary ITT estimate."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.chart_theme import ACCENT, CANVAS, DPI, HIGHLIGHT, INK, WIDE_SIZE, add_header, add_source, style_axis, style_figure


def proportions(a_success: int, a_total: int, b_success: int, b_total: int) -> dict:
    a = a_success / a_total
    b = b_success / b_total
    difference = a - b
    standard_error = math.sqrt(a * (1 - a) / a_total + b * (1 - b) / b_total)
    z = difference / standard_error
    p_value = math.erfc(abs(z) / math.sqrt(2))
    return {"treatment_rate": a, "control_rate": b, "absolute_difference": difference, "relative_difference": a / b - 1, "ci95": [difference - 1.96 * standard_error, difference + 1.96 * standard_error], "p_value": p_value}


def analyze(source: Path, chunksize: int = 500_000) -> dict:
    fields = ["treatment", "conversion", "visit", "exposure"]
    required_features = {f"f{index}" for index in range(12)}
    header = set(pd.read_csv(source, nrows=0).columns)
    missing_features = required_features - header
    if missing_features:
        raise ValueError(f"Missing required anonymized features: {sorted(missing_features)}")
    counts = {(assignment, exposure): {"n": 0, "conversion": 0, "visit": 0} for assignment in [0, 1] for exposure in [0, 1]}
    rows = 0
    null_counts = {field: 0 for field in fields}
    invalid_counts = {field: 0 for field in fields}
    for chunk in pd.read_csv(source, usecols=fields, chunksize=chunksize):
        rows += len(chunk)
        for field in fields:
            null_counts[field] += int(chunk[field].isna().sum())
            if field != "exposure":
                invalid_counts[field] += int((~chunk[field].isin([0, 1])).sum())
        invalid_counts["exposure"] += int((~chunk["exposure"].isin([0, 1])).sum())
        for (assignment, exposure), group in chunk.groupby(fields[:1] + fields[3:]):
            key = (int(assignment), int(exposure))
            counts[key]["n"] += len(group)
            counts[key]["conversion"] += int(group["conversion"].sum())
            counts[key]["visit"] += int(group["visit"].sum())
    control = counts[(0, 0)]
    treated = {key: sum(counts[(1, exposure)][key] for exposure in [0, 1]) for key in ["n", "conversion", "visit"]}
    if any(null_counts.values()) or any(invalid_counts.values()):
        raise ValueError(f"Invalid source values: nulls={null_counts}, invalid={invalid_counts}")
    if counts[(0, 1)]["n"]:
        raise ValueError("Control rows with exposure=1 would invalidate the treatment interpretation")
    expected_ratio = 0.85
    treatment_ratio = treated["n"] / rows
    srm_se = math.sqrt(expected_ratio * (1 - expected_ratio) / rows)
    srm_z = (treatment_ratio - expected_ratio) / srm_se
    result = {"rows": rows, "treatment_ratio": treatment_ratio, "srm_check": {"expected_ratio": expected_ratio, "observed_ratio": treatment_ratio, "z": srm_z, "p_value": math.erfc(abs(srm_z) / math.sqrt(2))}, "data_quality": {"nulls": null_counts, "invalid_values": invalid_counts}, "counts": {f"assignment_{a}_exposure_{e}": value for (a, e), value in counts.items()}, "conversion_itt": proportions(treated["conversion"], treated["n"], control["conversion"], control["n"]), "visit_itt": proportions(treated["visit"], treated["n"], control["visit"], control["n"])}
    result["f0_quartile_conversion"] = segment_analysis(source, chunksize)
    return result


def segment_analysis(source: Path, chunksize: int) -> list[dict]:
    feature = pd.read_csv(source, usecols=["f0"])["f0"]
    edges = feature.quantile([0, 0.25, 0.5, 0.75, 1]).to_list()
    edges[0], edges[-1] = -float("inf"), float("inf")
    counts = {index: {"n": 0, "success": 0} for index in range(8)}
    for chunk in pd.read_csv(source, usecols=["f0", "treatment", "conversion"], chunksize=chunksize):
        band = pd.cut(chunk["f0"], bins=edges, labels=False, include_lowest=True, duplicates="drop")
        for assignment in [0, 1]:
            group = chunk[chunk["treatment"] == assignment].copy()
            labels = band.loc[group.index]
            for label in sorted(labels.dropna().unique()):
                key = int(label) * 2 + assignment
                counts[key]["n"] += int((labels == label).sum())
                counts[key]["success"] += int(group.loc[labels == label, "conversion"].sum())
    output = []
    for band in range(4):
        control = counts[band * 2]
        treated = counts[band * 2 + 1]
        effect = proportions(treated["success"], treated["n"], control["success"], control["n"])
        output.append({"band": band + 1, "feature": "f0", "control_n": control["n"], "treatment_n": treated["n"], **effect})
    return output


def save_chart(result: dict, destination: Path) -> None:
    metric = result["conversion_itt"]
    value = metric["absolute_difference"] * 100
    low = metric["ci95"][0] * 100
    high = metric["ci95"][1] * 100
    figure, axis = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
    style_figure(figure)
    style_axis(axis, grid_axis="x")
    figure.subplots_adjust(left=0.10, right=0.96, top=0.80, bottom=0.16)
    axis.errorbar([value], [0], xerr=[[value - low], [high - value]], fmt="o", color=ACCENT,
                  ecolor=ACCENT, capsize=5, markersize=7, linewidth=2)
    axis.axvline(0, color=HIGHLIGHT, linewidth=1.2, linestyle=(0, (3, 3)))
    axis.set_xlim(-0.2, 0.2)
    axis.set_ylim(-0.65, 0.65)
    axis.set_yticks([])
    axis.set_xlabel("Difference in conversion rate (percentage points)")
    axis.annotate(f"+{value:.3f} pp", (value, 0), xytext=(0, 22), textcoords="offset points",
                  ha="center", color=INK, fontsize=11, fontweight="bold")
    add_header(figure, "Ad assignment increased conversion by 0.115 percentage points",
               f"Criteo randomized benchmark, 13.98M user records; 95% CI +{low:.3f} to +{high:.3f} pp")
    add_source(figure, "Criteo AI Lab uplift dataset; intention-to-treat estimate, benchmark only")
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=DPI, facecolor=figure.get_facecolor())
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, nargs="?", default=Path("analysis_data/growth_sources/criteo-uplift-v2.1.csv.gz"))
    parser.add_argument("--output", type=Path, default=Path("analysis_data/growth_sources/criteo-itt-results.json"))
    parser.add_argument("--chart-only", action="store_true", help="Regenerate the chart from the checked result JSON without rereading the source data")
    args = parser.parse_args()
    if args.chart_only:
        result = json.loads(args.output.read_text(encoding="utf-8"))
        save_chart(result, Path("public/images/growth-criteo-itt.png"))
        return
    result = analyze(args.source)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    save_chart(result, Path("public/images/growth-criteo-itt.png"))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
