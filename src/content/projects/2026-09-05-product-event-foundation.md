---
title: "Product Events: Building a Funnel the Product Team Can Trust"
date: 2026-09-06
categories: [analytics engineering]
tags: [event tracking, dbt, DuckDB, product analytics]
excerpt: "An event warehouse and ordered product funnel built from 885,129 real browsing events, with duplicate, identity, and session-window controls."
problem: "The product team needs to choose where to improve the shopping journey, but raw event counts can overstate conversion when identity, order, and metric grain are unclear."
result: "After duplicate and identity controls, 40,234 sessions reached cart after a view and 19,977 then reached purchase within a 24-hour step window. The largest measured loss occurs before cart."
featured: true
kind: flagship
published: true
caseId: product-event-foundation
primaryTrack: analytics-engineering
secondaryTracks: [product-analytics]
displayOrder: 10
evidenceManifest: /data/evidence/product-event-foundation.json
evidenceVisuals:
  - /images/senior-product-funnel.png
  - /images/senior-product-categories.png
  - /images/rees46-model-grain.svg
header:
  teaser: /images/senior-product-funnel.png
---

## The decision

The product lead must decide which part of the shopping journey deserves the next discovery and experiment cycle. The analysis first tests whether the event data can support that decision, then identifies where observed sessions leave the ordered journey.

## Decision framework

| Layer | Definition |
|---|---|
| Decision owner | Product lead and instrumentation owner |
| Outcome metric | Ordered view-to-cart conversion within 24 hours of the first view |
| Drivers to investigate | Product information, displayed price, availability, delivery promise, and browsing intent |
| Guardrails | Ordered purchase completion, revenue per eligible session, returns, and page latency |

The public data can locate the largest measured step, but it cannot identify which driver caused the loss. That boundary determines the next measurement and experiment plan.

## What the data can measure

The [REES46 Electronics export](https://data.rees46.com/datasets/electronics-events/electronics-events.csv.gz) contains **885,129 events**, **407,283 users**, and **490,398 raw identified sessions** from 24 September 2020 to 28 February 2021. Each row is a recorded view, cart, or purchase event. Only **165 rows** lack a session identifier.

The source does not contain registration, acquisition channel, experiment assignment, stock availability, or a confirmed order identifier. I therefore describe an ordered shopping funnel, not activation, marketing attribution, or completed revenue.

## Metric contract

| Metric | Definition | Decision use |
|---|---|---|
| Valid identified session | Distinct non-null `user_session` linked to one user; sessions may span more than 24 hours | Funnel denominator |
| View session | Session with at least one view | Entry to the measured journey |
| Ordered cart session | First cart occurs after the first view | Product-interest progression |
| Ordered purchase session | First purchase occurs after a qualifying cart | Measured funnel completion |
| Session purchase rate | Ordered purchase sessions / all identified sessions | Overall journey health |

Rows without a session remain in event-volume reporting but do not enter the funnel denominator. The quality review also found **655 exact duplicate rows**, **214 session IDs linked to more than one user**, and **10,362 sessions spanning more than 24 hours**. Exact duplicates and multi-user sessions are excluded. Long sessions remain in the denominator, but ordered funnel steps must occur within 24 hours of the first view. Events with the same timestamp use source row order as a deterministic tie-breaker.

## Analytics architecture

`raw events → typed staging → ordered session events → funnel and quality marts → evidence JSON → article`

The source is a static export, so staging is a full refresh. A source-file hash plus row number identifies the loaded extract; a separate logical-event key finds exact duplicates. CI tests accepted event types, keys, timestamps, purchase prices, and monotonic funnel counts.

![Analytics engineering model grain from source event to product funnel mart](/images/rees46-model-grain.svg)

## What I investigated

I tested three hypotheses:

1. The largest loss happens before customers show cart intent.
2. Customers who reach cart usually continue to purchase.
3. Category mix can hide different journey patterns.

## The largest measured loss happens before cart

Of **490,184 valid identified sessions**, **488,150** contain a view. Only **40,234** reach cart after a view within 24 hours, an **8.2% view-to-cart rate**. **19,977** then reach purchase after cart, a **49.7% cart-to-purchase rate**. The full ordered path appears in **4.1% of valid identified sessions**.

![REES46 Electronics, September 2020 to February 2021: 490,184 valid sessions narrow to 19,977 ordered view-cart-purchase journeys within 24 hours](/images/senior-product-funnel.png)

The evidence points product discovery toward the view-to-cart step. It does not explain the cause. Price presentation, product fit, stock, shipping information, and browsing intent are competing explanations that require additional properties or experiments.

## Category mix changes the benchmark

Among categories with at least 1,000 view sessions, purchase-event presence varies materially. Camera peripheral sessions show **13.9%**, video-card sessions **10.7%**, and printer sessions **7.4%**. These rates are descriptive because a session can contain several categories and the source does not identify intent or availability.

![REES46 Electronics categories with at least 1,000 view sessions: purchase-event presence differs across large categories](/images/senior-product-categories.png)

This result prevents one company-wide target from becoming an automatic category target. The product team should compare similar categories and add stock, price, and delivery context before assigning causes.

## Recommendation

**P0: improve measurement.** Require product availability, displayed price, delivery promise, page surface, and experiment assignment on view and cart events. Monitor session coverage and event freshness.

**P1: test the main opportunity.** Run a page-level experiment in high-volume categories that simplifies the decision to add an item to cart. Randomize eligible sessions, use ordered view-to-cart conversion as the primary metric, and monitor purchase completion, revenue per eligible session, returns, and page latency.

**P2: investigate category differences.** Review camera, video-card, printer, and cartridge journeys with merchandising and inventory teams. Treat the observed rates as prioritization evidence, not causal effects.

## Measurement plan

Set the test duration and sample size from current eligible-session volume and the smallest useful view-to-cart improvement. Keep assignment at session level, pre-register exclusions, and stop only on the agreed decision rule. A successful change must improve ordered view-to-cart conversion without reducing purchase completion or revenue per eligible session.

## Limitations

- The source is historical public data and does not represent a current product.
- Purchase is an event label, not a reconciled order or payment record.
- Category comparisons may reflect customer and product mix.
- The static source is full-refreshed; an append-only production feed would need a stable producer event ID before incremental loading.

## Key takeaway

The product decision became clear only after the warehouse protected event grain and sequence. The measured opportunity is before cart, while the reason for that loss remains a hypothesis to test.

## Technical appendix

The executable dbt project, event contract, loader, funnel mart, tests, and evidence builder are available in the repository. The aggregate result is published at `/data/senior/product-events.json`; raw user-level events remain outside the website.
