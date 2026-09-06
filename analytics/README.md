# Analytics Engineering foundation

Local dbt Core + DuckDB project for the public portfolio cases.

## Layers

raw source files -> staging -> intermediate -> marts -> metric views -> evidence

The source contract lives in `contracts/product_event_tracking.yml`; shared metric
definitions live in `metrics.yml`. They are reviewed inputs to the models, not
claims that the public source contains a complete production product schema.

The raw event file remains outside Git. The full-data profile records source hash, retrieval time, row count, event types, missingness, and event-time coverage. CI uses the small committed seed to test contracts and replay behavior.

The public case studies use two evidence levels:

- CI seeds prove model contracts, ordering, cutoff rules, and failure behavior.
- `scripts/build_senior_evidence.py` runs against the pinned full public snapshots and produces only aggregate JSON and charts under `public/`.
- Set `SENIOR_FULL_DBT=1` when a full-data dbt database is available and you want the evidence builder to reconcile Python output to that database. CI fixtures are intentionally not compared with full public snapshots.

## Commands

python -m pip install -r analytics/requirements.txt
python analytics/load_rees46.py --source analysis_data/product-events/electronics-events.csv.gz
python analytics/load_sec_company_facts.py --source analysis_data/raw/sec_microsoft_companyfacts.json
python analytics/download_nyc311.py
python analytics/load_nyc311.py --source analysis_data/service/nyc311-2025-01.csv
dbt build --profiles-dir analytics --project-dir analytics
python scripts/verify_financial_filing_extracts.py --download
dbt docs generate --profiles-dir analytics --project-dir analytics
python scripts/build_senior_evidence.py

For a pull request, replace the raw source with the committed CI seed and run
`dbt seed --profiles-dir analytics --project-dir analytics --select events`.

The first product path models events at source grain, orders events deterministically within sessions, and produces funnel and data-quality marts.

The public REES46 source is a static snapshot, so its staging model rebuilds as a table. A future append-only source would require a stable producer event ID or a separately tested ingestion ledger before incremental loading is enabled.
