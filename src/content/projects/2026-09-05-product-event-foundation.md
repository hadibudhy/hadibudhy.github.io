---
title: "Product Event Data: From Raw Clicks to Trustworthy Funnel Metrics"
date: 2026-09-05
categories: [analytics engineering]
tags: [event tracking, dbt, DuckDB, product analytics]
excerpt: "A small event warehouse that makes product-journey metrics reproducible, testable, and clear about what the source can actually measure."
problem: "Product teams cannot improve a funnel when event names, user identity, and session grain are unclear. The first decision is whether the data is safe to use before anyone ranks conversion opportunities."
result: "The published REES46 Electronics export supports event-level and identified-session metrics, while missing session identifiers on a small set of rows remain visible in the quality mart instead of being silently dropped."
featured: true
kind: flagship
published: true
caseId: product-event-foundation
primaryTrack: analytics-engineering
secondaryTracks: [product-analytics]
displayOrder: 10
evidenceManifest: /data/evidence/product-event-foundation.json
evidenceVisuals:
  - /images/rees46-event-mix.svg
  - /images/rees46-quality-checks.svg
  - /images/rees46-model-grain.svg
header:
  teaser: /images/rees46-event-mix.svg
---
## Problem - Can the team trust its funnel data?

Product teams cannot improve a customer journey if event names, identity, and session grain are unclear. A funnel can look precise while counting repeated events as people or silently excluding activity that cannot be tied to a session.

The decision is whether this public event model is reliable enough to demonstrate a safe measurement foundation. It is not a claim about a live product’s conversion.

## Hypotheses - What could make funnel counts unreliable?

- **Event volume may be mistaken for people or conversion.** Compare event-level counts with identified-session coverage.
- **Missing session IDs may hide part of the journey.** Count those rows explicitly and keep them out of session metrics.
- **Early joins may multiply events.** Preserve one recorded event per row until the session-level model is built.

## Analysis - What did the data checks show?

The source is the [REES46 Electronics behaviour export](https://data.rees46.com/datasets/electronics-events/electronics-events.csv.gz), covering 24 September 2020 through 28 February 2021 in the loaded file. The model separates raw events, typed staging, ordered identified sessions, and event-quality and funnel marts.

### The export contains 885,129 recorded events

![REES46 electronics export: 793,748 views, 54,035 cart events, and 37,346 purchase events; counts are events, not people](/images/rees46-event-mix.svg)

Views dominate the recorded activity, with fewer cart and purchase events. These counts describe events only; a user conversion rate needs a session or user denominator.

### Session coverage is a visible quality check

![REES46 event-quality checks: 165 of 885,129 events have no session identifier and stay outside session-level metrics](/images/rees46-quality-checks.svg)

The 165 rows without session IDs can still support event-volume reporting, but should not be silently included in a session funnel. Keeping them visible shows the size of that boundary.

### The model keeps each measure at its proper grain

![Event-model flow: recorded events are typed and ordered before separate funnel and quality marts are created](/images/rees46-model-grain.svg)

This separation reduces the risk of duplicating events when a downstream analysis joins event, user, or session summaries.

## Result - Approve the measurement foundation, not a product conclusion

The checks support event-level counts and identified-session measures: the source has 885,129 events across view, cart, and purchase, with 165 missing session identifiers. The model makes those rows and the event grain explicit. No live activation or retention effect was measured.

**Recommendation:** agree on an internal tracking plan before publishing funnel metrics. Product, engineering, and analytics should define event names, required properties, session identity, and what counts as an activated user. Add source-freshness, accepted-value, uniqueness, and session-coverage checks.

**Limitations:** this is a public electronics browsing sample, not current product telemetry. It cannot establish what a live product funnel would do. A small CI seed checks model contracts while the evidence manifest records the full-data source boundary.

## Technical appendix

The pipeline keeps each layer focused: raw events → typed staging → ordered identified sessions → separate funnel and event-quality marts. The evidence manifest records the observed file range, event totals, quality checks, and chart hashes.
