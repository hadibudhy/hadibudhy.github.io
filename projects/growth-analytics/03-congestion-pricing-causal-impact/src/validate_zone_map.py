"""Map official TLC taxi zones to the official NY State/MTA CBD geofence."""

from __future__ import annotations

import json
from pathlib import Path

import shapefile
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform, unary_union


ROOT = Path(__file__).resolve().parents[4]
ZONE_ZIP = ROOT / "analysis_data/growth_sources/taxi_zones.zip"
GEOFENCE = ROOT / "analysis_data/growth_sources/mta_cbd_geofence.json"
OUTPUT = ROOT / "analysis_data/growth_sources/cbd_taxi_zone_mapping.json"


def main() -> None:
    geofences = [shape(row["polygon"]) for row in json.loads(GEOFENCE.read_text(encoding="utf-8"))]
    cbd = unary_union(geofences)
    reader = shapefile.Reader(str(ZONE_ZIP))
    fields = [field[0] for field in reader.fields[1:]]
    to_wgs84 = Transformer.from_crs("EPSG:2263", "EPSG:4326", always_xy=True).transform
    results = []
    for record, raw_shape in zip(reader.records(), reader.shapes()):
        values = dict(zip(fields, record))
        zone = transform(to_wgs84, shape(raw_shape.__geo_interface__))
        overlap = zone.intersection(cbd).area / zone.area if zone.area else 0
        classification = "inside" if overlap >= 0.95 else "partial" if overlap > 0.05 else "outside"
        results.append({"LocationID": int(values["LocationID"]), "zone": values["zone"], "borough": values["borough"], "overlap_ratio": round(overlap, 6), "classification": classification})
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    counts = {key: sum(row["classification"] == key for row in results) for key in ["inside", "partial", "outside"]}
    print(json.dumps({"zones": len(results), "classification_counts": counts, "partial_zones": [row for row in results if row["classification"] == "partial"], "output": str(OUTPUT)}, indent=2))


if __name__ == "__main__":
    main()
