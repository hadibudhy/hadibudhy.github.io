---
title: "Financial Metrics: Building a Reconciled Company Performance Mart"
date: 2026-09-05
categories: [analytics engineering]
tags: [financial metrics, SEC data, dimensional modeling, data quality]
excerpt: "A filing-aware metric model that keeps reported periods, units, and restatements visible before financial trends reach a dashboard."
problem: "Finance and product leaders need a consistent view of revenue, net income, and margin, but public filing data contains multiple facts, units, periods, and restated values."
result: "The model treats each reported fact as evidence with source context, then selects a documented annual view instead of assuming that the latest value is automatically comparable."
featured: true
kind: flagship
published: true
caseId: financial-metrics
primaryTrack: analytics-engineering
secondaryTracks: [product-analytics]
displayOrder: 20
evidenceManifest: /data/evidence/financial-metrics.json
evidenceVisuals:
  - /images/sec-revenue-net-income.png
  - /images/sec-net-margin.png
  - /images/portfolio-sec-fact-grain.svg
header:
  teaser: /images/sec-revenue-net-income.png
---
## Problem — Which financial trend can leaders safely compare?

Finance and product leaders need a consistent view of revenue, net income, and margin. SEC filings contain multiple facts, periods, units, and amendments, so a dashboard can show a precise trend built from values that are not comparable.

The decision is whether the annual figures are consistent enough to support an executive trend view. This analysis uses Microsoft’s public filings; it does not represent an internal finance system.

## Hypotheses — What could make a trend misleading?

- **Mixed periods or units could distort growth.** Check that each annual value uses the same fiscal-period rule and compatible units.
- **Revenue growth could hide weaker profitability.** Compare net income and margin alongside revenue.
- **A correct number could still be hard to audit.** Preserve the tag, filing date, and accession context used to select it.

## Analysis — What do the selected facts show?

The source is the [SEC Company Facts API](https://www.sec.gov/edgar/sec-api-documentation). Each record is a reported fact with a tag, unit, fiscal period, filing date, and value. The model keeps this context while selecting an annual view; it does not mix quarterly and annual facts.

### Revenue and net income both rose

![Microsoft reported results, FY2023–FY2025: revenue rose from $211.9 billion to $281.7 billion while net income rose from $72.4 billion to $101.8 billion](/images/sec-revenue-net-income.png)

Both measures increased across the selected fiscal years. Revenue shows scale; net income shows what remained after reported costs. Together they give a fuller performance picture than revenue alone.

### Reported net margin improved slightly

![Microsoft reported net margin rose from 34.1% in FY2023 to 36.1% in FY2025; the vertical scale starts at zero](/images/sec-net-margin.png)

Selected net income divided by selected revenue rose from 34.1% to 36.1%. The full zero-based scale keeps that change in proportion. This company-level result does not explain which products or costs drove it.

### Filing context is part of the metric

![SEC Company Facts grain: each reported value retains its tag, unit, fiscal period, and filing identity for audit](/images/portfolio-sec-fact-grain.svg)

Keeping the source context makes it possible to review why each value was selected instead of relying on an undocumented spreadsheet cell.

## Result — Use a narrow, traceable annual view

The selected annual metrics show revenue rising from $211.9 billion to $281.7 billion and net income from $72.4 billion to $101.8 billion between FY2023 and FY2025; net margin rose from 34.1% to 36.1%. The evidence supports reported company-level trends, not product, customer, or causal operating conclusions.

**Recommendation:** publish a small finance mart with approved metric definitions, period rules, units, and source links. Finance and analytics engineering should reconcile the selected annual values to filings before connecting the mart to planning or dashboards. Add source freshness and reconciliation checks, then extend to quarterly or operating measures only after their definitions are agreed.

**Limitations:** SEC filings do not provide product-level drivers, customer cohorts, live performance, or the company’s internal operating model. Monitor source freshness, unit consistency, period coverage, and reconciliation variance.

## Technical appendix

The evidence manifest records the SEC source, annual period rule, validation checks, and chart hashes. No raw filing payloads or private business data are published.
