---
title: "Online Retail: Finding the Customers Behind Repeat Revenue"
date: 2026-08-15
categories: [customer growth]
tags:
  - customer value
  - retention
  - sales analysis
  - python
excerpt: "A transaction analysis showing where repeat revenue comes from and which markets deserve closer growth attention."
problem: "The retailer had many transactions, but it was not clear which customers and markets created repeat revenue."
result: "After cleaning 541,909 transactions, the analysis found 4,338 identifiable customers and a strong concentration of revenue among the highest-value customers."
featured: false
header:
  teaser: /images/retail-growth-patterns.png
---

## Executive summary

**Business problem:** grow repeat revenue without increasing dependence on one-off orders or a small customer group. **Key findings:** the cleaned data contains 4,338 identifiable customers; the top 10% generate 61.3% of revenue; and the UK contributes about 82% of revenue. **Decision implication:** retention is valuable but concentrated. **Recommended action:** protect high-value customers and validate repeat-purchase tests in nearby European markets.

## Business context

This UK online retailer sold gift products to customers in the UK and overseas. The transaction file contains more than half a million rows, but raw sales volume alone does not show whether growth comes from loyal customers, one-off orders, or a small group of high-value buyers.

That distinction matters. A business that relies heavily on a few customers needs a different growth plan from one with a broad base of repeat buyers.

## Business question

Which customers and markets should the retailer prioritize to grow repeat revenue without relying only on more one-time orders?

## Data used

I first separated completed purchases from cancellations and invalid quantities or prices. I then grouped line items into orders and orders into customers. This made it possible to compare revenue, order frequency, repeat behavior, and country mix using business-level measures instead of raw transaction rows.

## Why it matters

Revenue growth is more resilient when customers return and no single market or customer group carries all the risk. That makes concentration and repeat purchase useful management questions, not just reporting metrics.

## Approach

I remove cancellations and invalid values, group line items into orders, and group orders into customers. The result describes revenue and repeat behavior; it does not measure margin or prove that a retention offer will work.

## Key findings

### Finding 1: Revenue was concentrated among a small customer group

The cleaned data contains **4,338 identifiable customers**, **18,532 orders**, and **£8.91 million in recorded revenue**. Customers with at least two orders made up **65.6% of the customer base**.

The highest-value 10% of customers generated **61.3% of revenue**. This is a concentration risk and an opportunity: keeping a small group of valuable customers engaged could protect a large share of sales, while losing them would have an outsized effect.

![Cleaned UCI Online Retail orders, December 2010–December 2011: Recorded revenue rose into the holiday season while returning orders became a larger share of orders](/images/retail-growth-patterns.png)

### Finding 2: The UK was the core market, but nearby countries added visible opportunity

The UK generated **£7.31 million**, or about **82% of cleaned revenue**. The next markets were the Netherlands, EIRE, Germany, and France. These markets were much smaller than the UK, but they were large enough to support focused tests around product selection, shipping, and repeat-purchase offers.

![Cleaned UCI Online Retail revenue, December 2010–December 2011: The UK generated most revenue, while nearby European markets require validation before expansion](/images/retail-market-opportunity.png)

### Finding 3: Growth became more dependent on returning orders as the period progressed

Returning orders became a much larger part of monthly orders as the customer base matured. Revenue also rose sharply in September, October, and November 2011, with November reaching **£1.16 million**. December is only partially covered in the source data, so it should not be compared with a complete holiday month.

**Business meaning:** The retailer appears to have a useful repeat-purchase pattern, but the value is unevenly distributed. Growth planning should protect the strongest customer relationships while testing whether successful UK offers can travel to nearby markets; the data does not establish market attractiveness.

## Recommendation

1. **Create a high-value customer retention plan.** Track the top customer group separately and test early access, relevant bundles, or service improvements. The data shows where the value is concentrated, but it does not prove which offer will change behavior.
2. **Build country-specific growth tests.** Start with the Netherlands, EIRE, Germany, and France. Compare repeat order rate, shipping cost, and product mix before increasing marketing spend.
3. **Measure returning orders as a core growth metric.** Report new customers, returning customers, orders, and revenue together so higher sales are not mistaken for healthier customer relationships.
4. **Improve cancellation and customer identification fields.** The raw file contains 9,288 cancellation rows and 135,080 rows without a customer ID. Better capture would make retention reporting more complete.

## What internal data would improve the decision

Customer identity coverage, product margin, shipping cost, marketing exposure, inventory, and repeat-purchase history would turn the revenue signals into a contribution-based retention and expansion decision.

## Key takeaway

The retailer did not need more sales data first. It needed a clearer view of customer value. A small group generated most revenue, while the UK remained the foundation and nearby European markets offered the most practical expansion path.

## Decision details

**Decision owner:** Head of Growth. **Decision:** where should retention and market-expansion effort go first? **North-star KPI:** repeat revenue. **Drivers:** identifiable customers, repeat-customer rate, orders per customer, and average order value. **Guardrails:** cancellation rate, customer concentration, and shipping cost, which is not available in this file.

### What is driving the result?

The main result is not simply “sales grew.” The cleaned base contains **4,338 customers**, and the highest-value 10% generate **61.3% of revenue**. The business is therefore exposed to both customer concentration and incomplete customer identification. The UK contributes about **82% of revenue**, so a country-wide average hides the difference between protecting the core market and testing nearby markets.

This is evidence of concentration, not proof that high-value customers will respond to a particular offer. It also cannot separate customer behavior from product mix because margin, inventory, and marketing cost are missing.

### Opportunity scenarios

If a retention test increased revenue from the top 10% customer group by **5%**, the arithmetic opportunity would be about **£273,000** (`£8.91m × 61.3% × 5%`) before cost. That is a scenario, not a forecast. A conservative test should start below this level and compare against a holdout group.

### Prioritized action and measurement

- **P0 — Act now:** create a protected high-value customer cohort and monitor repeat revenue, order frequency, and cancellations monthly.
- **P1 — Test:** run country-specific repeat-purchase offers in the Netherlands, EIRE, Germany, and France against a control group. Measure repeat-order rate and contribution after shipping cost.
- **P2 — Investigate:** improve CustomerID capture and cancellation reason fields before using the portfolio as a complete retention view.

The test succeeds only if repeat revenue rises without increasing cancellations or reducing contribution. Sensitivity checks should repeat the result with the top 5% and top 20% definitions, and exclude the incomplete December 2011 period.

## Technical appendix

The source is the [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online%2Bretail), licensed CC BY 4.0. The raw file covers 2010-12-01 through 2011-12-09. The cleaned analysis removed cancelled invoices, non-positive quantities, non-positive prices, and rows without `CustomerID`. Revenue is `Quantity * UnitPrice`; cost, margin, shipping cost, and marketing spend are not available, so this case study discusses revenue opportunity rather than profit.

**Code and data:** [View the UCI dataset](https://archive.ics.uci.edu/dataset/352/online%2Bretail)
