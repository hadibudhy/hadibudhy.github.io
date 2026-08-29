---
title: "Campaign Incrementality: Did Advertising Create New Customers?"
date: 2026-08-30
categories: [growth analytics]
tags: [experimentation, causal inference, incrementality, Python]
excerpt: "A randomized advertising analysis that separates additional conversions from customers who would have converted anyway."
problem: "A campaign can increase reported conversions while adding little incremental value if it mainly reaches people who were already likely to act."
result: "In the official Criteo benchmark, the assigned advertising group converted 0.115 percentage points more often than the control group."
featured: true
---

## The Business Question

The growth team needs to know whether paid advertising creates new customers. Reported conversions alone cannot answer that question. Some people would have converted even without seeing the campaign.

## Why This Matters

If the business counts every conversion touched by an ad as campaign value, it can spend money on customers who did not need the ad. The right measure is the extra conversions caused by assigning the campaign.

## What Data I Used

I used the [Criteo AI Lab uplift dataset](https://ailab.criteo.com/criteo-uplift-prediction-dataset/). It combines results from randomized advertising tests. Each row represents one user record and shows whether the user was assigned to advertising, visited, or converted.

The validated release contains **13,979,592 rows**. The user features are anonymized, so they can show different response patterns but cannot be turned into real customer groups. Criteo also warns that the file combines experiments and was sampled in a way that prevents the original campaign effect from being recovered. It is a benchmark for learning, not a forecast for a current campaign.

## How I Approached It

1. Check that the advertising and control groups are present in the expected proportions.
2. Compare conversion and visit rates using the group each user was assigned to.
3. Measure the extra response in the advertising group.
4. Explore whether response differs across anonymized user features.
5. Define the information a real campaign needs before the business spends more.

## What I Found

### The advertising group converted more often

The advertising group converted at **0.309%**. The control group converted at **0.194%**. The difference was **0.115 percentage points**, with a 95% confidence range from **0.108 to 0.122 percentage points**.

![Criteo randomized advertising benchmark: assigned advertising increased conversion by 0.115 percentage points, with the 95% confidence range shown](/images/growth-criteo-itt.png)

The same pattern appeared in visits. The difference was **1.034 percentage points**, with a 95% confidence range from **1.006 to 1.063 percentage points**.

**Business meaning:** the released benchmark shows a clear difference between assigning users to advertising and holding them out. It does not tell us that a current campaign will produce the same result.

### The headline rate is not the same as profitable growth

The benchmark difference is about **115 extra conversions per 100,000 assigned users in this released sample**. That number explains the experiment. It cannot calculate current campaign profit because the file has no ad cost, conversion value, margin, or later customer value.

**Business meaning:** statistical confidence tells us that the benchmark difference is unlikely to be random noise. It does not tell us whether the campaign earns more than it costs.

### Response was uneven across the anonymized audience

I divided the complete `f0` feature into four equal-sized bands as an exploratory check. The second band had the largest difference, **0.386 percentage points**. The other bands were **0.038**, **0.019**, and **0.010 percentage points**.

| Exploratory group | Extra conversion rate | What the business should do |
|---|---:|---|
| `f0` lowest quarter | +0.038pp | Do not target from this benchmark alone |
| `f0` second quarter | +0.386pp | Retest in a new holdout |
| `f0` third quarter | +0.019pp | Do not target from this benchmark alone |
| `f0` highest quarter | +0.010pp | Do not target from this benchmark alone |

These are not real customer personas. The feature has no business label and the split was chosen for exploration. The useful conclusion is that response may differ across users, so a real campaign should test targeting rather than assume everyone has the same value.

## What I Recommend

**What:** Run the current campaign with a randomized holdout and measure extra conversions, not only attributed conversions.

**Where / who:** Start with an audience definition the business can explain and reach. Use anonymized feature bands only as hypotheses for the next test.

**Why:** The benchmark shows that assignment can change conversion, but response is not even across users.

**Risk:** The benchmark's effect cannot be transported to a current campaign, and targeting the wrong group could reduce reach or increase acquisition cost.

**Next test:** Compare broad targeting with uplift-based targeting. Set the minimum useful effect, sample size, stopping rule, and multiple-segment rule before launch.

## What I Would Do With Internal Data

I would add ad spend, contribution margin, conversion value, customer identity, channel, frequency, and later retention. Then I would calculate incremental CPA and incremental return by a business-defined audience. The campaign would scale only when incremental CPA stays below contribution value and customer-experience guardrails remain healthy.

## Key Takeaway

More reported conversions do not automatically mean profitable advertising. The important decision is to measure the conversions created by the campaign, then spend more only where a current holdout shows that the extra customers are worth the cost.

## Interview Versions

**30 seconds:** “I used a randomized Criteo advertising benchmark to separate campaign response from conversions that would have happened anyway. The assigned advertising group converted 0.115 percentage points more often, with a tight confidence range. I would not call that a current campaign forecast or a profit result because cost and contribution are missing. I would run a current holdout and use incremental CPA as the rollout gate.”

**2 minutes:** Explain the business problem, assignment-based comparison, absolute lift, confidence range, uneven response across anonymized bands, and why current cost and contribution data are needed before scaling.

**5 minutes:** Explain the sample-ratio check, intention-to-treat estimate, why exposure is downstream, exploratory segment testing, multiple comparisons, holdout design, MDE, stopping rules, and the difference between attribution, incrementality, and profit.

## Technical Note

The primary analysis uses intention-to-treat. In plain language, each user stays in the group they were assigned to, even if the ad was not actually shown. This protects the fairness of the randomized comparison. The full validation and SQL live under `projects/growth-analytics/01-campaign-incrementality`.
