# Supporting-case metric validation

The Online Retail and NYC restaurant case studies publish metrics from pinned source snapshots. Raw inputs live under ignored `analysis_data/` paths and are intentionally not committed.

Prepare only the two required sources:

```bash
python scripts/download_inspect_sources.py online_retail nyc_restaurants
```

The downloader records source URLs and SHA-256 hashes in `analysis_data/inventory.json` and extracts the retail workbook to `analysis_data/extracted/Online Retail.xlsx`. The mutable restaurant extract is stored at `analysis_data/raw/nyc_restaurants.csv`.

Recompute every published supporting-case metric and chart:

```bash
python scripts/generate_chart_replacements.py retail restaurant
```

The chart script first compares each input with the recorded 20 August 2026 snapshot hash. A hash mismatch is reported as source drift and requires a fresh metric review; metric assertions then distinguish a computation or cleaning regression from changed source data.
