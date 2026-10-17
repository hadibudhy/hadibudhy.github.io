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
## Project brief

- **Project:** Build a filing-aware annual performance view for Microsoft.
- **Question:** Which financial trend can leaders compare safely?
- **Built:** A narrow metric model that preserves tags, units, fiscal periods, and filing identity.
- **Result:** From FY2023 to FY2025, revenue rose from $211.9 billion to $281.7 billion. Net margin rose from 34.1% to 36.1%. These are reported company-level trends.

## Business question

Finance and product leaders need a consistent view of revenue, net income, and margin. SEC filings contain multiple facts, periods, units, and amendments, so a dashboard can show a precise trend built from values that are not comparable.

The decision is whether the annual figures are consistent enough to support an executive trend view. This analysis uses Microsoft’s public filings; it does not represent an internal finance system.

## Data and preparation

The source is the [SEC Company Facts API](https://www.sec.gov/edgar/sec-api-documentation). Each fact includes a tag, unit, period, filing date, and value. The selected view uses documented annual facts for Microsoft and keeps quarterly and annual facts separate.

The checks cover unit compatibility, annual period selection, duplicate fact context, margin reconciliation, and source lineage. The evidence manifest records the source hash and period rule.

## Stakeholder questions

- **Did revenue and net income rise together?** Yes. Revenue rose from $211.9 billion to $281.7 billion. Net income rose from $72.4 billion to $101.8 billion.
- **Did reported net margin change?** It rose from 34.1% in FY2023 to 36.1% in FY2025.
- **Can these values explain product performance?** No. The source supports reported company-level trends, not product or customer drivers.

## Findings

### Revenue and net income both rose

![Microsoft reported results, FY2023–FY2025: revenue rose from $211.9 billion to $281.7 billion while net income rose from $72.4 billion to $101.8 billion](/images/sec-revenue-net-income.png)

Both measures increased across the selected fiscal years. Revenue shows scale; net income shows what remained after reported costs. Together they give a fuller performance picture than revenue alone.

### Reported net margin improved slightly

![Microsoft reported net margin rose from 34.1% in FY2023 to 36.1% in FY2025; the vertical scale starts at zero](/images/sec-net-margin.png)

Selected net income divided by selected revenue rose from 34.1% to 36.1%. The full zero-based scale keeps that change in proportion. This company-level result does not explain which products or costs drove it.

### Filing context is part of the metric

![SEC Company Facts grain: each reported value retains its tag, unit, fiscal period, and filing identity for audit](/images/portfolio-sec-fact-grain.svg)

Keeping the source context makes it possible to review why each value was selected instead of relying on an undocumented spreadsheet cell.

### A worked tie-out shows why filing identity stays attached

For FY2024, the selected revenue fact is **$245.122 billion** under `RevenueFromContractWithCustomerExcludingAssessedTax`, for 1 July 2023 through 30 June 2024. The same period and value appear in the FY2024, FY2025, and FY2026 10-K filings (filed 30 July 2024, 30 July 2025, and 29 July 2026). Net income is **$88.136 billion** in those filings, so the reconciled net margin is **35.96%**. The tie-out found no value change; it confirms that repeated comparative facts should not be counted as separate periods.

| Fiscal period | Selected tag | Value | Filing context | Treatment |
|---|---|---:|---|---|
| FY2024 revenue | `RevenueFromContractWithCustomerExcludingAssessedTax` | $245.122B | FY2024, FY2025, and FY2026 10-Ks | Keep one FY2024 period; retain all filing references |
| FY2024 net income | `NetIncomeLoss` | $88.136B | FY2024, FY2025, and FY2026 10-Ks | Reconcile on the same period and unit |
| FY2024 net margin | Derived | 35.96% | $88.136B ÷ $245.122B | Calculate only after period and unit alignment |

## Built

The model preserves each reported fact and its filing context. It selects annual revenue and net income, calculates net margin, and reconciles the ratio to the selected facts.

## Result

The selected annual metrics show revenue rising from $211.9 billion to $281.7 billion and net income from $72.4 billion to $101.8 billion between FY2023 and FY2025; net margin rose from 34.1% to 36.1%. The evidence supports reported company-level trends, not product, customer, or causal operating conclusions.

**Recommendation:** publish a small finance mart with approved metric definitions, period rules, units, and source links. Store filing identity with each fact, deduplicate repeated comparative periods, and reconcile the selected annual values before connecting the mart to planning or dashboards. Alert when a later filing changes a selected historical value; extend to quarterly or operating measures only after definitions are agreed.

**Limitations:** SEC filings do not provide product-level drivers, customer cohorts, live performance, or the company’s internal operating model. Monitor source freshness, unit consistency, period coverage, and reconciliation variance.

## Technical appendix

The evidence manifest records the SEC source, annual period rule, validation checks, and chart hashes. No raw filing payloads or private business data are published.
