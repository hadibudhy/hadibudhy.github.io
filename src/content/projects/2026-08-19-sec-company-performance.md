---
title: "Company Performance: Explaining Growth Before Calling It Healthy"
date: 2026-08-19
categories: [financial performance]
tags: [financial analysis, revenue, profitability, SEC]
excerpt: "A public-filing analysis that separates reported growth from profitability and turns divergence into management questions."
problem: "Revenue growth can hide margin pressure, while profit growth can be distorted by mix, accounting, or one-off items."
result: "For Microsoft, SEC Company Facts reports FY2023 revenue of $211.9B and net income of $72.4B, rising to $281.7B and $101.8B in FY2025; reported net margin moved from about 34.1% to 36.1%."
featured: false
header:
  teaser: /images/sec-revenue-net-income.png
---

## Executive summary

**Business problem:** determine whether reported growth is also improving profitability.

**Evidence strength:** Medium for the reported company-level trend; low for explaining segment drivers or durable contribution from three annual observations.

**Key findings:** Microsoft’s reported revenue increased about 32.9% from FY2023 to FY2025; net income increased about 40.7%; and net margin improved from approximately 34.1% to 36.1%.

**Decision implication:** the observed result is healthy at the reported-company level, but it does not identify whether growth came from volume, price, mix, acquisitions, or cost control.

**Recommended action:** use the margin improvement as a starting point for segment and cost-driver review, not as proof that every business line improved.

## Business question

**Decision owner:** Finance Leader. **Decision:** where should management invest, control cost, or investigate performance quality? **North-star KPI:** sustainable operating contribution. **Drivers:** revenue growth, gross margin, operating expense, tax, mix, and recurring demand. **Guardrails:** cash flow, customer concentration, and one-off items.

## My role

I owned the public-filing extraction, revenue/net-income comparison, margin calculation, chart, and driver-review recommendation for this independent portfolio case. I did not access Microsoft’s internal segment or operating data.

## Why it matters

Reported growth can look healthy while a segment, product, or cost base weakens. Management needs the driver behind the ratio before changing investment or cost targets.

## Data used

The SEC Company Facts API provides structured filing facts, periods, forms, and filing dates. The Microsoft comparison uses reported annual revenue and net income facts. Revenue rose from **$211.9B to $281.7B**, while net income rose from **$72.4B to $101.8B**. The margin movement is directionally positive, but net income is not the same as operating contribution.

This is evidence of reported improvement, not causal proof. Fiscal periods, amended filings, accounting tags, and restatements must remain visible. The next diagnostic layer is segment revenue, gross margin, operating expense, and cash conversion.

![Microsoft reported results, FY2023–FY2025: Revenue rose from $211.9B to $281.7B while net income rose from $72.4B to $101.8B](/images/sec-revenue-net-income.png)

![Microsoft reported results, FY2023–FY2025: Net margin improved from about 34.1% to 36.1% on a full percentage scale, but segment drivers still need review](/images/sec-net-margin.png)

## Approach

The reported margin improvement is modest—about **2.0 percentage points** over two years—so it is a reason to investigate, not proof of a broad operating transformation. The conservative case is to preserve the FY2025 margin while growth slows; the expected case tests whether the current margin can hold as mix changes; the ambitious case identifies controllable cost or mix drivers that improve contribution without reducing product investment. No incremental profit is claimed because segment costs and intervention effects are not established.

## Key findings

- Reported revenue rose from **$211.9B to $281.7B** and net income from **$72.4B to $101.8B** between FY2023 and FY2025.
- Reported net margin rose from about **34.1% to 36.1%**, calculated as net income divided by revenue; the result is company-level reporting, not a segment diagnosis.
- SEC facts cannot show whether volume, price, mix, or cost control caused the improvement.

## Recommendation

- **P0 — Act now:** monitor revenue growth, net margin, operating expense, and cash flow together.
- **P1 — Test:** investigate one segment or cost category where growth and margin direction diverge.
- **P2 — Investigate:** reconcile SEC facts to the filing statements and notes when tags or periods change.

Success means durable contribution and cash conversion, not one strong annual ratio. Repeat the analysis using filing date, fiscal period, amended filings, and alternative revenue tags as sensitivity checks.

## Key takeaway

Senior financial analysis turns growth into a question about quality and durability. SEC data makes the baseline repeatable; the filing context explains what management can actually control.

## What internal data would improve the decision

Segment revenue, gross margin, customer retention, price and volume, operating costs, cash flow, and one-off items would separate durable performance from accounting or mix effects.

## Technical appendix

Source: [SEC Company Facts](https://www.sec.gov/data-research/sec-api-documentation). Values come from public XBRL filings and can reflect restatements, taxonomy changes, and different fiscal calendars. This is not stock-price analysis or investment advice.
