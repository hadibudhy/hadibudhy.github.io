"""Hand-checked input contracts: malformed rows must stop or enter quarantine."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ingest import validate_records

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
