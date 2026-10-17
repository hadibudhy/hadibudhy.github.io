---
title: "Netflix: Catalog Freshness Moved Differently for TV and Movies"
date: 2026-05-03
categories: [product analytics]
tags: [business-strategy, data-analysis, netflix, content-growth]
excerpt: "A catalog analysis that separates TV and movie freshness, movie depth, and metadata coverage."
problem: "A falling freshness measure made it unclear whether Netflix was weakening the catalog or using different roles for shows and movies."
result: "US additions became less same-year fresh overall, while TV freshness rose and movie titles with explicit drama/international or family tags shifted toward older release vintages. These catalog measures do not show viewing or customer outcomes."
featured: false
published: true
caseId: netflix-content-strategy
kind: completed
primaryTrack: product-analytics
displayOrder: 70
evidenceManifest: /data/evidence/netflix-content-strategy.json
evidenceVisuals:
  - /images/netflix-beat01.png
  - /images/netflix-beat03.png
  - /images/netflix-beat05.png
header:
  teaser: /images/netflix-beat01.png
---

## Project brief

- **Project:** Review title freshness, movie depth, and metadata coverage in the Netflix catalog snapshot.
- **Question:** Should leaders use one freshness target for TV shows and movies?
- **Built:** A cleaned catalog analysis with acquisition-lag, explicit genre-tag, and UK metadata measures.
- **Result:** From 2015 to 2021, same-year US TV additions rose from 40.0% to 61.1%. The movie share fell from 84.6% to 14.0%. The data does not measure customer outcomes.

## Business question

From 2015 to 2021, the share of US catalog additions released in the same year fell from **72.2% to 28.1%**. If a team reads that single trend as a decline in catalog quality, it may miss different patterns for TV shows and movies.

The business question is: **should catalog investment be judged by one freshness target, or do TV and movies need separate goals?**

## Data and preparation

The analysis uses 8,807 Netflix titles from the [Movies and TV Shows dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows), with a [Zenodo preservation copy](https://zenodo.org/records/13925131). It calculates acquisition lag as year added minus release year. The freshness and explicit genre-tag comparisons below use US additions; the metadata check uses UK titles grouped by release decade. These are descriptive catalog measures, not business outcomes.

The analysis excludes titles with negative acquisition lag. It compares titles with explicit genre tags and release vintage; genre groups can overlap. The UK metadata check selects titles with UK as the primary country, then counts missing director and cast fields.

## Stakeholder questions

- **Did freshness change in the same way for TV and movies?** No. The same-year share rose for TV and fell for movies.
- **Did the share of older additions change in prespecified genre groups?** Yes. It rose for both explicit drama/international and children-and-family tags.
- **Was the point estimate for UK titles missing director and cast higher in the 2020s?** Yes, but the interval is wide and includes no difference; the data does not confirm a higher rate.

## Findings

### TV additions became fresher while movies shifted toward older titles

The share of US TV additions released in the same year increased from **40.0% in 2015 to 61.1% in 2021**. The same-year share for movies fell from **84.6% to 14.0%**. The combined result therefore hides opposite movements between the two content types.

![US Netflix additions from 2015 to 2021: same-year TV acquisitions rose to 61% while movies fell to 14%](/images/netflix-beat01.png)

This supports separate freshness measures. It does not show that either trend improved viewing or retention.

### Older additions increased in two explicit genre groups

The analysis defines older additions as having an acquisition lag over five years. The share rose from **3.7% (4/108)** to **41.1% (240/584)** among US movie additions tagged `Dramas` or `International Movies`. It rose from **16.4% (10/61)** to **48.0% (129/269)** among titles tagged `Children & Family Movies`. These prespecified genre groups can overlap. They describe the catalog snapshot; they do not prove Netflix's intent.

![US movie additions, 2015–2017 versus 2018–2021: titles tagged drama or international increased 37.4 points in older-release share; children and family titles increased 31.6 points](/images/netflix-beat03.png)

### The recent UK metadata gap is too uncertain for a strong trend claim

Among UK-primary titles, **11 of 86** 2020s releases (12.8%) and **29 of 463** 2010s releases (6.3%) lacked both director and cast fields. The estimated difference is **+6.5 percentage points**, but an approximate 95% Newcombe interval spans **−1.6 to +17.1 points**. The data does not establish that recent titles have a higher missing-field rate. Country is present by definition because it selects the subset. This check does not measure description or genre-tag completeness.

![UK-primary Netflix title metadata by release vintage: 11 of 86 2020s titles and 29 of 463 2010s titles lacked both director and cast; 95% Wilson intervals show uncertainty](/images/netflix-beat05.png)

The point estimate is higher for 2020s releases, but the interval includes no difference. Treat this as a reason to monitor metadata coverage, not a confirmed deterioration. It does not establish why fields are missing or how the gaps affect discovery.

## Built

The work includes source checks, acquisition-lag measures, two explicit and potentially overlapping genre-tag comparisons, and a UK metadata check with uncertainty intervals. The linked workbook and scripts reproduce the analysis.

## Result

The evidence shows opposite freshness trends for TV and movies and higher older-release shares in two explicit movie genre groups. The UK metadata point estimate was higher for 2020s titles, but the uncertainty interval includes no difference. None of these observations proves customer impact or intentional licensing strategy.

- Set separate freshness goals for TV and movies.
- Track deep-library share by explicit genre tags, while allowing overlapping tags and avoiding intent claims.
- Track director, cast, description, and genre-tag completeness by release vintage. Review the metric again when the sample is larger before treating the point-estimate difference as a change.
- For each market, compare those catalog measures with title-level viewing, completion, retention, search, and licensing cost before moving acquisition budget. Treat freshness as a supply-side guardrail, not a success KPI.

## Technical notes

The source snapshot contains 8,807 unique title IDs. Acquisition lag is year added minus release year; negative lags are excluded. The published genre comparison uses explicit `listed_in` tags and can overlap; clustering does not define those groups. The UK metadata measure counts missing director and cast fields among UK-primary titles. Wilson intervals describe each proportion, and a Newcombe interval describes the 2020s-minus-2010s difference.

Regeneration instructions and source hashes are in [`legacy_jekyll/scripts/netflix/README.md`](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/legacy_jekyll/scripts/netflix/README.md). The workbook is downloadable from [Zenodo](https://zenodo.org/records/13925131) and linked to the original [Kaggle dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows).
