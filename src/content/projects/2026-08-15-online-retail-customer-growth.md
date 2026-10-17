---
title: "Online Retail: Customer Sales Are Highly Concentrated"
date: 2026-08-15
categories: [customer growth]
tags:
  - customer value
  - customer concentration
  - sales analysis
  - python
excerpt: "A transaction analysis showing how positive, identifiable sales value is distributed across customers and existing markets."
problem: "The retailer had many invoice lines, but lacked a clear view of how much recorded sales value depended on a small set of identifiable customers or markets."
result: "After documented transaction filters, the top 10% of identifiable customers generated 61.4% of eligible sales value; the top 20% generated 74.6%. These are sales-value shares, not profit or causal effects."
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
  - /images/retail-customer-concentration.png
  - /images/retail-market-opportunity.png
  - /images/portfolio-retail-cleaning.svg
header:
  teaser: /images/retail-growth-patterns.png
---
## Project brief

- **Project:** Measure concentration in eligible sales value across identifiable customers and markets.
- **Question:** How much of recorded sales value sits with a small customer group or one market?
- **Built:** A cleaned invoice-line analysis with customer concentration, monthly totals, country mix, and explicit data-quality boundaries.
- **Result:** The top 10% of 4,338 identifiable customers generated 61.4% of eligible sales value; the UK generated 82.0%. The data does not measure profit or causal offer impact.

## Business question

More than half a million invoice lines show activity, but not how concentrated their eligible sales value is. The decision is which customer and market segments deserve a closer contribution review before allocating retention or expansion budget.

## Data and preparation

The [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online%2Bretail) covers 1 December 2010 to 9 December 2011. Each row is an invoice line. The 541,909-row file includes 135,080 rows without customer IDs.

The analysis removes cancelled invoices, non-positive quantities and prices, and rows without customer IDs. It groups line items by invoice number, then invoices by customer. A **repeat-order customer** has at least two distinct eligible invoice numbers. The 65.6% customer share and 93.1% sales-value share use that definition; neither is a cohort-retention measure. The measures describe positive sales lines from identifiable customers, not net realized sales or profit. The source snapshot and checks are recorded in the evidence manifest.

## Stakeholder questions

- **How concentrated is eligible sales value?** The top 1%, 5%, 10%, and 20% generated 32.0%, 50.4%, 61.4%, and 74.6%.
- **How much value came from repeat-order customers?** Customers with at least two distinct eligible invoice numbers were 65.6% of identifiable customers and generated 93.1% of eligible sales value. This does not measure cohort retention or retention lift.
- **Which market accounts for most eligible sales value?** The UK generated £7.31 million, about 82% of the cleaned total.
- **How large is the identifiable customer base?** The cleaned analysis includes 4,338 customers and 18,532 orders.

## Findings

### The top 20% of customers generated 74.6% of eligible sales value

The cleaned data contains **4,338 identifiable customers**, **18,532 orders**, and **£8.91 million in eligible sales value**. Ranked by customer sales value, the top **1% generated 32.0%**, top **5% 50.4%**, top **10% 61.4%**, and top **20% 74.6%**. Repeat-order customers were **65.6%** of customers and generated **93.1%** of eligible sales value.

![UCI Online Retail customer concentration profile: top 10% of identifiable customers generated 61.4% of eligible sales value and top 20% generated 74.6%, above the equal-share reference](/images/retail-customer-concentration.png)

This is concentration in recorded sales value, not contribution or profit. Use it to prioritize a margin and service-dependency review; do not infer that a retention offer would change customer behavior.

### Monthly sales provide historical context

Eligible sales value varied across the observed months and peaked in November. December contains only nine days, so it is not a full-month comparison.

![UCI Online Retail monthly eligible sales value peaked at £1.16 million in November 2011; December includes only nine days](/images/retail-growth-patterns.png)

### The UK is the main recorded market

The UK generated **£7.31 million**, about **82%** of eligible sales value. The Netherlands, Ireland, Germany, and France were the next largest markets, each far smaller than the UK.

![UCI Online Retail eligible sales value by country: the UK generated £7.31 million, while smaller historical markets are research candidates rather than proven expansion opportunities](/images/retail-market-opportunity.png)

Historical sales identify where the retailer already sold products. They do not measure reachable demand, competition, acquisition cost, shipping cost, or contribution in those countries.

### Customer identity limits the concentration denominator

![UCI Online Retail cleaning boundary: 541,909 raw rows include 135,080 rows without a customer ID; 4,338 customers remain identifiable after cleaning](/images/portfolio-retail-cleaning.svg)

The raw file also contains **9,288 cancellation rows**. The filters keep the sales-value and repeat-order calculations on positive, identifiable transactions. The analysis does not include customers without an ID.

## Built

The analysis validates the invoice-line grain, removes records that cannot support the chosen customer measures, and aggregates eligible sales value by order, customer, and country. It includes four evidence visuals.

## Result

The historical data supports a customer-concentration, repeat-order-customer, and country-mix assessment. It does not measure profit, current demand, or causal retention effects. December is observed only through 9 December and should not be compared with a complete month.

**Recommendation:** prioritize a contribution and service-dependency review for the top-value customer groups, then validate the concentration on a later period. Require margin, order cadence, support cost, and customer-level exposure before changing retention investment. Treat non-UK markets as historical sales locations—not expansion opportunities—until demand, margin, acquisition and shipping costs, competition, and regulation are assessed.

**Limitations:** the source lacks margin, shipping cost, marketing exposure, inventory, and complete customer identity. Better identity coverage and internal contribution data are needed for a commercial decision.

## Technical appendix

Eligible sales value is quantity multiplied by unit price after the stated filters. Customer sales values are summed across eligible invoice lines, ranked, and cumulatively compared with an equal-share reference. The analysis uses a locally validated workbook snapshot retrieved on 20 August 2026. Its evidence manifest records the file hash and data boundary. The source is licensed CC BY 4.0. [Validation workflow](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/supporting-case-validation.md) · [Metric validation and chart code](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/scripts/generate_chart_replacements.py)
