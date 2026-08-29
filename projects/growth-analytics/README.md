# Growth analytics interview portfolio

These three projects are decision studies for Growth Analyst and Marketplace Analytics interviews. They use official or company-released data, keep raw files outside Git, and separate observed evidence from assumptions and hypotheses.

## Reproducibility

```text
python scripts/download_growth_sources.py
python projects/growth-analytics/01-campaign-incrementality/src/analyze.py
```

The Criteo file is the unbiased 13,979,592-row release. The TLC work uses the official TLC Open Data API for a bounded HVFHV slice and official TLC Parquet files where available. The current TLC endpoint is heavily throttled, so the analysis scripts fail clearly rather than silently using an incomplete file.

## Projects

1. Campaign incrementality: decide whether a randomized ad campaign creates additional visits and conversions.
2. Marketplace supply and demand: diagnose where completed HVFHV trips concentrate and what the public data cannot observe about unmet demand.
3. Congestion-pricing causal impact: define and test an econometric design around 5 January 2025 without presenting a before/after comparison as causal proof.
