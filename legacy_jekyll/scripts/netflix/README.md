# Netflix Content Strategy analysis scripts

The current article uses the 8,807-title Netflix Movies and TV Shows dataset by Shivam Bansal. Download the source file from the [Zenodo snapshot](https://zenodo.org/records/13925131) or the [original Kaggle dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) and save it as `analysis_data/raw/netflix_titles.csv`. The expected MD5 is `0bc7e8d9621caab0a32f46d054faca7f`. Raw data is excluded from Git by the repository ignore rules.

Regenerate the three chart assets referenced by the current article with:

```bash
python scripts/generate_chart_replacements.py netflix
```

The chart generator verifies the source hash and asserts the article's key same-year acquisition, movie-cluster, and UK metadata figures. The older scripts in this folder document the historical pipeline; they expect intermediate files from that archived workflow.
