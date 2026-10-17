---
title: "What 14 Years of Happiness Data Really Shows"
date: 2026-05-10
categories: product analytics
tags:
  - data-analysis
  - world-happiness-report
  - exploratory-analysis
excerpt: "A consistent country panel separates long-term progress from changing rankings and shows where the score gap widened."
problem: "Single-year rankings obscure how happiness changes across countries and over time."
result: "Across the same 129 countries, the unweighted average life evaluation rose from 5.47 in 2011 to 5.74 in 2025 while the highest-to-lowest gap widened."
featured: false
published: true
caseId: world-happiness-report
kind: completed
primaryTrack: product-analytics
displayOrder: 80
evidenceManifest: /data/evidence/world-happiness-report.json
evidenceVisuals:
  - /images/happiness-beat01.png
  - /images/happiness-beat02.png
  - /images/happiness-beat03.png
  - /images/happiness-beat04.png
  - /images/happiness-drivers-inequality.png
  - /images/happiness-beat05-bottom-cohort.png
header:
  teaser: /images/happiness-beat01.png
---

## Project brief

- **Project:** Compare reported life evaluations across a balanced country panel.
- **Question:** How did scores change, and did the gap between countries narrow?
- **Built:** A 129-country panel, trend and range measures, country comparisons, and factor correlations.
- **Result:** The average rose from 5.47 to 5.74. The lowest 13 countries in 2011 rose from 3.80 to 4.35 by 2025, while the overall range widened.

## Business question

Annual rankings can change because countries enter or leave the comparison. A policy team needs to know whether the same countries improved, whether gaps narrowed, and which factors moved with life evaluations.

The question is: **how did national life evaluations change from 2011 to 2025, which countries moved most, and which reported factors were most closely associated with the scores?**

## Data and preparation

The [World Happiness Report 2026 Figure 2.1 workbook](https://www.worldhappiness.report/data-sharing/) covers 168 countries in 14 measured years from 2011 through 2025. The source has no 2013 observation. I use the 129 countries with data in all measured years. Scores are self-reported three-year-average life evaluations on a 0 to 10 scale. Country averages are unweighted. Factor correlations use observations from 2019 to 2025.

## Stakeholder questions

- **Did the same countries improve on average?** The 129-country unweighted average increased by 0.26 points from 2011 to 2025.
- **Did the gap narrow?** No. The highest-to-lowest range grew from 4.8 to 6.3 points.
- **Did the 2011 bottom group improve?** Yes. Its average rose by 0.55 points, and its gap from the remaining 116 countries narrowed from 1.86 to 1.54 points.
- **Which reported factors had the strongest associations?** Social support, GDP per person, and healthy life expectancy had correlations of 0.70, 0.68, and 0.66.

## Findings

### The average rose, including after the 2021 to 2022 dip

The balanced-panel average rose from **5.47 in 2011 to 5.74 in 2025**, a **0.26 point** increase. It dipped in 2021 and 2022, then recovered to a panel high in 2025. This does not mean every country improved.

![Balanced panel of 129 countries from 2011 to 2025: the average recovered after the 2021 to 2022 dip](/images/happiness-beat01.png)

### Country scores moved in both directions

Seven of the eight largest gains were in post-Soviet or Balkan countries; China was the exception. Serbia gained **2.13 points**. Afghanistan had the largest decline at **2.81 points**. These comparisons do not show that one policy caused the change.

![Balanced panel of 129 countries from 2011 to 2025: the largest gains and losses show different paths](/images/happiness-beat02.png)

### The largest top-to-bottom gaps were not about income alone

In 2025, the top 10 countries averaged **7.33** and the bottom 10 averaged **3.36**. The average gaps were **0.83 points** for GDP per person, **0.83** for social support, and **0.62** for healthy life expectancy.

![Top 10 and bottom 10 countries in 2025: income, social support, and health had the largest component gaps](/images/happiness-beat03.png)

### Social support, income, and health had the strongest associations

Across country-year observations from 2019 to 2025, correlations with life evaluation were **0.70** for social support, **0.68** for GDP per person, and **0.66** for healthy life expectancy. Generosity had a **0.04** correlation. The factors are related to one another, so these values do not isolate individual effects.

![Countries measured from 2019 to 2025: social support, income, and health had the strongest associations with life evaluation](/images/happiness-beat04.png)

### The highest-to-lowest gap widened

The range grew from **4.8 points in 2011 to 6.3 points in 2025**, an increase of about 31%. A wider range shows more dispersion; it does not tell whether the lowest-scoring group improved or declined without a separate group trend.

![Balanced panel of 129 countries from 2011 to 2025: the highest-to-lowest score range widened](/images/happiness-drivers-inequality.png)

### The 2011 bottom group improved, but remained below other countries

The 13 countries in the bottom decile in 2011 had an average score of **3.80** that year and **4.35** in 2025. The remaining 116 countries averaged **5.66** in 2011 and **5.89** in 2025. The gap between these fixed groups narrowed from **1.86 to 1.54 points**. These are unweighted country averages.

![Life evaluation trend for the 13 countries in the bottom decile in 2011 compared with the remaining 116 countries in the same balanced panel](/images/happiness-beat05-bottom-cohort.png)

## Built

The work selects a balanced country panel, checks country-year uniqueness and period coverage, and calculates average scores, ranges, country changes, factor correlations, and a fixed baseline bottom-decile trend.

## Result

The fixed-panel average increased. The highest-to-lowest range widened, while the baseline bottom-decile gap to the remaining countries narrowed. This supports tracking averages, extremes, and a fixed lower-scoring group together. It does not identify which policy caused a country's change.

- Track country trends over time alongside rankings.
- Review social support, income, and health as connected conditions, not independent causal levers.
- Use the fixed 2011 bottom group to guide follow-up research. Use within-country data before choosing an intervention.

Public country data cannot show which programs changed living conditions or how outcomes differ within a country. A policy team would need local administrative outcomes, program reach, health access, household income, and survey microdata before choosing an intervention.

## Technical notes

The analysis uses the World Happiness Report 2026 data for Figure 2.1. It checks source rows, country-year uniqueness, the 14 measured years, the 129-country balanced panel, and the reported averages, ranges, and factor correlations. The workbook is available from the [official Data Sharing page](https://www.worldhappiness.report/data-sharing/). Code: [World Happiness analysis scripts](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/legacy_jekyll/scripts/world-happiness).
