"""Hand-checked input contracts: malformed rows must stop or enter quarantine."""
import sys
from pathlib import Path
import pytest
import duckdb
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ingest import validate_records
from load_sec_company_facts import rows_from_facts
from load_sec_company_facts import load_rows as load_sec_rows
from load_nyc311 import load_rows as load_311_rows

def test_missing_key_cannot_be_loaded_as_a_valid_request():
    with pytest.raises(ValueError, match="unique_key"):
        validate_records([{"created_date": "2025-01-01"}], ["unique_key", "created_date"], "unique_key")

def test_duplicate_request_keys_cannot_multiply_a_snapshot():
    with pytest.raises(ValueError, match="duplicate"):
        validate_records([{"unique_key": "1"}, {"unique_key": "1"}], ["unique_key"], "unique_key")

def test_valid_records_are_not_rewritten_by_validation():
    rows = [{"unique_key": "1", "closed_date": None}, {"unique_key": "2"}]
    assert validate_records(rows, ["unique_key"], "unique_key") == rows

def test_empty_api_response_is_not_a_complete_extract():
    with pytest.raises(ValueError, match="empty"):
        validate_records([], ["unique_key"], "unique_key")

def test_sec_fact_loader_preserves_one_row_per_reported_observation():
    payload = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [{"fy": 2024, "fp": "FY", "filed": "2024-07-30", "end": "2024-06-30", "val": 10, "accn": "a", "form": "10-K"}]}}}}}
    rows = rows_from_facts(payload)
    assert len(rows) == 1
    assert rows[0][1] == "Revenues"
    assert rows[0][-1] == "10-K"

def test_sec_loader_writes_a_queryable_raw_relation():
    payload = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [{"fy": 2024, "fp": "FY", "filed": "2024-07-30", "end": "2024-06-30", "val": 10, "accn": "a", "form": "10-K"}]}}}}}
    with duckdb.connect(":memory:") as connection:
        load_sec_rows(connection, rows_from_facts(payload))
        assert connection.execute("select count(*) from raw.company_facts").fetchone()[0] == 1

def test_311_loader_writes_a_queryable_raw_relation():
    rows = [("1", "2025-01-01 00:00:00", None, "Open", "DEP", "Water", "QUEENS")]
    with duckdb.connect(":memory:") as connection:
        load_311_rows(connection, rows)
        assert connection.execute("select count(*) from raw.requests").fetchone()[0] == 1
