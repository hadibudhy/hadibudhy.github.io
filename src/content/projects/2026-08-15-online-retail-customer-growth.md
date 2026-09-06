---
title: "Customer Retention: Choosing the Right Repeat-Purchase Window"
date: 2026-09-06
categories: [product analytics]
tags: [retention, cohorts, customer value, experimentation]
excerpt: "A cohort-based retention analysis that replaces lifetime repeat rate with comparable 30, 60, and 90-day windows."
problem: "The retailer wants to protect repeat revenue, but customers who joined earlier have more time to order again, making a lifetime repeat rate an unfair basis for targeting."
result: "Among the common 90-day eligible cohort, 22.2% reordered within 30 days, 37.5% within 60 days, and 47.5% within 90 days. First-order value is associated with later repeat, but it does not prove which offer will work."
featured: true
kind: flagship
published: true
caseId: customer-retention
primaryTrack: product-analytics
secondaryTracks: [analytics-engineering]
displayOrder: 30
evidenceManifest: /data/evidence/customer-retention.json
evidenceVisuals:
  - /images/senior-retail-retention.png
  - /images/senior-retail-segments.png
  - /images/senior-retail-cohorts.png
  - /images/portfolio-retail-cleaning.svg
header:
  teaser: /images/senior-retail-retention.png
---

## The decision

The retention lead needs to decide when to intervene after a customer’s first observed purchase and which customers should enter the first test. The analysis must compare customers with equal time to return.

## Data and customer boundary

The [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online%2Bretail) contains **541,909 transaction rows** from 1 December 2010 to 9 December 2011. After removing cancellations, non-positive quantity or price, and rows without `CustomerID`, the analysis contains **18,532 orders** from **4,338 identifiable customers**.

The file has **9,288 cancellation rows** and **135,080 rows without customer identity**. These exclusions are material because retention cannot be measured without a stable customer denominator.

![UCI Online Retail: 541,909 raw rows narrow to 4,338 identifiable customers after the retention boundary is applied](/images/portfolio-retail-cleaning.svg)

## Metric contract

| Metric | Numerator | Denominator | Eligibility |
|---|---|---|---|
| 30-day repeat rate | Customers with another order 1–30 days after first observed purchase | Customers whose first purchase is at least 30 days before data ends | Identified customers with valid orders |
| 60-day repeat rate | Another order within 60 days | At least 60 observable days | Same |
| 90-day repeat rate | Another order within 90 days | At least 90 observable days | Same |

Day zero is excluded so multiple invoices on the first day do not become retention. “First observed purchase” is precise: the source may begin after a customer’s true first purchase.

## What I investigated

1. How quickly do eligible customers place another order?
2. Does first-order value identify a useful retention segment?
3. Could seasonality or observation-window bias explain the apparent repeat pattern?

## Repeat behaviour builds over time

Among the common cohort of **3,370 customers** with at least 90 days of follow-up:

- **748 of 3,370** reordered within 30 days: **22.2%**.
- **1,264 of 3,370** reordered within 60 days: **37.5%**.
- **1,601 of 3,370** reordered within 90 days: **47.5%**.

![UCI Online Retail common 90-day eligible cohort: repeat purchase rises from 22.2% within 30 days to 47.5% within 90 days](/images/senior-retail-retention.png)

The common cohort makes the three windows comparable. The 30-day window gives the earliest usable intervention point; the 90-day figure remains a lifecycle benchmark.

## Cohort mix changes the 30-day benchmark

Thirty-day repeat differs by first-observed-purchase month. The December 2010 cohort is **34.9%**, while later eligible cohorts range from **14.8% to 30.2%**. The first month is especially vulnerable to left-censoring because customers may have purchased before the dataset began.

![UCI Online Retail first-observed-purchase cohorts: 30-day repeat differs materially by month, so the experiment must balance cohort mix](/images/senior-retail-cohorts.png)

The pooled 22.2% rate remains a useful overall baseline, but it is not enough for a rollout decision. A retention test should block or stratify by first-observed-purchase month and report cohort-adjusted results.

## First-order value is associated with repeat, but it is not a treatment rule

Among customers eligible for 90-day follow-up, repeat rate rises from **39.5%** in the lowest first-order-value quartile to **56.9%** in the highest. The median first order is about **£115** in the lowest group and **£684** in the highest.

![UCI Online Retail 90-day eligible customers: higher first observed order value is associated with higher repeat purchase](/images/senior-retail-segments.png)

This relationship may reflect business buyers, product mix, order purpose, or existing loyalty before the dataset began. It is useful for stratifying a test, not proof that a high-value reward will cause retention.

## Opportunity sizing

The 30-day benchmark leaves **3,169 eligible customers** without a recorded repeat purchase in that window. If a new experience improved the observed 30-day rate by **2 percentage points**, the expected scale would be about **81 additional repeat customers per 4,070 eligible customers**. This is an experiment target, not a forecast of revenue or profit.

## Recommendation

**P0: adopt eligible-window cohorts.** Replace lifetime repeat rate with 30/60/90-day definitions and report the eligible denominator beside every rate.

**P1: test an early second-order experience.** Randomize customers after their first valid order. Test a relevant replenishment or bundle prompt before day 30. Stratify by first-observed-purchase month and first-order-value quartile so treatment balance does not depend on customer mix.

**Primary metric:** 30-day repeat purchase. **Secondary metrics:** time to second order, order value, and 90-day repeat. **Guardrails:** discount cost, returns, cancellations, gross margin, unsubscribes, and customer-support contacts.

**P2: improve identity and economics.** Raise customer-ID coverage and connect product margin, fulfilment cost, marketing exposure, and inventory before scaling.

## Risks and trade-offs

A promotion may move an order forward rather than create an additional order. It may also improve repeat rate while reducing margin. The holdout must remain through 90 days to measure timing, total orders, and contribution.

## Limitations

- First observed purchase may not be the true first purchase.
- The source ends during a partial December and covers one historical retailer.
- Customer identity is missing for a large share of transaction rows.
- Revenue is observed; margin, acquisition source, and campaign exposure are not.

## Key takeaway

Retention becomes decision-ready only when customers have equal time to return. The evidence supports an early second-order test, while the offer and financial impact still require randomized measurement.

## Technical appendix

The reproducible builder pins the workbook hash, cleans transaction grain, creates order and customer tables, applies cohort eligibility, runs segment sensitivity, and publishes aggregate results at `/data/senior/retention.json`.
