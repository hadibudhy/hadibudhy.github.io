"""Download the fixed January 2025 NYC 311 snapshot used by the public case."""

from __future__ import annotations

import argparse
import csv
import urllib.parse
import urllib.request
from pathlib import Path


API = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
PARAMS = {
    "$select": "unique_key,created_date,closed_date,agency,complaint_type,borough,status",
    "$where": "created_date between '2025-01-01T00:00:00' and '2025-01-31T23:59:59'",
    "$order": "unique_key",
    "$limit": "500000",
}
EXPECTED_ROWS = 348_180


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("analysis_data/service/nyc311-2025-01.csv"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(f"{API}?{urllib.parse.urlencode(PARAMS)}", headers={"User-Agent": "Hadi Budhy portfolio analytics"})
    with urllib.request.urlopen(request, timeout=300) as response, args.output.open("wb") as target:
        target.write(response.read())
    with args.output.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != EXPECTED_ROWS or len({row["unique_key"] for row in rows}) != EXPECTED_ROWS:
        raise ValueError(f"Unexpected NYC 311 snapshot: rows={len(rows)} unique={len({row['unique_key'] for row in rows})}")
    print(f"downloaded {len(rows):,} unique requests to {args.output}")


if __name__ == "__main__":
    main()
