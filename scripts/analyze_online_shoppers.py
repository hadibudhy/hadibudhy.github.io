"""Reproduce the Online Shoppers portfolio result from the UCI CSV."""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


EXPECTED_SHA256 = "b3055ee355f59134d851d32641183cb4a8b45def7124d2f50442a042f358e0d9"
EXPECTED_HEADERS = [
    "Administrative", "Administrative_Duration", "Informational", "Informational_Duration",
    "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues",
    "SpecialDay", "Month", "OperatingSystems", "Browser", "Region", "TrafficType",
    "VisitorType", "Weekend", "Revenue",
]


def conversion_by_visitor(records):
    grouped = defaultdict(Counter)
    for row in records:
        grouped[row["VisitorType"]]["sessions"] += 1
        grouped[row["VisitorType"]]["conversions"] += row["Revenue"] == "TRUE"
    return grouped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Path to online_shoppers_intention.csv")
    parser.add_argument("--output", help="Optional path for the verified metrics JSON")
    args = parser.parse_args()

    source_path = Path(args.csv_path)
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if source_hash != EXPECTED_SHA256:
        raise SystemExit(f"Unexpected source SHA-256: {source_hash}")

    with source_path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != EXPECTED_HEADERS:
            raise SystemExit(f"Unexpected headers: {reader.fieldnames}")
        rows = list(reader)

    if any(value == "" for row in rows for value in row.values()):
        raise SystemExit("Missing cell found")
    if {row["Revenue"] for row in rows} != {"TRUE", "FALSE"}:
        raise SystemExit("Revenue must contain exactly TRUE and FALSE")
    if {row["VisitorType"] for row in rows} != {"New_Visitor", "Other", "Returning_Visitor"}:
        raise SystemExit("Unexpected VisitorType category")

    unique_rows = list(dict.fromkeys(tuple(row.items()) for row in rows))
    records = [dict(row) for row in unique_rows]
    raw_by_visitor = conversion_by_visitor(rows)
    by_visitor = conversion_by_visitor(records)
    by_month = defaultdict(Counter)
    page_values = defaultdict(list)

    for row in records:
        converted = row["Revenue"] == "TRUE"
        by_month[row["Month"]]["sessions"] += 1
        by_month[row["Month"]]["conversions"] += converted
        page_values[converted].append(float(row["PageValues"]))

    print(f"raw_sessions={len(rows):,}")
    print(f"exact_duplicates={len(rows) - len(records):,}")
    print(f"deduplicated_sessions={len(records):,}")
    for visitor, counts in sorted(by_visitor.items()):
        rate = counts["conversions"] / counts["sessions"]
        print(f"{visitor}: n={counts['sessions']:,}, conversions={counts['conversions']:,}, rate={rate:.1%}")
    for converted in (False, True):
        values = page_values[converted]
        print(f"Revenue={converted}: n={len(values):,}, mean_page_values={sum(values) / len(values):.1f}")

    metrics = {
        "source": {
            "name": "UCI Online Shoppers Purchasing Intention Dataset",
            "url": "https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset",
            "retrieved": "2026-08-30",
            "license": "CC BY 4.0",
            "sha256": source_hash,
        },
        "period": "Ten months of 2018",
        "grain": "one session",
        "raw_sessions": len(rows),
        "exact_duplicates": len(rows) - len(records),
        "deduplicated_sessions": len(records),
        "visitor_conversion": {
            visitor: {
                "sessions": counts["sessions"],
                "conversions": counts["conversions"],
                "rate": counts["conversions"] / counts["sessions"],
            }
            for visitor, counts in sorted(by_visitor.items())
        },
        "raw_visitor_conversion": {
            visitor: {
                "sessions": counts["sessions"],
                "conversions": counts["conversions"],
                "rate": counts["conversions"] / counts["sessions"],
            }
            for visitor, counts in sorted(raw_by_visitor.items())
        },
        "month_conversion": {
            month: {
                "sessions": counts["sessions"],
                "conversions": counts["conversions"],
                "rate": counts["conversions"] / counts["sessions"],
            }
            for month, counts in sorted(by_month.items())
        },
        "mean_page_values": {
            str(converted).lower(): sum(values) / len(values)
            for converted, values in page_values.items()
        },
    }
    assert len(rows) == 12_330
    assert len(records) == 12_205
    assert by_visitor["New_Visitor"] == Counter(sessions=1_693, conversions=422)
    assert by_visitor["Returning_Visitor"] == Counter(sessions=10_431, conversions=1_470)
    assert raw_by_visitor["New_Visitor"] == Counter(sessions=1_694, conversions=422)
    assert raw_by_visitor["Returning_Visitor"] == Counter(sessions=10_551, conversions=1_470)

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
