"""Load the public REES46 export into the local DuckDB raw schema.

The download is intentionally kept outside Git. This script only creates the
raw source relation; dbt owns the typed models and marts.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import duckdb


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
        connection.execute("create schema if not exists raw")
        connection.execute(
            """
            create or replace table raw.events as
            select * from read_csv_auto(?, header = true, compression = 'gzip')
            """,
            [os.fspath(source)],
        )
        row_count = connection.execute("select count(*) from raw.events").fetchone()[0]
        print(f"loaded raw.events: {row_count:,} rows")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
