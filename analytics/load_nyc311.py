"""Load a fixed NYC 311 CSV snapshot into DuckDB at request grain."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import duckdb


TARGET_COLUMNS = ["request_id", "created_at", "closed_at", "status", "agency", "complaint_type", "borough"]
SOURCE_ALIASES = {
    "request_id": ("request_id", "unique_key"),
    "created_at": ("created_at", "created_date"),
    "closed_at": ("closed_at", "closed_date"),
    "status": ("status",),
    "agency": ("agency",),
    "complaint_type": ("complaint_type",),
    "borough": ("borough",),
}


def load_rows(connection: duckdb.DuckDBPyConnection, rows: list[tuple]) -> None:
    connection.execute("create schema if not exists raw")
    connection.execute("drop table if exists raw.requests")
    connection.execute("""
        create table raw.requests (
            request_id varchar, created_at timestamp, closed_at timestamp,
            status varchar, agency varchar, complaint_type varchar, borough varchar
        )
    """)
    connection.executemany("insert into raw.requests values (?, ?, ?, ?, ?, ?, ?)", rows)


def read_rows(source: Path) -> list[tuple]:
    with source.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        available = set(reader.fieldnames or [])
        mapping = {target: next((field for field in aliases if field in available), None) for target, aliases in SOURCE_ALIASES.items()}
        missing = [target for target, field in mapping.items() if field is None]
        if missing:
            raise ValueError(f"missing required fields {missing}; found {reader.fieldnames}")
        return [tuple(row[mapping[column]] or None for column in TARGET_COLUMNS) for row in reader]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--database", type=Path, default=Path("target/ae_product.duckdb"))
    args = parser.parse_args()
    database = args.database.resolve()
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(database))
    try:
        connection.execute("create schema if not exists raw")
        connection.execute("drop table if exists raw.requests")
        connection.execute(
            """
            create table raw.requests as
            select
                cast(unique_key as varchar) as request_id,
                try_cast(cast(created_date as varchar) as timestamp) as created_at,
                try_cast(cast(closed_date as varchar) as timestamp) as closed_at,
                cast(status as varchar) as status,
                cast(agency as varchar) as agency,
                cast(complaint_type as varchar) as complaint_type,
                nullif(cast(borough as varchar), '') as borough
            from read_csv_auto(?, header = true)
            """,
            [str(args.source.resolve())],
        )
        row_count = connection.execute("select count(*) from raw.requests").fetchone()[0]
        print(f"loaded raw.requests: {row_count:,} rows")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
