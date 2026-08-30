---
title: "Wikipedia Pageviews: Refresh Durable Interest, Not Just Viral Spikes"
date: 2026-08-30
categories: [product analytics]
tags: [content analytics, pageviews, discovery, time series]
excerpt: "A content-discovery study using Wikimedia’s public pageview API to separate durable reader interest from short-lived traffic spikes."
problem: "An editorial product team needs to decide which pages deserve refresh, related-content links, or better discovery placement when a high view count may only reflect a temporary event."
result: "The public API supports article and project pageview time series by access method and agent type, making persistence and spike-recovery metrics observable without pretending that pageviews are unique readers."
published: true
---

## Business question

Which content topics should receive refresh and discovery work because interest persists across periods, rather than because one event produced a temporary spike?

## Why it matters

Promoting a viral page can waste editorial capacity once interest fades. Ignoring a lower-volume page with steady demand can create a discoverability problem for readers who return to the topic over time.

## Decision brief

- **Recommendation:** rank refresh candidates by sustained pageview floor, recovery after spikes, and mobile/desktop mix; do not rank by one-month volume alone.
- **Evidence:** the [Wikimedia Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/getting-started.html) publishes open pageview and related metrics, with monthly and daily endpoints.
- **Evidence strength:** Moderate for aggregate content demand; low for user-level retention because article pageviews do not identify people.
- **Main risk:** search changes, news events, bots, redirects, and changes in article quality can all move pageviews.
- **Next test:** A/B test related-content links or refresh modules against a holdout and measure downstream article depth, not just pageviews.

## Role

Role: API extraction, time-series quality checks, spike classification, content-prioritization logic, and product measurement design.

## Data used

The [Wikimedia Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/) provides public pageview metrics for Wikimedia projects. The unit is a page/project × time period × access/agent slice. The API documentation defines a pageview as a request that returns a successful page response and explains how spiders, apps, mobile web, and desktop traffic are tagged.

The source measures requests, not unique readers, comprehension, satisfaction, or article quality.

## Approach

1. Pull a fixed historical window and record the request URL and retrieval date.
2. Exclude or separately report automated traffic.
3. Calculate median period views, lower-percentile floor, peak-to-baseline ratio, and recovery time.
4. Compare topics at the same language and access grain.
5. Convert candidate ranks into a controlled discovery or refresh test.

## Key findings

### A spike and a durable audience are different product states

Pages with one unusually high period can look more important than pages with consistent demand.

**Meaning:** peak views measure attention; a sustained floor measures repeat demand at an aggregate level.

**Why it matters:** editorial queues should not let one news event crowd out evergreen content maintenance.

### Access mix is a product signal, not decoration

The API separates desktop, mobile web, app, and automated traffic where available.

**Meaning:** a page that performs on desktop may still have a mobile readability or navigation opportunity.

**Why it matters:** refresh and internal-link decisions should include the access mix so the intervention matches the reader context.

### Pageviews cannot prove reader retention

The public article metric does not identify a person returning to the same page.

**Meaning:** persistence across months is a time-series pattern, not a user-retention rate.

**Why it matters:** a product team needs authenticated or privacy-safe reader cohorts before calling an intervention a retention improvement.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | The API returns page/project views by period, access method, and agent type | Rank content by stable demand and access context |
| Inferred | A sustained lower bound can be more useful for refresh planning than a single peak | Separate evergreen maintenance from spike response |
| Not established | A pageview is a unique returning reader, or a refresh caused more reading | Require first-party reader telemetry and a holdout |

## Validation record

- **Grain:** page/project × period × access × agent.
- **Checks:** fixed endpoint and retrieval window; automated traffic separated; access series not double-counted.
- **Guardrail:** pageview persistence is labeled as aggregate demand, never user retention.

## Recommendation

**What:** create a two-track content queue: spike follow-up for timely pages and durable-interest refresh for pages with a stable view floor.

**Where / who:** use page-level candidates with enough volume for an A/B test, and split decisions by access method.

**Why:** the public data is strong enough to prioritize investigation, not to measure the full reader journey.

**Risk:** event-driven demand and search ranking changes can make historical rankings unstable.

**Next test:** test related-content placement with a holdout and report article-depth and return outcomes from first-party product telemetry.

## Evidence strength and limitations

The analysis is descriptive. It cannot identify unique readers at article level, explain why someone viewed a page, measure content correctness, or estimate causal effects from a pageview time series. Historical comparisons require stable endpoint definitions and a fixed retrieval window.

## Reproducibility

Source documentation and endpoint examples: [Wikimedia Analytics API getting started guide](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/getting-started.html). The portfolio [validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md) records the grain and interpretation boundary.

## Technical appendix

Use the same project, language, period, access, and agent filters when comparing pages. Report the endpoint URL and retrieval date. Do not sum desktop, mobile, and app series if the API already returns an all-access total.
