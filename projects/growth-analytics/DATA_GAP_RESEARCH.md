# Marketplace data-gap research

Research date: 29 August 2026. The goal was to find real public evidence for requests, wait, supply, and utilization before accepting a limitation.

| Variable | Sources checked | Found? | Best available alternative | Quality |
|---|---|---:|---|---|
| Total ride requests | TLC trip records, TLC monthly reports, TLC HVFHV data dictionary, NYC Open Data | No public trip-level request stream found | Use recorded dispatched trips only; request denominator requires internal platform logs | Low for demand; do not call trips total demand |
| Lost / unmatched requests | TLC trip records, TLC reports, TLC public notices, NYC Open Data | No | Use cancellation only if a source explicitly identifies request failure; otherwise collect internal match outcomes | Not reconstructable from trip rows |
| Request timestamp | TLC HVFHV records, TLC trip dictionary | No in the validated historical table | No defensible proxy from pickup timestamp alone | Do not infer wait |
| Estimated / actual wait | TLC FHV License Review, TLC reports | Yes, aggregate | January 2025 average citywide HVF wait reported as 4.8 minutes; January 2024 comparison 4.25 minutes | Good for citywide context, not zone-hour causality |
| Active drivers | TLC monthly data reports | Yes, aggregate | High Volume FHV unique drivers and average driver-hours per day | Monthly, not concurrent hourly supply |
| Active vehicles | TLC monthly data reports and FHV base aggregate report | Yes, aggregate | Unique vehicles and vehicles per day by month | Good observed-activity proxy; not online availability |
| Driver online-hours | TLC monthly data reports | Partial | Average hours per day per driver | Reported average, not zone-hour online supply |
| Vehicle utilization | TLC monthly data reports | Partial | Average hours per day per vehicle and trips per day | Activity proxy; not idle time or matched supply |
| Driver utilization | TLC monthly data reports | Partial | Average hours per day per driver and trips per day | Cannot calculate passenger-occupied share |
| Idle time | TLC trip records, monthly reports | No | Gap between consecutive recorded trips for observed vehicles only, if a stable vehicle identifier is available | Not true idle time because off-platform and unavailable periods are unobserved |
| Supply / demand ratio | TLC public sources | No direct ratio | Combine recorded trips with monthly drivers/vehicles as a descriptive triangulation | Not a true marketplace ratio |
| Congestion-zone entries | MTA Congestion Relief Zone Vehicle Entries | Yes | Daily/hourly vehicle entries by detection crossing and vehicle class | Independent traffic context, not HVFHV-only supply |
| Congestion-zone boundary | NY State MTA CBD geofence and TLC taxi-zone shapefile | Yes | Spatial overlap mapping with inside/partial/outside labels | 20 inside, 21 partial, 222 outside among 263 geometry records; through-route exposure remains unresolved |

## Sources that materially improve the project

- [TLC Aggregated Reports](https://www.nyc.gov/site/tlc/about/aggregated-reports.page) publishes monthly trips per day, unique drivers, unique vehicles, vehicles per day, average hours, and average trip minutes. The downloaded report has 896 rows from 2010-01 through 2026-05 and 137 High Volume FHV rows from 2015-01 through 2026-05.
- [TLC FHV License Review](https://a860-gpp.nyc.gov/downloads/vh53x103h?locale=en) reports aggregate wait context. The January 2025 review reports 4.8 minutes average citywide HVF wait versus 4.25 minutes in January 2024, while warning that full congestion-pricing impact could not yet be determined.
- [MTA Congestion Relief Zone Vehicle Entries](https://data.ny.gov/) provides hourly and 10-minute traffic-entry counts by detection crossing and vehicle class. It is a triangulation source, not a substitute for HVFHV requests.
- [MTA Central Business District Geofence](https://data.ny.gov/widgets/srxy-5nxn?mobile_redirect=true) provides a machine-readable polygon collection.
- [TLC taxi-zone geometry](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) provides the official spatial units used by trip records.

The downloaded Q1 2025 MTA entry extract contains post-launch records beginning 5 January 2025. It supports an external post-policy traffic context, but not a pre-policy trend on its own. A longer historical traffic source or pre-period sensor data is required for causal validation.

## Decision gate

**TLC marketplace: KEEP, REDESIGN.** The project is stronger with monthly drivers, vehicles, hours, and aggregate wait context. It must remain a triangulated marketplace-health study, not a claim about total demand or true online supply. A replacement dataset was not selected because the official TLC combination is more relevant to a Bolt-style city marketplace than a generic accommodation or ecommerce marketplace, even though the request funnel still requires internal data.

**Congestion pricing: KEEP, REDESIGN, PRIVATE.** The official geofence and MTA traffic-entry data solve the boundary and external-validation gaps. The full HVFHV pre/post panel and through-route exposure still need to be completed before publishing a causal estimate. The article remains hidden until that evidence exists.
