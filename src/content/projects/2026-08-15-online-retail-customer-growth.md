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
featured: true
kind: flagship
published: true
caseId: customer-retention
primaryTrack: product-analytics
secondaryTracks: [analytics-engineering]
displayOrder: 30
evidenceManifest: /data/evidence/customer-retention.json
evidenceVisuals:
  - /images/retail-growth-patterns.png
  - /images/retail-market-opportunity.png
  - /images/portfolio-retail-cleaning.svg
header:
  teaser: /images/retail-growth-patterns.png
---
## Problem — Where can the retailer grow repeat revenue?

The retailer recorded more than half a million transaction rows, but raw sales volume does not show whether growth came from loyal customers, one-time orders, or a small group of high-value buyers. The business question is which customers and markets merit closer attention without mistaking revenue for profit.

## Hypotheses — What patterns could shape the growth decision?

- **Revenue may depend heavily on a small customer group.** Compare customer-level value and repeat ordering.
- **Returning orders may contribute more as the customer base matures.** Compare monthly order mix, while treating the partial December as incomplete.
- **Nearby markets may be candidates for research.** Compare recorded sales by country, but do not infer local demand or profitability from historical revenue alone.

## Analysis — What does the cleaned transaction history show?

The source is the [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online%2Bretail), covering 1 December 2010 through 9 December 2011. The analysis removes cancelled invoices, non-positive quantities and prices, and rows without a customer ID. It groups line items into orders and orders into customers.

### A small customer group accounts for much of recorded revenue

The cleaned data contains **4,338 identifiable customers**, **18,532 orders**, and **£8.91 million in recorded revenue**. Customers with at least two orders made up **65.6%** of the identifiable customer base. The highest-value 10% generated **61.4%** of recorded revenue.

![UCI Online Retail, December 2010–December 2011: recorded revenue rose into the holiday season, while returning orders grew as a share of monthly orders](/images/retail-growth-patterns.png)

The customer concentration makes retention worth testing, but the history does not show whether a particular offer would keep these customers.

### The UK is the main recorded market

The UK generated **£7.31 million**, about **82%** of cleaned revenue. The Netherlands, Ireland, Germany, and France were the next largest markets, each far smaller than the UK.

![UCI Online Retail revenue by country: the UK generated £7.31 million, while smaller historical markets are research candidates rather than proven expansion opportunities](/images/retail-market-opportunity.png)

Historical sales identify where the retailer already sold products. They do not measure reachable demand, competition, acquisition cost, shipping cost, or contribution in those countries.

### Customer identity limits the retention denominator

![UCI Online Retail cleaning boundary: 541,909 raw rows include 135,080 rows without a customer ID; 4,338 customers remain identifiable after cleaning](/images/portfolio-retail-cleaning.svg)

The raw file also contains **9,288 cancellation rows**. Removing cancellations and unidentifiable transactions keeps the revenue and repeat-customer calculations aligned, but means the analysis covers only identifiable customers.

## Result — Protect retention value and research markets before investing

The historical data supports revenue concentration, repeat-order, and country-mix findings. It does not measure profit or prove a causal retention effect. December is only observed through 9 December, so it should not be compared with a complete holiday month.

**Recommendation:** test retention offers with a control group and report new customers, returning customers, orders, and revenue together. Track high-value customers as a segment, but do not assume an offer will change their behavior. Treat the Netherlands, Ireland, Germany, and France as research candidates; validate reachable demand, repeat purchase, margin, acquisition and shipping costs, competition, regulation, and product mix before an expansion pilot.

**Limitations:** the source lacks margin, shipping cost, marketing exposure, inventory, and complete customer identity. Better identity coverage and internal contribution data are needed for a commercial decision.

## Technical appendix

Revenue is quantity multiplied by unit price. The analysis uses a locally validated workbook snapshot retrieved on 20 August 2026; its evidence manifest records the file hash and validation boundary. The source is licensed CC BY 4.0. [Validation workflow](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/supporting-case-validation.md) · [Metric validation and chart code](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/scripts/generate_chart_replacements.py)
