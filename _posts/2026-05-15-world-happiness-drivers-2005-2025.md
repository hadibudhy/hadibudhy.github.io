---
title: "World Happiness Drivers 2005–2025"
date: 2026-05-15
categories: data-scientist
tags: [python, duckdb, correlation, global-data, happiness]
excerpt: "Social support and GDP explain most of why some countries are happy. Generosity does not."
header:
  teaser: /images/world-happiness-drivers-2005-2025/teaser.png
mathjax: false
---

## The Story

Which factors predict whether a country is happy — and has the world actually gotten happier over time?

I used the World Happiness Report dataset to find out. It covers 168 countries from 2011 to 2025. The dataset records annual Cantril Ladder scores — a 0 to 10 self-report of life satisfaction — alongside six contributing factors: GDP per capita, social support, healthy life expectancy, freedom, generosity, and corruption perception.

**Key findings:**

- **The world has gotten measurably happier.** Average happiness rose from 5.39 in 2011 to 5.65 in 2025 — a gain of 0.26 points. The trend is statistically significant (Spearman r=0.87, p<0.001, slope=0.019 points/year). That is small in absolute terms, but consistent across 14 years and 140+ countries.
- **Social support and GDP are the strongest predictors.** Both show Spearman correlations above 0.70 with happiness scores (social support: r=0.701, GDP: r=0.716). Healthy life expectancy follows at r=0.672. These three factors account for most of the variation between happy and unhappy countries.
- **Generosity barely matters.** The correlation between generosity and happiness is r=0.042 — not statistically significant (p=0.18). Countries that score high on charitable giving are not systematically happier. This contradicts the common assumption that generosity and wellbeing go together at the national level.
- **Serbia improved the most (+2.1 points) since 2011; Afghanistan declined the most (-2.8 points).** Serbia's rise tracks economic development and EU integration. Afghanistan's collapse follows the 2021 political transition. Most countries moved less than 0.5 points in the same period.
- **Happiness inequality is widening.** The gap between the happiest and least happy country grew from 4.8 points in 2011 to 6.3 points in 2025 — a 31% increase. While the global average rises, the bottom is falling faster than the top is climbing.

The generosity finding is the most surprising. One plausible explanation: the WHR generosity measure captures charitable donations, which are concentrated in wealthier countries with formal giving infrastructure. It may not capture informal mutual aid common in lower-income countries. The metric may reflect economic structure more than genuine social generosity.

The widening inequality finding is the most concerning. Global averages mask growing divergence. If the goal is higher happiness for more people, the aggregate trend is misleading. The countries that need improvement most are falling further behind.

---

## How I Did It

**Tools and stack:** Python 3.12 · pandas 2.0 · DuckDB 0.10 · scipy 1.12 · matplotlib 3.8

**Data quality:** The dataset has two clean segments. Core columns (`year`, `country`, `happiness_score`, `rank_in_year`) are 100% complete across all 2,116 rows. The factor decomposition columns are null for 2011–2018 — the WHR added decomposition starting with the 2019 report. This is expected, not a data error. The 2019–2025 subset (1,019 country-years) was used for all driver analysis.

One minor anomaly: Gambia and Sri Lanka share rank 120 in the 2018 dataset despite different scores (4.516 vs 4.366). This appears to be a source transcription error. It does not affect any headline finding.

**Methodology decisions:**

- I used Spearman correlation rather than Pearson for driver analysis. Cantril Ladder scores are bounded (0–10) and driver contribution distributions are right-skewed. Spearman is more robust to both conditions. Results were nearly identical to Pearson for top drivers, confirming the relationship is not an artifact of method choice.
- I restricted driver analysis to 2019–2025. Using 2011–2018 rows (which lack decomposition data) would have required imputation — introducing noise with no analytical benefit. The 2019–2025 sample covers 7 years and 1,019 country-year observations, sufficient for reliable estimates.
- Year 2013 is absent from the dataset (the WHR was not published that year). I treated it as a missing data point rather than interpolating.

**Validation:** Driver contributions sum to happiness score within 0.003 tolerance (DuckDB-verified). Score range (1.36–7.86) is within the plausible Cantril Ladder bounds. Correlation directions match the WHR's own published findings. Key statistics (Serbia +2.13, Afghanistan -2.81, global slope 0.019/year) were verified directly against the source data. A pandas-vs-DuckDB tie-out confirmed 2,116 rows and a score sum of 11,565.33 before any analysis.

---

## Key Code

The global trend regression uses `scipy.stats.linregress` on year-averaged scores. The slope of 0.019 points per year means the world gains roughly one full point of happiness every 53 years at the current rate.

```python
global_trend = con.execute("""
    SELECT year, ROUND(AVG(happiness_score), 4) as avg_score
    FROM happiness
    GROUP BY year ORDER BY year
""").df()

slope, intercept, r, p, se = stats.linregress(global_trend['year'], global_trend['avg_score'])
```

Driver correlations use Spearman to handle the bounded scale and skewed distributions. The null mask ensures we only compare rows where both the happiness score and the driver value are present — three driver columns have a small number of missing values even in the 2019-2025 subset.

```python
df_drivers = con.execute("""
    SELECT happiness_score, explained_log_gdp_per_capita,
           explained_social_support, explained_healthy_life_expectancy,
           explained_freedom, explained_generosity, explained_corruption
    FROM happiness
    WHERE year >= 2019 AND explained_log_gdp_per_capita IS NOT NULL
""").df()

for col, label in driver_cols:
    mask = df_drivers['happiness_score'].notna() & df_drivers[col].notna()
    r_val, p_val = stats.spearmanr(df_drivers.loc[mask, 'happiness_score'],
                                   df_drivers.loc[mask, col])
    driver_correlations[label] = {'r': round(r_val, 3), 'p': round(p_val, 6)}
```

The biggest-movers query joins the 2011 and 2025 snapshots on country name, then sorts by score change. This pattern is reusable for any two-year comparison in the dataset.

```python
biggest_movers = con.execute("""
    WITH y2011 AS (SELECT country, happiness_score as s2011 FROM happiness WHERE year=2011),
         y2025 AS (SELECT country, happiness_score as s2025 FROM happiness WHERE year=2025)
    SELECT y2025.country,
           ROUND(s2011, 3) as score_2011,
           ROUND(s2025, 3) as score_2025,
           ROUND(s2025 - s2011, 3) as change
    FROM y2025 JOIN y2011 ON y2025.country = y2011.country
    ORDER BY change DESC
""").df()
```

> Charts: `outputs/charts/` · Full analysis code: `working/analysis_world_happiness_report_2005_2025_2026-05-15.py`
