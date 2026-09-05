def validate_records(rows, required, key):
    """Validate an input batch before it can enter a model.

    The function intentionally returns the original row objects. The loader
    owns validation; staging owns type conversion, so failures stay visible.
    """
    if not rows:
        raise ValueError("empty input batch")
    missing = [column for row in rows for column in required if not row.get(column)]
    if missing:
        raise ValueError(f"missing required field: {missing[0]}")
    keys = [row[key] for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError(f"duplicate {key} values")
    return rows
