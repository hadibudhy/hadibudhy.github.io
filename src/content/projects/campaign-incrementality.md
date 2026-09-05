---
title: "Campaign Incrementality: Did Advertising Create New Customers?"
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

## Business question

The growth team needs to know whether paid advertising creates new customers. Reported conversions alone cannot answer that question. Some people would have converted even without seeing the campaign.

## Why it matters

If the business counts every conversion touched by an ad as campaign value, it can spend money on customers who did not need the ad. The right measure is the extra conversions caused by assigning the campaign.

## Decision brief

- **Recommendation:** run the live campaign with a randomized holdout; scale only when incremental CPA is below contribution value.
- **Evidence:** control conversion was **0.194%** and treatment conversion **0.309%**: absolute lift **+0.115 percentage points** (95% CI **+0.108 to +0.122pp**), or about **+59.3% relative**.
- **Potential value:** about **115 extra conversions per 100,000 assigned users** in this benchmark, before economics.
- **Evidence strength:** High for the released randomized comparison; low for transporting the rate to a current campaign.
- **Cost / resource requirement:** Current ad cost and contribution cannot be estimated from this dataset; reserve a randomized holdout and measurement capacity. Break-even CPA is contribution value per incremental conversion, not total attributed conversions.
- **Main risk:** the file has no ad cost, margin, LTV, or current-campaign population.
- **Cost of inaction:** Cannot be estimated from this dataset; the risk is paying for conversions that would have happened anyway.
- **Success / stop rule:** Continue only if incremental CPA stays below contribution value; stop or redesign if the holdout shows no useful lift or the guardrail fails.
- **Next action:** pre-register the holdout, minimum useful effect, sample size, and stopping rule.

## Role

Role: analysis design, streaming validation, intention-to-treat calculation, chart, and business recommendation. No live campaign execution or commercial outcome is included. Decision-owner handoff: a holdout design, break-even CPA rule, and segment hypotheses to retest. [Analysis code, SQL, and validation](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/01-campaign-incrementality) are available for review.

## Data used

The analysis uses the [Criteo AI Lab uplift dataset](https://ailab.criteo.com/criteo-uplift-prediction-dataset/). It combines results from randomized advertising tests. Each row represents one user record and shows whether the user was assigned to advertising, visited, or converted.

The validated release contains **13,979,592 rows**. The user features are anonymized, so they can show different response patterns but cannot be turned into real customer groups. Criteo also warns that the file combines experiments and was sampled in a way that prevents the original campaign effect from being recovered. It is a benchmark for learning, not a forecast for a current campaign.

## Approach

1. Check that the advertising and control groups are present in the expected proportions.
2. Compare conversion and visit rates using the group each user was assigned to.
3. Measure the extra response in the advertising group.
4. Explore whether response differs across anonymized user features.
5. Define the information a real campaign needs before the business spends more.

## Key findings

### The advertising group converted more often

The advertising group converted at **0.309%**. The control group converted at **0.194%**. The difference was **0.115 percentage points**, with a 95% confidence range from **0.108 to 0.122 percentage points**. This is the intention-to-treat difference within the released benchmark; it is not a forecast for a current campaign.

![Criteo randomized advertising benchmark: assigned advertising increased conversion by 0.115 percentage points, with the 95% confidence range shown](/images/growth-criteo-itt.png)

The same pattern appeared in visits. The difference was **1.034 percentage points**, with a 95% confidence range from **1.006 to 1.063 percentage points**.

**Business meaning:** the released benchmark shows a clear difference between assigning users to advertising and holding them out. It does not tell us that a current campaign will produce the same result.

### The headline rate is not the same as profitable growth

The benchmark difference is about **115 extra conversions per 100,000 assigned users in this released sample**. That number explains the experiment. It cannot calculate current campaign profit because the file has no ad cost, conversion value, margin, or later customer value.

**Business meaning:** statistical confidence tells us that the benchmark difference is unlikely to be random noise. It does not tell us whether the campaign earns more than it costs.

The practical launch threshold is explicit: scale only when incremental CPA is below contribution value after ad cost, with the holdout result stable across the pre-specified audience and frequency guardrails.

## Visual evidence

### Main finding: the benchmark’s lift is statistically clear but economically incomplete

![Criteo randomized benchmark: 0.194% control conversion, 0.309% treatment conversion, +0.115 percentage-point lift, and 115 extra conversions per 100,000 assigned users](/images/portfolio-campaign-economics.svg)

The visual keeps the lift and its economic boundary in the same frame.

### Decision: retain a randomized holdout and an economic stop rule

![Conceptual campaign holdout: assign treatment or holdout, measure incremental conversion, and scale only when incremental CPA is below contribution](/images/portfolio-campaign-holdout.svg)

This makes the rollout recommendation operational.

## Recommendation

**What:** Run the current campaign with a randomized holdout and measure extra conversions, not only attributed conversions.

**Where / who:** Start with an audience definition the business can explain and reach. Use anonymized feature bands only as hypotheses for the next test.

**Why:** The benchmark shows that assignment can change conversion, but response is not even across users.

**Risk:** The benchmark's effect cannot be transported to a current campaign, and targeting the wrong group could reduce reach or increase acquisition cost.

**Next test:** Compare broad targeting with uplift-based targeting. Set the minimum useful effect, sample size, stopping rule, and multiple-segment rule before launch.

**Decision status:** Completed benchmark analysis; current-campaign holdout and commercial outcome not measured.

## What internal data would improve the decision

A complete decision needs ad spend, contribution margin, conversion value, customer identity, channel, frequency, and later retention. Incremental CPA and incremental return can then be calculated by a business-defined audience. Scale remains conditional on incremental CPA staying below contribution value and customer-experience guardrails remaining healthy.

## Key takeaway

More reported conversions do not automatically mean profitable advertising. The important decision is to measure the conversions created by the campaign, then spend more only where a current holdout shows that the extra customers are worth the cost.

## Technical appendix

The primary analysis uses intention-to-treat. In plain language, each user stays in the group they were assigned to, even if the ad was not actually shown. This protects the fairness of the randomized comparison. [Analysis code, SQL, and validation](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/01-campaign-incrementality) are available for review.

### Exploratory subgroup check

![Criteo exploratory f0 quartiles: absolute conversion lift was 0.038, 0.386, 0.019, and 0.010 percentage points across the four bands](/images/portfolio-campaign-f0.svg)

An exploratory check divided the complete `f0` feature into four equal-sized bands. The second band had the largest difference, **0.386 percentage points**; the other bands were **0.038**, **0.019**, and **0.010 percentage points**. These are not real customer personas. The feature has no business label and the split was chosen for exploration, so a new campaign should retest any targeting hypothesis in a holdout.

| Exploratory group | Extra conversion rate | Interpretation |
|---|---:|---|
| `f0` lowest quarter | +0.038pp | Hypothesis only |
| `f0` second quarter | +0.386pp | Retest in a new holdout |
| `f0` third quarter | +0.019pp | Hypothesis only |
| `f0` highest quarter | +0.010pp | Hypothesis only |
