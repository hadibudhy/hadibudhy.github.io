"""Download and inspect public source inputs without adding raw data to git.

The output is written to analysis_data/inventory.json, which is ignored by git.
Large sources are downloaded because reproducibility requires inspecting the
actual files, not only their landing pages.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "analysis_data"
RAW = DATA / "raw"
RAW.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "online_retail": "https://archive.ics.uci.edu/static/public/352/online+retail.zip",
    "clickstream": "https://archive.ics.uci.edu/static/public/553/clickstream+data+for+online+shopping.zip",
    "bank_marketing": "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip",
    "credit_default": "https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip",
    "world_happiness_2026": "https://files.worldhappiness.report/WHR26_Data_Figure_2.1.xlsx",
    "nyc_taxi_january_2025": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet",
    "nyc_taxi_zones": "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv",
    "nyc_restaurants": "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD",
    "airbnb_nyc_june_2026": "https://data.insideairbnb.com/united-states/ny/new-york-city/2026-06-14/visualisations/listings.csv",
    "sec_microsoft_companyfacts": "https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json",
}

BLS_SERIES = [
    "JTS000000000000000JOL",
    "JTS000000000000000HIR",
    "JTS000000000000000QUR",
    "JTS000000000000000TSL",
]


def download(name: str, url: str) -> dict:
    suffix = Path(url.split("?")[0]).suffix or ".bin"
    target = RAW / f"{name}{suffix}"
    if not target.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "portfolio-analysis-research contact@example.com"})
        with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return {"name": name, "url": url, "path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": digest}


def inspect_file(item: dict) -> dict:
    path = ROOT / item["path"]
    result = dict(item)
    result["status"] = "downloaded"
    try:
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as archive:
                result["members"] = archive.namelist()
                result["status"] = "archive_downloaded"
        elif path.suffix == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="", errors="replace") as handle:
                reader = csv.reader(handle)
                header = next(reader, [])
                rows = [next(reader, []) for _ in range(10)]
                result["columns"] = header
                result["sample_rows"] = len([row for row in rows if row])
                result["status"] = "tabular_sampled"
        elif path.suffix == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            result["top_level_keys"] = list(payload)[:20] if isinstance(payload, dict) else []
            result["status"] = "json_inspected"
        elif path.suffix in {".parquet", ".xlsx"}:
            result["status"] = "binary_downloaded_requires_table_reader"
    except Exception as exc:  # Keep the inventory complete even if one source changes format.
        result["status"] = "downloaded_inspection_failed"
        result["error"] = str(exc)
    return result


def download_bls() -> dict:
    target = RAW / "bls_jolts_2025.json"
    if not target.exists():
        payload = json.dumps({"seriesid": BLS_SERIES, "startyear": "2025", "endyear": "2025"}).encode("utf-8")
        request = urllib.request.Request(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "portfolio-analysis-research contact@example.com"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    return {
        "name": "bls_jolts_2025",
        "url": "https://api.bls.gov/publicAPI/v2/timeseries/data/",
        "path": str(target.relative_to(ROOT)),
        "bytes": target.stat().st_size,
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "status": "json_inspected",
        "series": BLS_SERIES,
    }


def main() -> None:
    inventory = []
    for name, url in SOURCES.items():
        try:
            inventory.append(inspect_file(download(name, url)))
        except Exception as exc:
            inventory.append({"name": name, "url": url, "status": "download_failed", "error": str(exc)})
    try:
        inventory.append(download_bls())
    except Exception as exc:
        inventory.append({"name": "bls_jolts_2025", "status": "download_failed", "error": str(exc)})
    (DATA / "inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print(json.dumps(inventory, indent=2))


if __name__ == "__main__":
    main()
