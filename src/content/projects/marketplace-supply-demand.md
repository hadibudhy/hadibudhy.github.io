---
title: "Ride-Hailing Marketplace: Where Pickup Friction Is Concentrated"
date: 2026-09-06
categories: [product analytics]
tags: [marketplace, pickup experience, segmentation, experimentation]
excerpt: "A 20.4-million-trip diagnosis of completed-ride pickup delay by provider, zone, and hour, with clear limits on what public data can prove."
problem: "A country manager is considering driver incentives, but citywide trip volume cannot show where completed riders wait longest or whether incentives would create supply rather than move it."
result: "Pickup friction is concentrated in provider-zone-hour windows. JFK-linked zone 132 appears repeatedly in the longest pickup-delay tail, while the busiest citywide hours are not always the slowest."
featured: true
kind: flagship
published: true
caseId: marketplace-experience
primaryTrack: product-analytics
secondaryTracks: [analytics-engineering, experimentation-growth]
displayOrder: 40
evidenceManifest: /data/evidence/marketplace-experience.json
evidenceVisuals:
  - /images/senior-marketplace-hourly.png
  - /images/senior-marketplace-priority.png
  - /images/portfolio-marketplace-measurement.svg
header:
  teaser: /images/senior-marketplace-hourly.png
---

## The decision

The marketplace lead must decide whether to test more driver supply and, if so, where and when. The public file cannot observe total ride requests, unmatched demand, cancellations, or driver online hours. The decision therefore starts with completed-ride pickup friction and uses it to select an internal experiment.

## Data and metric boundary

The [NYC TLC January 2025 HVFHV file](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) contains **20,405,666 completed trips** from two licensed high-volume providers. The analysis uses **20,404,497 rows** whose `request_datetime` falls inside January 2025; this excludes 1,169 spillover rows at the file boundary. Every analyzed row has a request and pickup time.

I define **completed-trip pickup delay** as `pickup_datetime - request_datetime`. This is a valid operational interval for recorded trips. It is not total passenger wait because the source excludes rides that never completed.

The quality review found **199,788 negative intervals** and **21 intervals above 120 minutes**. Those rows stay visible in quality reporting and are excluded from delay summaries. Request timestamps also cross the file boundary for trips picked up near the start or end of January, so the analysis records the observed timestamp range explicitly.

![NYC TLC public data: completed trips and pickup timestamps are observed, while unmatched requests, cancellations, online supply, and incentive ROI are unavailable](/images/portfolio-marketplace-measurement.svg)

## Metric framework

The decision owner is the marketplace lead. The north-star outcome is fulfilled requests per eligible supply block or driver-hour once internal request and online-time data are available. Public completed trips and pickup delay are diagnostic measures; driver pay and passenger fare are context, not unit economics. Matching quality and driver availability are the main drivers to test, with cost, cancellations, neighbouring-zone wait, and total marketplace rides as guardrails.

| Layer | Metric | Meaning |
|---|---|---|
| Demand served | Completed trips | Recorded fulfilled activity |
| Matching friction | Median and P90 request-to-pickup minutes | Typical and long-tail pickup experience among completed rides |
| Driver economics | Average recorded driver pay | Context, not hourly earnings |
| Passenger economics | Average base fare | Context, not contribution margin |
| Missing internally | Requests, match rate, cancellation, online driver hours | Needed to prove shortage and incremental fulfilment |

## What I investigated

1. Do the busiest hours also have the longest pickup delays?
2. Is friction broad across the city or concentrated by provider, pickup zone, and hour?
3. Which windows are suitable for a targeted supply experiment?

## Busy hours are not automatically the slowest

Completed trips peak at **18:00 with 1.25 million trips**. However, the longest citywide P90 pickup delay occurs at **07:00 at 10.3 minutes**. At 18:00, P90 delay is **7.7 minutes**.

![NYC TLC HVFHV completed trips, January 2025: citywide volume peaks in the evening while the longest pickup-delay tail appears in the morning](/images/senior-marketplace-hourly.png)

This rejects a simple “incentivize the busiest hour” rule. Volume and friction answer different questions.

## Pickup friction is concentrated

Provider-zone-hour segmentation ranks groups by completed-trip P90 delay only after requiring at least **500 monthly trips** and **20 observed daily windows** inside the January request-time window. Airport windows dominate the longest tail. For provider HV0005 at JFK at 00:00, P90 delay is **19.0 minutes** across **3,550 completed trips**; daily P90 exceeded 12 minutes on **17 of 31** observed windows. The same provider and airport at 23:00 shows **18.6 minutes** across **5,157 trips**, with daily P90 above 12 minutes on **25 of 31** observed windows.

![NYC TLC HVFHV completed trips, January 2025: selected provider-zone-hour windows have materially longer P90 pickup delay](/images/senior-marketplace-priority.png)

Airport staging rules, long pickup paths, flight banks, provider operations, and geography are plausible drivers. The public file cannot separate them or show whether riders abandoned before pickup.

## Recommendation

**P0: do not increase incentives citywide.** The citywide peak is not the citywide delay peak, and the public evidence cannot measure unmet demand.

**P1: test a focused airport intervention.** Use JFK zone-hour blocks selected by the published delay and observed-window coverage rule. Compare a driver staging or destination-based incentive with business as usual through a switchback design.

**Primary metric:** fulfilled requests per eligible block or driver-hour using internal data. **Secondary metrics:** match rate, P90 passenger wait, completed rides, driver utilization, and driver earnings. **Guardrails:** incentive cost per incremental ride, passenger price, cancellation, neighbouring-zone wait, airport queue compliance, and total marketplace rides.

**P2: diagnose mechanism before scale.** Add request, dispatch, acceptance, cancellation, online time, driver location, incentive, and flight-arrival data. Determine whether the issue is insufficient supply, airport process, or matching quality.

## Experiment design

Randomize comparable zone-time blocks, not individual drivers, because treated drivers can affect control drivers in the same marketplace. Balance weekday, hour, provider, and flight-volume patterns. Keep nearby zones as displacement monitors. Scale only if the treatment creates net rides or lowers wait at an acceptable incremental cost.

## Limitations

- Every marketplace result is conditional on completed trips.
- Unique active drivers and true supply hours are unavailable at the required grain.
- Provider codes are public identifiers, but operating policies are not observed.
- One month cannot establish seasonality or intervention response.
- Higher delay is consistent with friction; it does not prove a supply shortage.

## Key takeaway

The public data supports a targeted experiment, not a citywide subsidy. The strongest signal is concentrated pickup friction around airport windows, and internal request and supply data must determine whether more incentives create value.

## Technical appendix

DuckDB scans the official 491MB Parquet file, validates timestamps, and builds provider × zone × hour segments without loading the full table into memory. Aggregate evidence is published at `/data/senior/marketplace.json`; trip-level records remain private to the analysis workspace.
