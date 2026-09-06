"""Verify the finance reference values against pinned SEC filing documents."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from urllib.request import Request, urlopen
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "analytics" / "seeds" / "ci" / "expected_financial_metrics.csv"
RAW = ROOT.parents[1] / "analysis_data" / "raw"


def document_for_accession(accession: str) -> Path:
    return RAW / {"0000950170-24-087843": "msft-2024-10k.htm", "0000950170-25-100235": "msft-2025-10k.htm", "0001193125-26-323660": "msft-2026-10k.htm"}[accession]


def download_documents(rows: list[dict[str, str]]) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for row in rows:
        destination = document_for_accession(row["source_accession"])
        if destination.exists():
            continue
        request = Request(row["source_document_url"], headers={"User-Agent": "portfolio-evidence-verifier/1.0"})
        destination.write_bytes(urlopen(request, timeout=60).read())


def display_millions(value: str) -> str:
    return f"{int(value) // 1_000_000:,}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="download missing official SEC filing documents before checking their hashes")
    args = parser.parse_args()
    with REFERENCE.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if args.download:
        download_documents(rows)
    for row in rows:
        document = document_for_accession(row["source_accession"])
        contents = document.read_bytes()
        actual_hash = hashlib.sha256(contents).hexdigest()
        if actual_hash != row["source_document_sha256"]:
            raise AssertionError(f"filing hash mismatch for {document}")
        text = contents.decode("utf-8", errors="replace")
        for value in (display_millions(row["revenue"]), display_millions(row["net_income"])):
            if not re.search(rf">{re.escape(value)}<", text):
                raise AssertionError(f"{value} not found in {document}")
    print(f"verified {len(rows)} annual finance references against pinned 10-K filings")


if __name__ == "__main__":
    main()
