# Online Retail metric validation

The Online Retail case publishes metrics from a pinned UCI source snapshot. Raw inputs live under the Git-ignored `analysis_data/` directory and are not committed.

Download and inspect the source from the repository root:

```bash
python scripts/download_inspect_sources.py online_retail
```

The downloader records the source URL and SHA-256 in `analysis_data/inventory.json` and extracts the workbook to `analysis_data/extracted/Online Retail.xlsx`.

Recompute the published case metrics and charts:

```bash
python scripts/generate_chart_replacements.py retail
```

The chart script checks the workbook against the recorded 20 August 2026 snapshot hash before calculating metrics. A mismatch stops the run so the changed source can be reviewed before updating the evidence manifest. The metric assertions distinguish a computation or cleaning regression from source drift.
