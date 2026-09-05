from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

URL = "https://data.rees46.com/datasets/electronics-events/electronics-events.csv.gz"


def download_and_profile(output: Path) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    if not output.exists():
        request = urllib.request.Request(URL, headers={"User-Agent": "Hadi Budhy portfolio analytics"})
        with urllib.request.urlopen(request, timeout=120) as response, output.open("wb") as target:
            target.write(response.read())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    counts = Counter()
    missing = Counter()
    rows = 0
    first = None
    last = None
    with gzip.open(output, "rt", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames or []
        for row in reader:
            rows += 1
            counts[row["event_type"]] += 1
            for column in columns:
                if not row.get(column):
                    missing[column] += 1
            timestamp = row["event_time"]
            first = timestamp if first is None or timestamp < first else first
            last = timestamp if last is None or timestamp > last else last
    profile = {
        "source": URL,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "path": str(output),
        "sha256": digest,
        "rows": rows,
        "columns": columns,
        "event_counts": dict(counts),
        "missing": dict(missing),
        "first_event_time": first,
        "last_event_time": last,
        "grain": "one observed event row",
    }
    output.with_suffix(".profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")
    return profile


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("analysis_data/product-events/electronics-events.csv.gz"))
    args = parser.parse_args()
    print(json.dumps(download_and_profile(args.output), indent=2))
