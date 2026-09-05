# Analytics Engineering foundation

Local dbt Core + DuckDB project for the public portfolio cases.

## Layers

raw source files -> staging -> intermediate -> marts -> metric views -> evidence

The source contract lives in `contracts/product_event_tracking.yml`; shared metric
definitions live in `metrics.yml`. They are reviewed inputs to the models, not
claims that the public source contains a complete production product schema.

The raw event file remains outside Git. The full-data profile records source hash, retrieval time, row count, event types, missingness, and event-time coverage. CI uses the small committed seed to test contracts and replay behavior.

## Commands

python -m pip install -r analytics/requirements.txt
python analytics/load_rees46.py --source analysis_data/product-events/electronics-events.csv.gz
dbt build --profiles-dir analytics --project-dir analytics
dbt docs generate --profiles-dir analytics --project-dir analytics

For a pull request, replace the raw source with the committed CI seed and run
`dbt seed --profiles-dir analytics --project-dir analytics --select events`.

The first product path models events at source grain, orders events deterministically within sessions, and produces funnel and data-quality marts.
