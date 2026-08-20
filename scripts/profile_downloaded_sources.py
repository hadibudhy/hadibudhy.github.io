"""Create reproducible structural profiles for the local public-data downloads."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "analysis_data" / "raw"
OUT = ROOT / "analysis_data" / "profiles.json"


def profile_table(path: Path, **read_kwargs) -> dict:
    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
        return table_result(path, df)
    if path.suffix in {".xls", ".xlsx"}:
        sheets = pd.read_excel(path, sheet_name=None, **read_kwargs)
        return {"file": str(path.relative_to(ROOT)), "sheets": {name: table_result(path, frame) for name, frame in sheets.items()}}
    if path.suffix == ".csv":
        chunks = []
        rows = 0
        missing = None
        columns = []
        for frame in pd.read_csv(path, chunksize=100_000, low_memory=False, encoding_errors="replace", **read_kwargs):
            if not columns:
                columns = list(frame.columns)
                missing = {column: 0 for column in columns}
            rows += len(frame)
            for column in columns:
                missing[column] += int(frame[column].isna().sum())
            chunks.append(frame.head(1))
        sample = pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()
        return {"file": str(path.relative_to(ROOT)), "rows": rows, "columns": columns, "missing": missing, "duplicate_sample_rows": int(sample.duplicated().sum()), "read_options": read_kwargs}
    return {"file": str(path.relative_to(ROOT)), "status": "unsupported_table_format"}


def table_result(path: Path, frame: pd.DataFrame) -> dict:
    return {
        "file": str(path.relative_to(ROOT)),
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "missing": {str(key): int(value) for key, value in frame.isna().sum().items() if int(value)},
        "duplicate_rows": int(frame.duplicated().sum()),
        "dtypes": {str(key): str(value) for key, value in frame.dtypes.items()},
    }


def main() -> None:
    extracted = ROOT / "analysis_data" / "extracted"
    extracted.mkdir(parents=True, exist_ok=True)
    profiles = []
    for path in sorted(RAW.iterdir()):
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as archive:
                candidates = [name for name in archive.namelist() if name.lower().endswith((".csv", ".xls", ".xlsx"))]
                nested = [name for name in archive.namelist() if name.lower().endswith(".zip")]
                for nested_name in nested:
                    nested_target = extracted / Path(nested_name).name
                    if not nested_target.exists():
                        nested_target.write_bytes(archive.read(nested_name))
                    with zipfile.ZipFile(nested_target) as nested_archive:
                        candidates.extend(f"{nested_name}/{name}" for name in nested_archive.namelist() if name.lower().endswith((".csv", ".xls", ".xlsx")))
                if not candidates:
                    profiles.append({"file": str(path.relative_to(ROOT)), "members": archive.namelist(), "status": "no_tabular_member"})
                    continue
                archive_profiles = []
                for member in candidates:
                    if "/" in member and member.split("/", 1)[0].lower().endswith(".zip"):
                        nested_name, nested_member = member.split("/", 1)
                        nested_path = extracted / Path(nested_name).name
                        target = extracted / Path(nested_member).name
                        if not target.exists():
                            with zipfile.ZipFile(nested_path) as nested_archive:
                                target.write_bytes(nested_archive.read(nested_member))
                    else:
                        target = extracted / Path(member).name
                        if not target.exists():
                            target.write_bytes(archive.read(member))
                    try:
                        if target.suffix.lower() == ".xls":
                            archive_profiles.append({"member": member, "profile": profile_table(target, header=1)})
                        elif target.suffix.lower() == ".csv":
                            sample = target.read_text(encoding="latin-1", errors="replace")[:4096]
                            delimiter = ";" if sample.count(";") > sample.count(",") else ","
                            archive_profiles.append({"member": member, "profile": profile_table(target, sep=delimiter, encoding="latin-1")})
                        else:
                            archive_profiles.append({"member": member, "profile": profile_table(target)})
                    except Exception as exc:
                        archive_profiles.append({"member": member, "profile": {"file": str(target.relative_to(ROOT)), "status": "profile_failed", "error": str(exc)}})
                profiles.append({"archive": str(path.relative_to(ROOT)), "profiles": archive_profiles})
        elif path.suffix in {".csv", ".parquet", ".xlsx"}:
            if path.suffix == ".csv":
                sample = path.read_text(encoding="latin-1", errors="replace")[:4096]
                delimiter = ";" if sample.count(";") > sample.count(",") else ","
                profiles.append(profile_table(path, sep=delimiter, encoding="latin-1"))
            else:
                profiles.append(profile_table(path))
    (OUT).write_text(json.dumps(profiles, indent=2, default=str), encoding="utf-8")
    print(json.dumps(profiles, indent=2, default=str))


if __name__ == "__main__":
    main()
