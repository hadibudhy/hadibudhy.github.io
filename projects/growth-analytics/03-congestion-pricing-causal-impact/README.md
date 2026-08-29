# Congestion pricing and marketplace outcomes

## Executive summary

**Decision owner:** Marketplace and Commercial leadership. **Decision:** should pricing, incentives, or geographic strategy change after congestion pricing? **Primary outcome:** request fulfillment or recorded trips per zone-hour, depending on data availability. **Guardrails:** passenger fare, driver pay, trip duration, cancellations, and cross-zone substitution.

NYC congestion pricing began on **5 January 2025**. TLC states that a `cbd_congestion_fee` field was added to Yellow, Green, and HVFHV records from 2025 onward. The January 2025 yellow-taxi file currently validated in this repository contains **3,475,226 trips** and **2,246,495 rows with a positive CBD fee**. Those are exposure and fee observations, not a causal estimate.

The senior conclusion is deliberately conditional: a simple January before/after comparison cannot identify the policy effect. A credible answer needs a pre-period, a comparison group, event-time controls, and tests for spillovers and pre-trends. Until the official HVFHV 2024–2025 files are complete locally, this project is a causal-design prototype rather than a published effect claim.

## Business problem

Leadership needs to know whether the new fee changed ride volume, fare, driver economics, or geography. A raw post-policy decline could also reflect winter seasonality, weather, holidays, provider mix, or reporting changes.

## Data and grain

The analysis uses [official TLC trip records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), the [HVFHV data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf), and official taxi-zone lookup data. Each trip record is one submitted trip. The policy exposure is assigned at trip-zone and date-time level. The data does not directly contain every ride request, lost match, driver online hour, or customer value.

The validated January 2025 yellow file is used only for schema and fee-field validation. HVFHV is the intended marketplace outcome source because it records licensed high-volume FHV trips; its large official Parquet file must be fully downloaded and checked before publishing estimates.

## Metric framework

```text
Marketplace outcome
  -> fulfilled trips per zone-hour
    -> trip volume, fare, duration, route mix
  Diagnostics: CBD exposure, time of day, airport flows, provider mix
  Guardrails: cancellations, wait, driver pay, substitution, reporting coverage
```

## Identification strategy

The preferred design is a difference-in-differences event study. Policy exposure is defined from origin, destination, and documented zone eligibility after 5 January 2025. A pickup-only flag is not enough because the charge can apply to trips to, from, within, or through the zone. Controls must be plausibly untreated, with ambiguous through-trips and border spillovers handled explicitly. The downloaded MTA CBD geofence and TLC taxi-zone geometry now provide a reproducible boundary map: 20 zones are mostly inside, 21 are partial/boundary, and 222 are outside. The included Python estimator requires one row per zone-day, a precomputed exposure flag, zone and date fixed effects, and at least 10 zone clusters before clustered inference. Provider mix and route composition are diagnostics unless they are known pre-treatment covariates. Inference needs a pre-specified spatial and time dependence strategy, not only a default zone cluster.

The parallel-trends assumption must be inspected before the policy date. Placebo intervention dates should produce no comparable step change. Spillovers are expected: trips may move to border zones, drivers may reposition, and riders may substitute modes. Those effects are part of the business result, not noise to hide.

As an additional sensitivity check, the complete TLC monthly High Volume FHV subset from January 2015 through May 2026 was analyzed as an aggregate interrupted series. It contains **137 monthly observations** with reported trips per day, unique drivers, unique vehicles, and average hours. The model estimates a post-policy level change of **-0.257 log points** (HAC p = **0.034**) and a post-policy trend change of **-0.007 log points per month** (p = **0.110**). These are diagnostic associations, not congestion-pricing effects, because the series has no untreated market and no route-level toll exposure.

## Evidence and current boundary

The January yellow file confirms that the fee field is populated and that positive fee observations exist after the policy date. It does not supply the pre-policy HVFHV comparison needed for the requested causal claim. Therefore this project reports **no estimated policy effect** yet. That is the correct decision under insufficient identification.

## Recommendation

**P0:** complete and validate monthly HVFHV files from at least 2024 and 2025, with the same zone and provider definitions. **P1:** run the event-study and placebo checks. **P2:** add weather, holidays, airport activity, and transit data only when they materially improve pre-trend fit. Change pricing or incentives only if the estimated effect is stable across controls and does not create harmful cross-zone substitution.

## Interview explanation

**30-second explanation:** “I would not call the January change causal from a before/after chart. Congestion pricing started on 5 January 2025, and TLC added a CBD fee field, but seasonality and spillovers remain serious threats. I would use HVFHV trips with zone and time fixed effects, a matched outside-zone control, an event study, placebo dates, clustered errors, and border-zone guardrails. If pre-trends fail, I would report that the effect is not identified.”

**2-minute explanation:** Explain treatment assignment, control construction, parallel trends, anticipation, spillovers, provider mix, route substitution, event-time coefficients, placebo checks, and how the final result would change pricing or supply decisions.
