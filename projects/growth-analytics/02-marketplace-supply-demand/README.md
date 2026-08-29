# Marketplace supply and demand with incomplete data

## Executive summary

**Decision owner:** Country Manager and Marketplace Operations Lead. **Decision:** where and when should the team test driver incentives? **Primary metric:** fulfilled trips per eligible driver-hour. **Guardrails:** incentive cost per incremental ride, wait time, cancellations, driver earnings, and neighboring-zone displacement.

The official TLC HVFHV dataset records one dispatched trip per row and includes pickup/drop-off time, zones, and license group; the historical API table may omit optional fields when they are null. An official Open Data API slice for 1–7 February 2019 contains **4,965,017 dispatched-trip rows**, with hourly counts ranging from **59,285 at 04:00** to **334,713 at 18:00**. The peak is real completed-trip concentration, not a direct measure of requests or lost rides.

The decision is therefore not “pay more everywhere.” It is to instrument the missing marketplace denominators, identify repeatable shortage windows, and test targeted incentives with geographic or time-based randomization.

## Business problem

Leadership hears that riders wait longer and rides are lost in some areas. The public file shows completed dispatched trips, but it does not show every request, rejected match, or driver online hour. A senior analysis must diagnose what is observable and identify what is still unknown.

## Dataset

The source is the [NYC TLC High Volume FHV data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and the [official HVFHV data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf). TLC states that each row is a trip dispatched by a licensed high-volume FHV base. The API slice used here is the official 2019 HVFHV Open Data table `4p5c-cbgn`, restricted to 1–7 February 2019 and containing 4,965,017 rows. A later 2025 Parquet source is also supported by the downloader, but the throttled endpoint was not treated as complete until fully downloaded.

## Metric framework

```text
Marketplace health
  -> fulfilled trips per eligible driver-hour
    -> completed trips, active drivers, time and geography
  Diagnostics: trip concentration, duration, shared-ride mix, provider mix
  Guardrails: wait, cancellation, earnings, incentive cost, displacement
```

## Analysis

Hourly completed trips rise from **59,285 at 04:00** to **334,713 at 18:00** in the bounded week. This supports peak-window planning. It does not prove that 04:00 has excess supply or that 18:00 has unmet demand, because requests, cancellations, wait time, and online driver-hours are absent from the seven-field public table.

The correct next join is not another descriptive chart. It is an internal event table containing request, match, pickup, cancellation, driver-online, and incentive records at the same zone-time grain. Only then can the team distinguish low demand from poor fulfillment.

## Intervention design

Eligible drivers in a shortage zone-window receive an incremental incentive for completed trips. Randomize at zone-window or switchback level so treatment drivers do not directly contaminate control drivers. Primary metric is fulfilled trips per eligible driver-hour. Guardrails include incentive cost per incremental ride, estimated wait, cancellations, driver earnings, and trips in adjacent zones.

The main marketplace risk is interference: one driver can affect many riders and other drivers. A driver-level A/B test may therefore violate the independence assumption. Geographic cluster, time switchback, or staggered rollout designs are more defensible.

## Decision

Do not authorize a citywide incentive from completed-trip counts alone. **P0:** instrument requests, cancellations, wait, and driver online time. **P1:** run a zone-window switchback test in a repeatable peak. **P2:** add weather, holidays, and transit disruption controls only when they improve the comparison.

## Interview explanation

**30-second explanation:** “I used official TLC HVFHV trip data to map completed-trip concentration by hour and zone. The week had 59,285 trips at 04:00 and 334,713 at 18:00, but I would not call that a supply shortage because completed trips are not total demand. My recommendation is to add request, cancellation, wait, and driver-online denominators, then test incentives by zone-window with displacement and cost guardrails.”

**2-minute explanation:** Explain grain, missing denominators, peak diagnosis, provider and airport segmentation, interference, switchback randomization, and why fulfilled trips per driver-hour is more useful than gross trips.
