# Netflix Content Strategy — Analysis Scripts

Python scripts for the [Netflix Content Strategy case study](https://hadibudhy.github.io/product%20analytics/netflix-content-strategy/).

## Data

Source: `netflix_titles.csv` (public Kaggle dataset — 8,807 titles, 2008–2021).

The raw CSV is not included. Download it from [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows) and place it at `data/netflix_titles.csv`.

## Scripts

| Script | Description |
|--------|-------------|
| `phase0_clean.py` | Data cleaning — acquisition lag engineering, country bucketing, metadata completeness tiers |
| `phase2b_cluster.py` | K-Means clustering — 5 content clusters by type, language, and genre features |
| `validation_script.py` | 4-layer validation — structural, logical, business rules, Simpson's Paradox checks |
| `generate_charts.py` | Chart generation — all 6 presentation-ready charts (dark theme, SWD style) |
| `chart_helpers.py` | Chart style helpers — `hadi_dark()`, `highlight_bar()`, `highlight_line()`, `action_title()` |

## Setup

```bash
pip install pandas numpy matplotlib scikit-learn pyarrow
```

## Run order

```bash
python phase0_clean.py          # outputs: working/netflix/clean_df.parquet
python phase2b_cluster.py       # outputs: working/netflix/cluster_data.csv
python validation_script.py     # outputs: validation report
python generate_charts.py       # outputs: outputs/charts/beat_01-06.png
```
