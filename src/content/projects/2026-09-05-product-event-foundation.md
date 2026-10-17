---
title: "Product Event Data: What a Session Funnel Can and Cannot Measure"
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
  - /images/rees46-session-funnel.svg
  - /images/rees46-model-grain.svg
header:
  teaser: /images/rees46-event-mix.svg
---
## Project brief

- **Project:** Build and check an event model for a public electronics browsing sample.
- **Question:** Which funnel measures can the team trust at event and session grain?
- **Built:** A staged event model with separate session, funnel, and quality outputs.
- **Result:** The file contains 490,633 user-session pairs. Of these, 20,699 (4.2%) contain view, then cart, then purchase events. This is an event sequence, not a verified transaction rate.

## Business question

Product teams cannot improve a customer journey if event names, identity, and session grain are unclear. A funnel can look precise while counting repeated events as people or silently excluding activity that cannot be tied to a session.

The decision is whether this public event model is reliable enough to demonstrate a safe measurement foundation. It is not a claim about a live product’s conversion.

## Data and preparation

The [REES46 Electronics behaviour export](https://data.rees46.com/datasets/electronics-events/electronics-events.csv.gz) covers 24 September 2020 to 28 February 2021 in the loaded file. Each row is one recorded event. Event types are view, cart, and purchase.

The model checks event keys, event types, timestamps, and session coverage. It preserves the 165 rows with missing session IDs in the quality output and excludes them from session metrics.

## Stakeholder questions

- **How many events appear in each funnel stage?** The file has 793,748 views, 54,035 cart events, and 37,346 purchase events.
- **How many events lack session IDs?** 165 of 885,129 rows lack a session ID.
- **How is a session identified?** By the user ID and session ID pair; 214 raw session IDs are associated with more than one user ID.
- **How many user-session pairs contain the ordered view → cart → purchase sequence?** 20,699 of 490,633 (4.2%).
- **Can that be read as a verified purchase conversion rate?** No. It is a sequence of recorded event types, not a confirmed order or live product funnel.

## Findings

### Only 4.2% of user-session pairs contain a full recorded event sequence

The model finds **490,633 user-session pairs**. Of these, **488,586** include a view, **41,232** include a cart event after a view, and **20,699** include a purchase event after that cart. That is **4.2%** of pairs for the full sequence, and **50.2%** from view-cart to purchase-event. These counts use the composite user-session grain, not raw event rows.

![REES46 ordered user-session funnel: 20,699 of 490,633 user-session pairs contain view, then cart, then purchase events; the sequence is not verified order conversion](/images/rees46-session-funnel.svg)

The event mix supplies context. It counts records, not unique users or sessions.

![REES46 electronics export: 793,748 views, 54,035 cart events, and 37,346 purchase events; counts are event rows, not people](/images/rees46-event-mix.svg)

Views dominate the recorded activity, with fewer cart and purchase events. These counts describe events only; a user conversion rate needs a session or user denominator.

### Session coverage is a visible quality check

![REES46 event-quality checks: 165 of 885,129 events have no session identifier and stay outside session-level metrics](/images/rees46-quality-checks.svg)

The 165 rows without session IDs can still support event-volume reporting, but should not be silently included in a session funnel. Keeping them visible shows the size of that boundary.

### The model keeps each measure at its proper grain

![Event-model flow: recorded events are typed and ordered before separate funnel and quality marts are created](/images/rees46-model-grain.svg)

This separation reduces the risk of duplicating events when a downstream analysis joins event, user, or session summaries.

## Built

The pipeline has raw events, typed staging, ordered identified sessions, and separate funnel and quality outputs. A small CI fixture checks model contracts. The evidence manifest records checks on the full source file.

## Result

The checks support event-level counts and an ordered funnel at the user-session pair grain: 20,699 of 490,633 pairs contain view, then cart, then purchase events. Another 165 event rows have no session ID and remain visible outside session measures. The export does not verify that a purchase event represents a completed order. No live activation or retention effect was measured.

**Recommendation:** use the user-session pair as the session grain, document the order of view, cart, and purchase events, and keep the 165 unassigned event rows visible. Before publishing a live funnel, product, engineering, and analytics should agree on event names, required properties, session identity, and what counts as an activated user. Add source-freshness, accepted-value, uniqueness, and session-coverage checks.

**Limitations:** this is a public electronics browsing sample, not current product telemetry. It cannot establish what a live product funnel would do. A small CI seed checks model contracts while the evidence manifest records the full-data source boundary.

## Technical appendix

The pipeline keeps each layer focused: raw events → typed staging → ordered user-session pairs → separate funnel and quality marts. The composite key combines user ID and session ID because 214 raw session IDs map to multiple users. Sequence order is event time, then source row for timestamp ties. A test checks that each composite key maps to one user and one raw session ID.
