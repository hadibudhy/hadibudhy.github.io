"""Load the public REES46 export into the local DuckDB raw schema.

The download is intentionally kept outside Git. This script only creates the
raw source relation; dbt owns the typed models and marts.
"""

from __future__ import annotations

import argparse
import csv
import gzip
from datetime import datetime
from pathlib import Path

import duckdb


def load_source(connection: duckdb.DuckDBPyConnection, source: Path) -> int:
    connection.execute("create schema if not exists raw")
    connection.execute("drop table if exists raw.events")
    connection.execute("""
        create table raw.events (
            source_row_number bigint, event_time timestamp, event_type varchar,
            product_id varchar, category_id varchar, category_code varchar,
            brand varchar, price double, user_id varchar, user_session varchar
        )
    """)
    batch: list[tuple] = []
    row_count = 0
    with gzip.open(source, "rt", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        for row_count, row in enumerate(reader, start=1):
            batch.append((
                row_count,
                datetime.fromisoformat(row["event_time"]),
                row["event_type"], row["product_id"], row["category_id"],
                row.get("category_code") or None, row.get("brand") or None,
                float(row["price"]) if row.get("price") else None,
                row["user_id"], row.get("user_session") or None,
            ))
            if len(batch) == 10_000:
                connection.executemany("insert into raw.events values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", batch)
                batch.clear()
    if batch:
        connection.executemany("insert into raw.events values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", batch)
    return row_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--database", type=Path, default=Path("target/ae_product.duckdb"))
    args = parser.parse_args()

    source = args.source.resolve()
    database = args.database.resolve()
    if not source.exists():
        raise SystemExit(f"source file does not exist: {source}")

    database.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(database))
    try:
        row_count = load_source(connection, source)
        print(f"loaded raw.events: {row_count:,} rows")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
