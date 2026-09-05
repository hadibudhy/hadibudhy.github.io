"""Load a fixed NYC 311 CSV snapshot into DuckDB at request grain."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import duckdb


EXPECTED_COLUMNS = ["request_id", "created_at", "closed_at", "status", "agency", "complaint_type", "borough"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--database", type=Path, default=Path("target/ae_product.duckdb"))
    args = parser.parse_args()
    with args.source.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != EXPECTED_COLUMNS:
            raise SystemExit(f"expected columns {EXPECTED_COLUMNS}, found {reader.fieldnames}")
        rows = [tuple(row[column] for column in EXPECTED_COLUMNS) for row in reader]
    database = args.database.resolve()
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(database))
    try:
        connection.execute("create schema if not exists raw")
        connection.execute("drop table if exists raw.requests")
        connection.execute("""
            create table raw.requests (
                request_id varchar, created_at timestamp, closed_at timestamp,
                status varchar, agency varchar, complaint_type varchar, borough varchar
            )
        """)
        connection.executemany("insert into raw.requests values (?, ?, ?, ?, ?, ?, ?)", rows)
        print(f"loaded raw.requests: {len(rows):,} rows")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
