---
title: "TransUnion Complaint Monitoring: What Changed in Public Credit-Report Complaints?"
date: 2026-11-07
categories: [customer operations, product analytics]
tags: [CFPB, complaint monitoring, credit reporting, support operations]
excerpt: "A current CFPB snapshot identifies rising complaint volume, concentrated issue themes, and a sharp shift in the company's recorded response categories."
problem: "Which complaint themes and response-code changes should a support operations team investigate first?"
result: "Across 3.44 million CFPB-published complaints from Jan 2025 to Sep 2026, monthly volume rose 89%; three issue categories made up 99.6% of the cohort."
featured: false
published: true
kind: completed
artifactLabel: Customer operations analytics
caseId: cfpb-complaint-monitoring
primaryTrack: product-analytics
secondaryTracks: []
displayOrder: 97
evidenceManifest: /data/evidence/cfpb-complaint-monitoring.json
evidenceVisuals:
  - /images/cfpb-transunion-monthly-volume.png
  - /images/cfpb-transunion-issue-mix.png
  - /images/cfpb-transunion-response-mix.png
header:
  teaser: /images/cfpb-transunion-monthly-volume.png
---

## Project brief

- **Project:** Build a monthly complaint-monitoring screen for TransUnion's credit-reporting complaints published by the CFPB.
- **Question:** Which issue themes dominate the incoming complaint signal, and did the company's recorded response mix change?
- **Built:** A 21-month aggregate snapshot, issue-share analysis, and monitoring visuals from the CFPB's public API.
- **Result:** Published monthly complaint counts rose from **115,860** in January 2025 to **219,349** in September 2026 (**+89.3%**). Three issue categories accounted for **99.6%** of the selected cohort.

## Business question

The CFPB uses complaint and company-response data to monitor consumer issues and response patterns. A financial-services operations team can use the public record as an external signal to decide which complaint themes and process changes to review against its internal case-management data.

This project is a monitoring screen, not a company scorecard. It asks: **what changed in the complaints the CFPB published about TransUnion's credit-reporting product, and what should an operations team verify next?**

## Data and preparation

The [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) is generally updated daily and is freely available for analysis. The snapshot uses **3,440,308** complaints received from **January 2025 through September 2026** for **TransUnion Intermediate Holdings, Inc.** and the product category **Credit reporting or other personal consumer reports**. The API was last updated **November 6, 2026** when accessed.

The CFPB publishes complaints after the company responds, confirms a commercial relationship, or after 15 days, whichever comes first. September is the final included month to allow the public-release lag to mature. The cutoff also excludes the updated complaint-form taxonomy that took effect on October 29, 2026. The study uses monthly API facets for issue, company-coded response, and timely response. It retains only aggregate counts; no complaint rows or narratives are stored.

## Findings

### Public complaint counts increased 89% between the first and last month

The count rose from **115,860** in January 2025 to **219,349** in September 2026. The increase was uneven: the series stepped up in March 2026 and then remained near 213,000–223,000 per month through September.

![Monthly CFPB-published complaints for TransUnion's credit-reporting product from January 2025 through September 2026, with a trailing three-month mean](/images/cfpb-transunion-monthly-volume.png)

This is a count of complaints published by the CFPB, not a rate per customer. The CFPB cautions that the database is not a statistical sample of all consumers' experiences and that company size affects complaint volume.

### Three issue categories account for nearly all records

Across the full period, **59.0%** of complaints were about incorrect report information, **22.5%** about improper use of a report, and **18.1%** about an investigation into an existing problem. Together, these issue categories made up **99.6%** of the cohort.

![Monthly share of TransUnion credit-reporting complaints across the three leading issue categories and all other issues](/images/cfpb-transunion-issue-mix.png)

These are the issue options selected on the CFPB form. They describe the complaint submitted; they do not establish that a company violated a law or that every underlying claim was verified.

### The company-coded response mix shifted sharply in mid-2025

For January–June 2025, **83.2%** of the cohort was coded **Closed with non-monetary relief** and **16.8%** **Closed with explanation**. In July–December 2025, those shares were nearly even. From January–September 2026, **58.6%** were coded **Closed with explanation**, **41.0%** **Closed with non-monetary relief**, and **0.4%** remained **In progress** at the snapshot.

![Monthly share of CFPB complaints by the company's recorded response category](/images/cfpb-transunion-response-mix.png)

The response codes are categorical records, not ratings of satisfaction, resolution quality, or monetary value. The shift is a reason to check internal workflow and coding history; the public data cannot explain its cause.

The CFPB's timely-response field was **Yes** for all **3,440,308** records in this filtered snapshot. It did not distinguish cases in this cohort, so it is not useful as a prioritization signal here.

## Recommendation

Review the March 2026 rise in complaint volume and the July 2025 change in recorded response mix against internal case volumes, process changes, and coding rules. For the monthly support review, prioritize the three dominant issue categories and track complaint counts alongside actual customer and account denominators, first-party case outcomes, and independently measured response times.

## Limitations

The CFPB database does not represent all customers or all company interactions. Complaint counts are not complaint rates because this project has no customer or market-share denominator. The public release process can lag, and the complaint form's product and issue options changed on October 29, 2026. The response categories and timely-response flag do not show whether a problem was resolved well, whether consumers were satisfied, or whether a legal violation occurred. The study does not measure internal support workload, company-wide service performance, causal effects, or consumer harm.

## Technical notes

The script queries one monthly cohort at a time from the [official CFPB complaint API](https://cfpb.github.io/api/ccdb/). Each month is filtered by exact company, product, and receipt-date range; issue, timely-response, and company-response facets must reconcile to the monthly total. The snapshot and artifact hashes are recorded in the [evidence manifest](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/public/data/evidence/cfpb-complaint-monitoring.json). Reproduction steps are in the [project README](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/projects/growth-analytics/06-cfpb-complaint-monitoring/README.md).
