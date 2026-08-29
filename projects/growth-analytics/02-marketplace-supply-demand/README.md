# Marketplace supply and demand with incomplete data

## Executive summary

**Decision owner:** Country Manager and Marketplace Operations Lead. **Decision:** where and when should the team test driver incentives? **Primary metric:** request fulfillment rate. **Supply diagnostic:** recorded trips per eligible online driver-hour. **Economic metric:** incremental fulfilled trips per incentive dollar. **Guardrails:** wait time, cancellations, driver earnings, and neighboring-zone displacement.

The official TLC HVFHV dataset records one submitted dispatched-trip row and includes pickup/drop-off time, zones, and license group; the historical API table may omit optional fields when they are null. An official Open Data API slice for 1–7 February 2019 contains **4,965,017 recorded trip rows**, with hourly counts ranging from **59,285 at 04:00** to **334,713 at 18:00**. The peak is recorded-trip concentration, not a direct measure of requests or lost rides.

The decision is therefore not “pay more everywhere.” It is to instrument the missing marketplace denominators, identify repeatable shortage windows, and test targeted incentives with geographic or time-based randomization.

## Business problem

Leadership hears that riders wait longer and rides are lost in some areas. The public file shows completed dispatched trips, but it does not show every request, rejected match, or driver online hour. A senior analysis must diagnose what is observable and identify what is still unknown.

## Dataset

The source is the [NYC TLC High Volume FHV data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and the [official HVFHV data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf). TLC states that each row is a trip dispatched by a licensed high-volume FHV base. The API slice used here is the official 2019 HVFHV Open Data table `4p5c-cbgn`, restricted to 1–7 February 2019 and containing 4,965,017 rows. A later 2025 Parquet source is also supported by the downloader, but the throttled endpoint was not treated as complete until fully downloaded.

## Metric framework

```text
Marketplace health
  -> request fulfillment rate
    -> recorded trips, active drivers, time and geography
  Diagnostics: trip concentration, duration, shared-ride mix, provider mix
  Guardrails: wait, cancellation, earnings, incentive cost, displacement
```

## Analysis

Hourly recorded trips rise from **59,285 at 04:00** to **334,713 at 18:00** in the bounded week. This describes a peak in submitted trip records. It does not prove that 04:00 has excess supply or that 18:00 has unmet demand, because requests, cancellations, wait time, and online driver-hours are absent from the historical public table.

TLC's official monthly report adds a useful, but different, supply view. In the 12-month averages for 2024 versus 2025, reported trips per day rose from **654,410 to 667,537 (+2.0%)**, while unique drivers were nearly flat (**83,399 to 83,299**) and average hours per driver changed from **6.35 to 6.38**. This suggests more recorded activity without a comparable increase in observed driver coverage, but it still does not identify hourly online supply or unmet demand.

![TLC monthly High Volume FHV reports, 2024–2025: reported trips increased while the observed driver count stayed broadly flat](/images/growth-hvf-monthly-supply.png)

The correct next join is not another descriptive chart. It is an internal event table containing request, match, pickup, cancellation, driver-online, and incentive records at the same zone-time grain. Only then can the team distinguish low demand from poor fulfillment. Recorded trips per driver-hour is a supply diagnostic, not the primary customer outcome.

## Intervention design

Eligible drivers in a shortage zone-window receive an incremental incentive for recorded trips. Randomize at zone-window or switchback level so treatment drivers do not directly contaminate control drivers. Primary metric is request fulfillment rate, with recorded trips per eligible online driver-hour as a supply diagnostic and incremental trips per incentive dollar as the economic metric. Guardrails include estimated wait, cancellations, driver earnings, and trips in adjacent zones.

The main marketplace risk is interference: one driver can affect many riders and other drivers. A driver-level A/B test may therefore violate the independence assumption. Geographic cluster, time switchback, or staggered rollout designs are more defensible.

## Decision

Do not authorize a citywide incentive from recorded-trip counts alone. **P0:** instrument requests, cancellations, wait, and driver online time. **P1:** run a pre-powered zone-window switchback test with a defined washout and border policy. **P2:** add weather, holidays, and transit disruption controls only when they improve the comparison.

## Interview explanation

**30-second explanation:** “I used official TLC HVFHV trip data to map recorded-trip concentration by hour and zone. The week had 59,285 records at 04:00 and 334,713 at 18:00, but I would not call that a supply shortage because recorded trips are not total demand. My recommendation is to add request, cancellation, wait, and driver-online denominators, then test incentives by zone-window with displacement and cost guardrails.”

**2-minute explanation:** Explain grain, missing denominators, peak diagnosis, provider and airport segmentation, interference, switchback randomization, and why fulfilled trips per driver-hour is more useful than gross trips.
