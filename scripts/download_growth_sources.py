"""Download the official sources used by the three growth-analysis projects.

Large raw files are stored under ignored analysis_data/growth_sources/.
"""

from __future__ import annotations

import hashlib
import argparse
import json
import shutil
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis_data" / "growth_sources"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "criteo_uplift_unbiased": (
        "https://criteostorage.blob.core.windows.net/criteo-research-datasets/criteo-uplift-v2.1.csv.gz",
        "criteo-uplift-v2.1.csv.gz",
    ),
    "tlc_hvfhv_january_2025": (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2025-01.parquet",
        "fhvhv_tripdata_2025-01.parquet",
    ),
    "tlc_zone_lookup": (
        "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv",
        "taxi_zone_lookup.csv",
    ),
    "tlc_monthly_reports": (
        "https://www.nyc.gov/assets/tlc/downloads/csv/data_reports_monthly.csv",
        "data_reports_monthly.csv",
    ),
    "tlc_taxi_zones_geometry": (
        "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip",
        "taxi_zones.zip",
    ),
    "mta_cbd_geofence": (
        "https://data.ny.gov/resource/srxy-5nxn.json?$limit=5000",
        "mta_cbd_geofence.json",
    ),
    "mta_crz_vehicle_entries_q1_2025": (
        "https://data.ny.gov/resource/t6yz-b64h.json?$select=toll_date,vehicle_class,sum(crz_entries)%20as%20crz_entries,sum(excluded_roadway_entries)%20as%20excluded_roadway_entries&$where=toll_date%20between%20%272025-01-01T00:00:00%27%20and%20%272025-03-31T00:00:00%27&$group=toll_date,vehicle_class&$order=toll_date,vehicle_class&$limit=50000",
        "mta_crz_vehicle_entries_q1_2025.json",
    ),
}


def download(name: str, url: str, filename: str) -> dict:
    target = OUT / filename
    if not target.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "Hadi Budhy growth analysis research"})
        with urllib.request.urlopen(request, timeout=300) as response, target.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"name": name, "url": url, "path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": digest.hexdigest()}


def download_ranged(name: str, url: str, filename: str, total_bytes: int, chunks: int = 8) -> dict:
    """Resume a large public file using independent HTTP range requests."""
    target = OUT / filename
    parts_dir = OUT / f"{filename}.parts"
    parts_dir.mkdir(exist_ok=True)
    ranges = []
    for index in range(chunks):
        start = total_bytes * index // chunks
        end = total_bytes * (index + 1) // chunks - 1
        ranges.append((index, start, end))

    def fetch(item: tuple[int, int, int]) -> None:
        index, start, end = item
        part = parts_dir / f"{index:02d}.part"
        expected = end - start + 1
        if part.exists() and part.stat().st_size == expected:
            return
        subprocess.run(["curl.exe", "-L", "--fail", "--range", f"{start}-{end}", "-o", str(part), url], check=True, timeout=900, capture_output=True)
        if part.stat().st_size != expected:
            raise RuntimeError(f"Unexpected range size for {part.name}: {part.stat().st_size} != {expected}")

    with ThreadPoolExecutor(max_workers=chunks) as pool:
        list(pool.map(fetch, ranges))
    with target.open("wb") as output:
        for index, _, _ in ranges:
            with (parts_dir / f"{index:02d}.part").open("rb") as part:
                shutil.copyfileobj(part, output)
    if target.stat().st_size != total_bytes:
        raise RuntimeError(f"Unexpected final size: {target.stat().st_size} != {total_bytes}")
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"name": name, "url": url, "path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": digest.hexdigest(), "download": "parallel_http_ranges"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-hvfhv", action="store_true", help="Attempt the large 2025 HVFHV Parquet download")
    args = parser.parse_args()
    manifest = [download("criteo_uplift_unbiased", *SOURCES["criteo_uplift_unbiased"])]
    manifest.append(download("tlc_zone_lookup", *SOURCES["tlc_zone_lookup"]))
    for name in ["tlc_monthly_reports", "tlc_taxi_zones_geometry", "mta_cbd_geofence", "mta_crz_vehicle_entries_q1_2025"]:
        manifest.append(download(name, *SOURCES[name]))
    if args.include_hvfhv:
        manifest.append(download_ranged("tlc_hvfhv_january_2025", *SOURCES["tlc_hvfhv_january_2025"], total_bytes=491076642))
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
