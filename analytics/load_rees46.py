"""Load the public REES46 export into the local DuckDB raw schema.

The download is intentionally kept outside Git. This script only creates the
raw source relation; dbt owns the typed models and marts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb


def load_source(connection: duckdb.DuckDBPyConnection, source: Path) -> int:
    connection.execute("create schema if not exists raw")
    connection.execute("drop table if exists raw.events")
    connection.execute("""
        create table raw.events as
        select
            row_number() over () as source_row_number,
            coalesce(
                try_strptime(event_time, '%Y-%m-%d %H:%M:%S UTC'),
                try_strptime(event_time, '%Y-%m-%d %H:%M:%S')
            ) as event_time,
            event_type,
            product_id,
            category_id,
            nullif(category_code, '') as category_code,
            nullif(brand, '') as brand,
            try_cast(price as double) as price,
            user_id,
            nullif(user_session, '') as user_session
        from read_csv_auto(?, header = true, all_varchar = true)
    """, [str(source)])
    return connection.execute("select count(*) from raw.events").fetchone()[0]


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
