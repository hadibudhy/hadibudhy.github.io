---
title: "What 14 Years of Happiness Data Really Shows"
date: 2026-05-10
categories: product analytics
tags:
  - data-analysis
  - world-happiness-report
  - python
  - exploratory-analysis
excerpt: "A long-term view of national happiness that separates real trends from changes in the countries being measured."
problem: "Single-year rankings obscure how happiness changes across countries and over time."
result: "The same 129 countries were compared across 14 years, revealing the biggest gains, losses, and relationships."
featured: false
header:
  teaser: /images/happiness-beat01.png
---

## Executive summary

**Business problem:** yearly rankings hide long-term progress and widening gaps. **Decision:** where should a development or policy team focus attention? **Key finding:** the balanced 129-country average rose from 5.47 to 5.74, but the gap between the highest and lowest scores widened. **Recommended action:** track distributional progress and treat social support, income, and health as connected factors rather than causal levers.

## Business context

The World Happiness Report is often discussed as a yearly ranking: Finland is near the top, Afghanistan is near the bottom, and the Nordic countries often lead.

Rankings are easy to share, but they can hide the longer story. A country may appear to move up or down because the set of countries being measured has changed. A multi-year view is more useful for understanding progress, risk, and where conditions are improving or deteriorating.

## Business question

How has national happiness changed over 14 years, which countries are moving most, and which conditions are most closely connected with higher scores?

## How I approached it

The source covers 168 countries from 2011 to 2025, with no measurement for 2013. I focused on the 129 countries that appear in all 14 measured years. This balanced group makes year-to-year comparisons more consistent because the same countries are being compared each time.

The happiness score is a self-reported 0-to-10 life evaluation. It measures how people rate their lives overall, not their mood at a particular moment.

## Finding 1: The global average rose, even through COVID

The average score for the balanced group increased from **5.47 in 2011 to 5.74 in 2025**, a gain of 0.26 points.

The average rose slightly in 2020, dipped in 2021 and 2022, then recovered by 2023 and reached a 14-year high in 2025.

![Balanced panel of 129 countries, 2011–2025: Average happiness rose and recovered after the 2021–2022 dip](/images/happiness-beat01.png)

**What this means:** The data does not show a long global happiness collapse during COVID. That does not remove the pain, loss, or anxiety caused by the pandemic. It shows that an overall life evaluation can behave differently from short-term mood or daily stress.

## Finding 2: Eastern Europe showed the strongest gains

Seven of the eight largest risers were post-Soviet or Balkan countries. China was the exception.

| Country | 2011 Score | 2025 Score | Change |
|---------|-----------|-----------|--------|
| Serbia | 4.56 | 6.69 | +2.13 |
| Bulgaria | 3.89 | 5.70 | +1.81 |
| Georgia | 3.89 | 5.52 | +1.63 |
| Latvia | 4.76 | 6.37 | +1.60 |
| Bosnia and Herzegovina | 4.86 | 6.38 | +1.52 |
| Kosovo | 5.42 | 6.91 | +1.49 |
| Romania | 5.18 | 6.63 | +1.45 |
| China | 4.68 | 6.07 | +1.39 |

These countries started from relatively low scores. Their gains are consistent with improving living standards and institutions, although this analysis does not prove that one specific policy caused the improvement.

The largest decline was in Afghanistan: **-2.81 points**, from 4.26 in 2011 to 1.45 in 2025. Lebanon, Malawi, and Jordan also experienced large falls. Conflict, economic collapse, and governance problems are important context for these results.

![Balanced panel of 129 countries, 2011–2025: The largest risers and fallers show how quickly national scores can change](/images/happiness-beat02.png)

## Finding 3: The gap is not about money alone

In 2025, the top 10 countries averaged **7.33**, while the bottom 10 averaged **3.36**. That is a four-point difference on a 10-point scale.

The largest gaps between the groups were:

- **GDP per person:** 0.83 points.
- **Social support:** 0.82 points.
- **Life expectancy:** 0.62 points.

![Top 10 versus bottom 10 countries in 2025: The largest happiness-score differences include income, social support, and health](/images/happiness-beat03.png)

**Business meaning:** Economic resources matter, but they are not the whole story. Access to support and the ability to live a healthy life are nearly as important in the group comparison.

## Finding 4: Social support, income, and health had the strongest relationships with happiness

Using factor data from 2019 to 2025, the strongest relationships with the final happiness score were:

- Social support: **r = 0.71**
- GDP per person: **r = 0.68**
- Life expectancy: **r = 0.66**

These factors are also related to each other. Wealthier countries often have better healthcare and stronger safety nets, so this analysis cannot separate the individual effect of each factor.

Generosity had almost no relationship with the national happiness score (**r = 0.03**). This does not mean generosity has no value for individuals. It means charitable giving alone did not explain differences between countries in this dataset.

![Countries measured from 2019–2025: Social support, income, and health showed the strongest associations with happiness](/images/happiness-beat04.png)

## Finding 5: The gap between countries widened

The range between the highest and lowest country scores grew from 4.8 points in 2011 to 6.3 points in 2025, an increase of 31%.

So the global average rose, but the countries at the bottom did not keep pace with the countries at the top. That is a more important signal than the average alone because it shows that progress was uneven.

![Balanced panel of 129 countries, 2011–2025: The gap between the highest and lowest country scores widened over time](/images/happiness-drivers-inequality.png)

## Recommendations

1. **Track progress over time, not only rankings.** A single yearly position can hide meaningful improvement or decline.
2. **Look beyond income.** Social support and health deserve equal attention when evaluating wellbeing and development.
3. **Focus on the bottom of the distribution.** A rising average does not mean that the countries with the lowest scores are improving at the same pace.

## Takeaway

National happiness improved on average over these 14 years, but progress was uneven. The strongest relationships were linked to social support, income, and health, while generosity alone did not explain country-level differences.

## Supporting technical detail

The analysis uses a balanced panel of 129 countries across all 14 measured years. Factor data is available from 2019 onward, and all factors were checked against the reported happiness score with a maximum rounding difference of 0.003. The results use a self-reported life-evaluation scale, not an objective measure of wellbeing.

**Code and data:** [View the analysis scripts](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/legacy_jekyll/scripts/world-happiness)
