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

## Business question

Can a product team trust the event data enough to decide where to improve the customer journey?

## Why it matters

Funnels look precise even when their definitions are not. If a view, cart, or purchase is counted at the wrong grain, the team can prioritize a problem that the product did not actually have.

## Decision brief

- **Recommendation:** use the event model as a foundation for product questions, but keep event-level volume separate from session-level conversion until identity coverage is reviewed.
- **Evidence:** the public export contains `view`, `cart`, and `purchase` events. The model keeps one row per event, creates a deterministic event key, and records missing session identifiers in a quality mart.
- **Business value:** a shared event grain makes funnel changes reproducible and gives product teams one place to agree on definitions.
- **Main risk:** this is a public electronics browsing sample, not a current product telemetry feed. It does not prove what a live product funnel would do.
- **Next action:** agree on an internal tracking plan, then add freshness, accepted-value, uniqueness, and session-coverage checks before publishing activation metrics.

## What the data represents

The source is the [REES46 Electronics behaviour export](https://data.rees46.com/datasets/electronics-events/electronics-events.csv.gz). It records customer events across a five-month public release. The source file is treated as the event grain: one row represents one recorded event, not one customer or one order.

The source profile is committed in the evidence manifest. It records the publisher description separately from the observed file range because a data contract should describe what was actually loaded.

## Analytics architecture

The pipeline is intentionally small:

`raw.events → stg_rees46_events → int_rees46_ordered_events → fct_product_funnel / mart_event_quality`

- **Raw:** source rows are loaded without business reinterpretation.
- **Staging:** timestamps, identifiers, categories, and prices are typed. A deterministic `event_id` protects the event grain.
- **Intermediate:** identified sessions are ordered with window functions so the next analysis can ask what happened before and after an event.
- **Marts:** daily event counts and session coverage are published separately from quality checks.

The project is runnable with local DuckDB and dbt. The CI seed is small enough to run in a pull request; the source manifest records the full-data evidence boundary.

## What I checked first

1. Are event types limited to the published values?
2. Is the event key unique?
3. Are timestamps and user identifiers present?
4. How much of the source can be tied to a session?
5. Are event counts being mistaken for users or conversions?

## What the evidence shows

### The source is event-rich, but event volume is not a funnel conversion rate

![Observed event mix from the REES46 electronics export](/images/rees46-event-mix.svg)

The export contains many product views and fewer cart and purchase events. That is useful for journey analysis, but the counts are event counts. They should not be presented as a user conversion rate without session-level denominators.

### Data quality belongs beside the metric, not in a hidden notebook

![Event quality checks for identifiers, timestamps, and session coverage](/images/rees46-quality-checks.svg)

The quality mart exposes duplicate-key checks and missing-session rows. This keeps an important boundary visible: rows without a session can still support event-volume reporting, but they should not enter a session funnel silently.

### The model protects the grain that downstream metrics depend on

![Analytics engineering model grain from source event to product funnel mart](/images/rees46-model-grain.svg)

Each layer has one job. This avoids joining event rows to user or session summaries too early, which is a common way to multiply counts.

## Recommendation

**What:** publish a shared event model and metric contract before launching product funnel reporting.

**Where / who:** product, engineering, and analytics teams should agree on event names, required properties, session identity, and the meaning of an activated user.

**Why:** the public evidence shows that event volume and session conversion answer different questions.

**Risk:** a clean model can still encode a weak tracking plan. Good SQL does not repair missing instrumentation.

**Next test:** replay a small known event fixture in CI, compare the resulting marts with expected rows, and monitor source freshness and session coverage in production.

## Measurement plan

For an internal product, I would track event delivery rate, session coverage, funnel step conversion, activation within a defined window, and downstream retention. The primary product metric should be chosen after the team agrees on the user action that represents real value.

## Key takeaway

The first product analytics decision is often a data-model decision. A trustworthy funnel starts by protecting event grain, defining identity, and showing what the source cannot measure.

## Technical appendix

The executable project lives in [`analytics/`](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/analytics). It includes a dbt source, incremental staging model, ordered-session model, funnel mart, quality mart, contracts, and a CI fixture. The public source is not copied into the website or committed to the repository.
