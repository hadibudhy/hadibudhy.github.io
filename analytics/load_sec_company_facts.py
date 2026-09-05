"""Load an SEC Company Facts JSON snapshot into DuckDB at fact grain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import duckdb


def rows_from_facts(payload: dict) -> list[tuple]:
    rows: list[tuple] = []
    for taxonomy, facts in payload.get("facts", {}).items():
        for tag, definition in facts.items():
            for unit, observations in definition.get("units", {}).items():
                for observation in observations:
                    values = (
                        taxonomy, tag, unit, observation.get("fy"), observation.get("fp"),
                        observation.get("frame"), observation.get("filed"), observation.get("end"),
                        observation.get("start"), observation.get("val"), observation.get("accn"),
                        observation.get("form"),
                    )
                    fact_id = hashlib.sha256("|".join(map(str, values)).encode()).hexdigest()
                    rows.append((fact_id, tag, unit, observation.get("fy"), observation.get("fp"), observation.get("frame"), observation.get("filed"), observation.get("end"), observation.get("start"), observation.get("val"), observation.get("accn"), observation.get("form")))
    return rows


def load_rows(connection: duckdb.DuckDBPyConnection, rows: list[tuple]) -> None:
    connection.execute("create schema if not exists raw")
    connection.execute("drop table if exists raw.company_facts")
    connection.execute("""
        create table raw.company_facts (
            fact_id varchar, tag varchar, unit varchar, fy integer, fp varchar,
            frame varchar, filed date, end_date date, start_date date, value double,
            accession varchar, form varchar
        )
    """)
    connection.executemany("insert into raw.company_facts values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--database", type=Path, default=Path("target/ae_product.duckdb"))
    args = parser.parse_args()
    payload = json.loads(args.source.read_text(encoding="utf-8"))
    rows = rows_from_facts(payload)
    database = args.database.resolve()
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(database))
    try:
        load_rows(connection, rows)
        print(f"loaded raw.company_facts: {len(rows):,} rows")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
