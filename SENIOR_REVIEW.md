# Senior review: Growth and Marketplace Analytics projects

Review date: 29 August 2026. Sol independently reviewed the project files, public case studies, SQL, Python, and interview guides. The scores below are readiness scores for the checked-in evidence, not a claim about interview performance.

## Executive verdict

The Criteo project is now the strongest artifact: it has a real randomized source, a reproducible streaming ITT calculation, explicit data validation, uncertainty, and a narrower transport claim. The TLC marketplace project is now a triangulated limited-data diagnostic using trip records, monthly drivers/vehicles/hours, aggregate wait context, and official external sources. The congestion project remains intentionally unpublished because the complete pre/post HVFHV panel and route-level exposure are not yet available, although the official geofence is now validated.

## Project 1: Campaign incrementality

**Original Sol score:** 6.5/10. **Current score:** 8.0/10 for benchmark-analysis readiness; it is not a current campaign performance claim.

| Area | Original | Current | Review |
|---|---:|---:|---|
| Business relevance | 7 | 8 | Clear Head of Growth decision and economic boundary |
| Analytical depth | 7 | 8 | ITT plus exploratory feature-band analysis |
| Statistical rigor | 6 | 8 | Absolute effect, confidence interval, p-value, and SRM check |
| Experimentation | 7 | 8 | Assignment, guardrails, holdout, MDE and stopping rules |
| Causal reasoning | 6 | 8 | Exposure is kept downstream; benchmark transport is limited |
| SQL | 5 | 8 | SQL now returns arm totals, rates, lift, and incremental-per-100k |
| Python | 5 | 8 | Streaming, schema, null, binary, exposure, and ratio checks |
| Visualization | 5 | 8 | Direct ITT effect chart with uncertainty and sample context |
| Communication | 8 | 8 | Plain-language decision story |
| Decision quality | 5 | 8 | No rollout claim without internal economics |
| Interview strength | 7 | 8 | Clear 30-second, 2-minute, and deep-dive path |
| Data limitations | 8 | 8 | Criteo subsampling and anonymization are explicit |

### Remaining limitation

Criteo combines several experiments and non-uniformly subsamples the release, so the observed lift is valid for the released benchmark comparison but should not be treated as a current advertiser forecast. The anonymized features also cannot support business-labeled segment recommendations.

## Project 2: Marketplace supply and demand

**Original Sol score:** 4.7/10. **Current score:** 7.5/10 for limited-data interview readiness.

| Area | Original | Current | Review |
|---|---:|---:|---|
| Business relevance | 7 | 8 | Clear incentive decision |
| Analytical depth | 6 | 8 | Official API extraction triangulated with monthly drivers, vehicles, and hours |
| Statistical rigor | 3 | 5 | Descriptive evidence is now labelled; no causal estimate is claimed |
| Experimentation | 4 | 7 | Zone-window switchback, washout, borders, and interference are named |
| Causal reasoning | 6 | 7 | Does not infer shortage from trip volume |
| Marketplace understanding | 6 | 7 | Denominator and displacement risks are explicit |
| SQL | 2 | 7 | SQL now reproduces the official hourly API output |
| Python | 2 | 8 | API fetch, monthly proxy processing, and chart regeneration are reproducible |
| Visualization | 1 | 8 | Hourly and monthly charts have units, source, and limitation |
| Communication | 6 | 8 | Clear distinction between recorded trips and demand |
| Decision quality | 4 | 7 | Collect missing funnel data before subsidy |
| Interview strength | 5 | 8 | 15 bounded cases plus experiment questions |

### Remaining limitation

The historical one-week API slice cannot establish current zone persistence, unmet demand, or incentive ROI. TLC monthly reports improve supply context but are aggregate and not zone-hour online availability. Aggregate wait data is useful context but not a zone-level outcome. These gaps cannot be fully resolved from public sources alone; the next required source is internal request, match, cancellation, wait, driver-online, and incentive data.

## Project 3: Congestion-pricing causal impact

**Original Sol score:** 4.0/10. **Current score:** 6.5/10 for causal-design readiness; **not published**.

| Area | Original | Current | Review |
|---|---:|---:|---|
| Business relevance | 7 | 8 | Direct pricing and marketplace decision |
| Analytical depth | 5 | 8 | Event-study estimator, external traffic context, and geofence validation |
| Statistical rigor | 2 | 6 | Estimator now specifies panel grain and clustered inference checks |
| Experimentation | 4 | 6 | Spillover and policy evaluation logic are explicit |
| Causal reasoning | 4 | 8 | Pickup-only treatment rejected; official zone overlap and through-trip ambiguity documented |
| Econometrics | 4 | 7 | Fixed effects, event time, placebo/pre-trend requirements |
| SQL | 1 | 7 | Integer event time and policy flag are explicit |
| Python | 1 | 7 | Validated zone-day event-study estimator added |
| Visualization | 1 | 3 | Boundary mapping is validated; no causal effect chart until the panel exists |
| Communication | 5 | 7 | Correctly reports no identified effect |
| Decision quality | 4 | 7 | No policy change from insufficient evidence |
| Interview strength | 4 | 8 | Strong discussion of assumptions and failure modes |

### Remaining limitation

TLC fee exposure applies to trips to, from, within, or through the charge zone. Pickup-only treatment and outside-zone controls are not sufficient. The MTA geofence-to-TLC-zone map is now reproducible and classifies 20 zones as inside, 21 as partial/boundary, and 222 as outside. The full HVFHV pre/post panel, route/fee exposure handling, and a valid untreated comparison are still required before publishing an effect or chart. Keeping this project unpublished is the correct business decision.

## Changes made after review

- Narrowed Criteo claims to the released benchmark and removed rollout language that over-transported the rate.
- Added Criteo schema, feature, null, binary, control-exposure, and sample-ratio checks.
- Added exploratory feature-band output and an effect-size chart with uncertainty.
- Replaced marketplace SQL that pointed to the wrong Parquet period and invalid field with the exact official API result source.
- Added reproducible TLC API extraction and chart regeneration.
- Added TLC monthly High Volume FHV driver, vehicle, trip, hours, and trip-duration proxies.
- Added MTA geofence, CRZ entries, and official taxi-zone geometry downloads.
- Added reproducible polygon-overlap validation with inside/partial/outside classification.
- Changed marketplace primary metric hierarchy to request fulfillment, supply productivity, and incremental trips per incentive dollar.
- Replaced “completed” with “recorded” where the public data only supports submitted-trip wording.
- Rejected pickup-only congestion treatment and post-treatment composition controls.
- Added a validated Python event-study estimator and integer event-time SQL.
- Kept the congestion article unpublished until the required data and exposure map exist.
- Added `DATA_GAP_RESEARCH.md` and `CONGESTION_ZONE_VALIDATION.md` with sources checked and remaining reconstructability limits.

## Final independent conclusion

The package demonstrates senior judgment most clearly when it refuses unsupported conclusions: Criteo separates benchmark ITT from current economics, TLC separates recorded trips from total demand, and congestion pricing remains unpublished without identification. Project 1 meets the senior portfolio bar. Project 2 is a credible limited-data case but should be presented as a diagnostic and interview exercise. Project 3 is a strong design exercise, not yet a finished causal analysis.
