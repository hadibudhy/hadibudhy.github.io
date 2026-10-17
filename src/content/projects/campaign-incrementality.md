---
title: "Campaign Incrementality: Did Ad Assignment Raise Visits and Conversion?"
date: 2026-08-29
categories: [growth analytics]
tags: [experimentation, causal inference, incrementality, Python]
excerpt: "A randomized advertising analysis that separates additional conversions from customers who would have converted anyway."
problem: "A campaign can increase reported conversions while adding little incremental value if it mainly reaches people who were already likely to act."
result: "In the official Criteo benchmark, the assigned advertising group converted 0.115 percentage points more often than the control group."
featured: true
kind: flagship
published: true
caseId: experiment-metrics
primaryTrack: experimentation-growth
secondaryTracks: [analytics-engineering, product-analytics]
displayOrder: 50
evidenceManifest: /data/evidence/experiment-metrics.json
evidenceVisuals:
  - /images/growth-criteo-itt.png
  - /images/portfolio-campaign-economics.svg
  - /images/portfolio-campaign-f0.svg
---
## Project brief

- **Project:** Estimate the assignment-level conversion difference in the Criteo advertising benchmark.
- **Question:** Did assigning users to advertising change visits and conversions, and what would leaders need before scaling?
- **Built:** Validated intention-to-treat comparisons for visits and conversions, uncertainty intervals, and an exploratory subgroup check.
- **Result:** The assigned-advertising group converted 0.115 percentage points more often. The benchmark has no current campaign cost or contribution data.

## Business question

A campaign can receive credit for conversions from people who would have acted anyway. The growth team needs to know whether assigning users to advertising changed conversion, then whether any added conversions were worth their cost.

## Data and preparation

The source is the [Criteo AI Lab uplift dataset](https://ailab.criteo.com/criteo-uplift-prediction-dataset/), a released benchmark combining randomized advertising tests. It contains **13,979,592 user records**. Its anonymized features cannot be translated into business-defined customer groups, and Criteo warns that the combined, sampled release does not recover an original campaign effect.

The checks cover row count, schema, binary outcomes, control exposure, and sample ratio. The analysis compares assigned groups, even when a treatment user was not exposed to an ad.

## Stakeholder questions

- **What changed after ad assignment?** Conversion rose by 0.115 percentage points. Visits rose by 1.034 points. Both use assigned users as the denominator.
- **How many additional conversions does that represent in the benchmark?** About 115 per 100,000 assigned users.
- **Does the result show the campaign was profitable?** No. The data has no ad cost, margin, conversion value, or later customer value.

## Findings

### Assigned advertising increased conversion in this benchmark

The control group converted at **0.194%**, compared with **0.309%** in the assigned-advertising group. The absolute difference was **0.115 percentage points** (95% confidence interval: **0.108–0.122 points**).

![Criteo randomized benchmark: assigned advertising increased conversion by 0.115 percentage points; the 95% confidence interval is shown](/images/growth-criteo-itt.png)

The comparison uses assignment, so users remain in their randomized group even if they were not exposed to an ad. This supports an intention-to-treat estimate for this benchmark, not a forecast for a current campaign.

### Assignment also increased visits

The assigned-advertising group had a **4.85% visit rate**, compared with **3.82%** in control. The lift was **1.034 percentage points** (95% CI: **1.006–1.063 points**). Visits are an intermediate outcome. They do not establish purchases or profit.

![Criteo randomized benchmark: assignment to advertising increased the visit rate from 3.82% to 4.85%; the 95% confidence interval for lift was 1.006 to 1.063 percentage points](/images/portfolio-campaign-economics.svg)

### The benchmark shows response, not profitability

The measured difference is about **115 additional conversions per 100,000 assigned users** in the released sample. The dataset does not contain ad cost, margin, conversion value, or later customer value, so this result cannot establish profitability.

The benchmark shows movement at both visit and conversion stages. A current campaign still needs its own holdout and contribution data before the business can decide whether to spend more.

### One anonymized feature band is an exploratory lead

A post-hoc check divided feature f0 into four equal-sized bands. The observed absolute lifts were **0.038**, **0.386**, **0.019**, and **0.010 percentage points**. The feature has no business label, and searching multiple segments can surface chance patterns.

![Exploratory Criteo f0 quartiles: observed lifts were 0.038, 0.386, 0.019, and 0.010 percentage points; the largest band is a retest hypothesis, not a targeting rule](/images/portfolio-campaign-f0.svg)

Treat the largest difference as a hypothesis only. A fresh, pre-registered holdout is needed before targeting from it.

## Built

The project includes a streaming analysis, an intention-to-treat calculation, a confidence interval, SQL, and source checks. The subgroup analysis is labeled exploratory.

## Result

The released benchmark supports a positive assignment-level conversion difference. It does not establish the current campaign’s lift, economics, or a segment-level targeting policy.

**Recommendation:** run a randomized holdout in the current campaign, with a pre-registered primary conversion measure, minimum useful effect, sample size, stopping rule, and guardrails. Scale only if measured incremental CPA is below contribution value and the result remains stable under the agreed audience and frequency rules.

**Limitations:** treatment assignment is the causal comparison; exposure is downstream. The benchmark combines and samples experiments, features are anonymized, and current campaign cost, margin, and retention are unavailable. No live campaign or commercial result is included in this analysis.

## Technical appendix

The analysis uses intention-to-treat: each user remains in the group they were assigned to. The source checks include row count, schema, binary outcomes, control exposure, and sample ratio. [Analysis code, SQL, and validation](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/01-campaign-incrementality) document the calculation and source boundary.
