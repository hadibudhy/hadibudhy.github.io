---
title: "Financial Metrics: Fixing the Period Logic Before Reporting Growth"
date: 2026-09-06
categories: [analytics engineering]
tags: [SEC data, metric governance, dbt, reconciliation]
excerpt: "A filing-aware finance mart that prevents comparative SEC facts from being assigned to the wrong year and reconciles revenue, earnings, and margin."
problem: "Finance leaders need one trusted annual performance view, but SEC Company Facts repeats values across filings and its filing-year field can differ from the fact's reporting period."
result: "Using period end, annual duration, form, and one coherent accession corrected the year assignment and produced five reconciled annual periods from FY2022 to FY2026."
featured: true
kind: flagship
published: true
caseId: financial-metrics
primaryTrack: analytics-engineering
secondaryTracks: [product-analytics]
displayOrder: 20
evidenceManifest: /data/evidence/financial-metrics.json
evidenceVisuals:
  - /images/senior-sec-performance.png
  - /images/senior-sec-margin.png
  - /images/portfolio-sec-fact-grain.svg
header:
  teaser: /images/senior-sec-performance.png
---

## The decision

The finance lead needs a consistent annual view of revenue, net income, and margin. The analytics decision is which reported fact belongs to each period when the source contains repeated filings, comparative values, several tags, and mixed durations.

## Why the first result was wrong

The [SEC Company Facts API](https://www.sec.gov/edgar/sec-api-documentation) provides structured facts with tags, units, filing dates, forms, accessions, and reporting periods. A first-pass model grouped facts by the source `fy` field. Reconciliation showed that this shifted comparative values into the filing year. For example, a prior-year figure repeated in a newer 10-K could be labelled with the newer filing context.

That is a senior analytics engineering problem: the SQL ran, but the metric meaning was wrong.

## Corrected metric contract

| Rule | Implementation |
|---|---|
| Annual period | 300–380 days between `start` and `end` |
| Fiscal year | Year of the reported `period_end`, not filing context `fy` |
| Filing form | `10-K` or `10-K/A` |
| Coherent context | Revenue and net income come from one selected accession per period |
| Revenue tag | Prefer `Revenues`; use the approved contract-revenue tag when needed |
| Net margin | Selected net income / selected revenue |

The model retains raw filing context in staging, ranks eligible filings deterministically, and publishes only periods with both approved metrics.

![SEC Company Facts: every metric keeps tag, unit, period, form, accession, and filing lineage](/images/portfolio-sec-fact-grain.svg)

## Data quality and reconciliation

The source snapshot contains **81 eligible annual revenue or net-income facts** after unit, form, period, and duration checks. The mart selects five periods, FY2022–FY2026, and confirms one accession per period. Tests require unique fiscal years, non-null metrics, positive revenue, and a calculable margin.

The corrected result was compared with pinned official 10-K documents. The reference file stores the accession, document URL, document hash, and the intended `Consolidated Statements of Income` source table for every period. The verifier confirms the document hash and that the reported values are present in the cited filing. It does not claim to parse the filing table automatically, so the source-table reference remains an explicit audit trail rather than a stronger automated assertion.

## What the corrected mart shows

Revenue increased from **$198.3B in FY2022** to **$331.8B in FY2026**. Net income increased from **$72.7B** to **$133.7B** over the same periods.

![Microsoft reported annual facts, FY2022–FY2026: revenue and net income both increased after filing-aware period selection](/images/senior-sec-performance.png)

Growth was not uniform. Revenue growth slowed to **6.9% in FY2023**, while net income declined **0.5%** and net margin fell from **36.7% to 34.1%**. By FY2026, revenue growth reached **17.8%**, net-income growth **31.3%**, and net margin **40.3%**.

![Microsoft reported annual facts, FY2022–FY2026: net margin recovered from 34.1% to 40.3%](/images/senior-sec-margin.png)

This is a performance signal, not a root-cause claim. Company Facts does not identify which products, prices, customer segments, or cost programmes drove the change.

## Recommendation

**P0: adopt the corrected period contract.** Use period end, duration, form, unit, and accession as required fields for annual metrics. Block publication when reconciliation to the filing exceeds an agreed tolerance.

**P1: add metric ownership.** Finance owns the definition and approved tags; analytics engineering owns lineage, tests, freshness, and backfills. Changes require versioned review.

**P2: connect operating drivers.** Add product revenue, gross margin, headcount, and customer metrics only after their grains and reporting calendars are aligned. Do not infer those drivers from company-level facts.

## Operational plan

Run the source daily, but rebuild the annual mart only when a relevant filing or amendment arrives. Store accession and filing time so restatements are visible. Monitor source freshness, eligible-fact count, duplicate contexts, selected-period count, and reconciliation variance. A backfill must reproduce prior results or record the filing that changed them.

## Limitations

- This is a single-issuer public filing case, not a cross-company benchmark.
- Company Facts is authoritative reporting data but can contain several valid contexts.
- Annual performance does not establish product or management causality.
- FY2026 reflects the source snapshot available at the recorded retrieval date.

## Key takeaway

The most important result was not the growth chart. It was finding and correcting a period-definition error that could have given leaders a confident but wrong trend.

## Technical appendix

The repository includes the Company Facts loader, typed staging model, accession-aware annual mart, dbt tests, CI seed, and aggregate evidence at `/data/senior/financial-metrics.json`.
