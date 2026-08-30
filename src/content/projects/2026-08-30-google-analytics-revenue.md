---
title: "Google Merchandise Store: Find Valuable Acquisition Before Buying More Traffic"
date: 2026-08-30
categories: [growth analytics]
tags: [acquisition, revenue, calibration, Google Analytics]
excerpt: "A revenue-quality study that ranks acquisition paths by observed value while keeping session leakage and the historical forecast boundary explicit."
problem: "Marketing needs to decide which acquisition paths deserve more attention, but session volume alone can reward channels that bring many low-value visits."
result: "The public Google Merchandise Store release contains visit-level records, user identifiers, channel and traffic fields, and a revenue target; it supports value-aware prioritization but not a current budget recommendation."
published: true
---

## Business question

Which acquisition paths should receive deeper measurement and testing when the objective is profitable customer value rather than visits?

## Why it matters

Buying traffic against sessions or clicks can increase activity without improving revenue. The commercial decision needs a value-weighted view and a clean separation between what is known at acquisition time and what is only known after the purchase.

## Decision brief

- **Recommendation:** prioritize channels for experimentation using user-level revenue distributions and calibrated holdouts, not attributed session counts.
- **Evidence:** the official competition file defines one row as one Google Merchandise Store visit and provides a string `fullVisitorId` for user identity. The training window is August 2016 through April 2018; the forward-looking test window ends in October 2018.
- **Evidence strength:** Moderate for historical channel and revenue patterns; low for current performance because the source is old and the target is competition-specific.
- **Main risk:** the store, tracking implementation, product catalog, and channel mix have changed. A model can also leak post-session revenue fields.
- **Next test:** use a randomized channel holdout or geo split with incremental revenue, contribution, and new-customer guardrails.

## Role

Role: nested-field preparation, user-level aggregation, temporal train/test design, calibration review, and budget-decision framing. No current Google commercial performance is claimed.

## Data used

The [Google Analytics Customer Revenue Prediction dataset](https://www.kaggle.com/c/ga-customer-revenue-prediction/data?select=train.csv) contains public Google Merchandise Store visit records. The source describes `fullVisitorId`, `channelGrouping`, date, device, geography, traffic source, session identifiers, and nested `totals` and `hits` fields. The target is the log of total revenue per user in a future period.

This is real store traffic, but it is a historical competition release. It is not a live analytics export and the competition terms govern reuse.

## Approach

1. Parse nested JSON fields without converting absent revenue to zero incorrectly.
2. Keep visitor IDs as strings so leading zeros do not collapse users.
3. Aggregate visits to the user-period grain before comparing value.
4. Use a forward time split and compare a simple channel baseline with a calibrated model.
5. Evaluate ranking quality and economic usefulness separately.

## Key findings

## Visual evidence

### Context: the release has separate historical windows

![Google Analytics Customer Revenue Prediction time boundary: training visits, forward test visits, and a competition target period not present in the file](/images/portfolio-google-analytics-window.svg)

The timeline makes it harder to mistake an old competition window for current budget evidence.

### Main finding: value must be aggregated to users

![Conceptual Google Analytics grain: visit-level channel and device fields aggregate to user-period value](/images/portfolio-google-analytics-grain.svg)

This is the denominator needed for a customer-value decision; sessions alone overcount repeat browsers.

### Decision: channel ranking must lead to a holdout

![Conceptual acquisition decision: rank calibrated user value, hold out business-as-usual traffic, and scale only when contribution clears cost](/images/portfolio-google-analytics-holdout.svg)

The design separates a prediction screen from the incremental commercial decision.

### Volume is not a value decision

Channels can bring many visits while contributing little user-level revenue, and a smaller channel can have a heavier tail of valuable users.

**Meaning:** channel share of sessions is an acquisition input, not a budget outcome.

**Why it matters:** the first commercial cut should show sessions, converting users, revenue per eligible user, and concentration side by side.

### User aggregation changes the question

The target is total future revenue per user, not revenue per individual visit.

**Meaning:** treating visits as independent commercial customers overweights repeat browsers.

**Why it matters:** budget and retention decisions need a user denominator and a time boundary.

### Prediction quality is not incremental value

A model can rank historical high-value users without proving that a paid touch caused their purchase.

**Meaning:** targeting is an allocation hypothesis; it is not an experiment.

**Why it matters:** a holdout is still required to estimate incremental revenue and avoid paying for customers who would have purchased anyway.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | Visit-level records include `fullVisitorId`, channel, traffic, device, date, and a nested revenue target | Build a user-period value view |
| Inferred | Acquisition quality should be compared at user level, not by session volume | Shortlist channels for controlled tests |
| Not established | A historical channel difference is current incremental contribution or ROI | Do not set present-day spend from this file |

## Validation record

- **Grain:** one visit in the source; user-period after aggregation.
- **Checks:** IDs remain strings; nested revenue is parsed separately; features are frozen before the target period.
- **Guardrail:** `transactionRevenue` is never used as an input feature, and the evaluation split is forward in time.

## Recommendation

**What:** use the dataset to shortlist acquisition paths for controlled tests, not to set current spend.

**Where / who:** select channels with enough volume, stable tracking, and a measurable user-level value tail.

**Why:** the public data supports value-aware ranking and shows the correct target grain.

**Risk:** channel attribution and historical tracking can be confounded by brand demand, seasonality, and repeat users.

**Next test:** preregister a holdout and compare incremental contribution per exposed user against paid media cost.

## Evidence strength and limitations

Observed channel differences are not causal. The dataset has no randomized marketing assignment, no reliable current cost, no margin, and no durable customer-value outcome beyond the competition target. The future period in the competition is historical now, so this is a method study rather than a forecast.

## Reproducibility

Source and field definitions: [Kaggle competition data page](https://www.kaggle.com/c/ga-customer-revenue-prediction/data?select=train.csv). Dataset boundaries and validation notes are captured in the [expansion validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md).

## Technical appendix

No `transactionRevenue` field is used as an input feature. A production design would freeze features at the acquisition decision timestamp, use a temporal holdout, calibrate predicted value, and compare the model policy with a business-as-usual control.
