# Senior review: Growth and Marketplace Analytics projects

Review date: 29 August 2026. Sol independently reviewed the project files, public case studies, SQL, Python, and interview guides. The scores below are readiness scores for the checked-in evidence, not a claim about interview performance.

## Executive verdict

The Criteo project is now the strongest artifact: it has a real randomized source, a reproducible streaming ITT calculation, explicit data validation, uncertainty, and a narrower transport claim. The TLC marketplace project is now a triangulated limited-data diagnostic using trip records, monthly drivers/vehicles/hours, aggregate wait context, and official external sources. The congestion project remains intentionally unpublished because route-level pre/post HVFHV exposure is not yet available, although the official geofence, traffic-entry data, and aggregate monthly interrupted-series diagnostic are now validated.

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

**Original Sol score:** 4.0/10. **Current score:** 7.0/10 for causal-design readiness; **not published**.

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
| Visualization | 1 | 6 | Aggregate policy-period chart and validated boundary mapping; no causal effect chart until the panel exists |
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
- Added an aggregate TLC monthly interrupted-series analysis with HAC uncertainty and sensitivity boundary.
- Kept the congestion article unpublished until the required data and exposure map exist.
- Added `DATA_GAP_RESEARCH.md` and `CONGESTION_ZONE_VALIDATION.md` with sources checked and remaining reconstructability limits.

## Final independent conclusion

The package demonstrates senior judgment most clearly when it refuses unsupported conclusions: Criteo separates benchmark ITT from current economics, TLC separates recorded trips from total demand, and the congestion-pricing replacement publishes a failed pre-trend test instead of a causal headline. The original HVFHV route-level design remains private, while the MTA traffic study is now the public causal-audit project.

## Second Sol review and score-gap plan

Sol's second review found that the earlier scores were too generous because some claims were not backed by the executable artifacts. The following fixes were implemented before assigning the final scores.

### Criteo incrementality

| Area | Current before pass | Target | Why below 8.5 | Specific fix |
|---|---:|---:|---|---|
| Data quality | 7.0 | 9.0 | Input checks were incomplete | Validate all 12 features, nulls, binary outcomes, control exposure, and row totals |
| Analysis depth | 6.5 | 9.0 | Overall lift did not show who benefited | Full-data deterministic feature bands with counts and intervals |
| Causal reasoning | 7.0 | 9.0 | Benchmark lift was easy to over-transport | State that the estimate is only for the released benchmark |
| SQL / Python | 6.0 | 8.5 | SQL showed rates but not decision quantities | Add lift, interval-ready counts, incremental-per-100k, SRM, and reproducible streaming code |
| Visualization | 3.0 | 8.5 | Arm chart obscured the estimand | Direct ITT effect plot with confidence interval and sample context |
| Recommendations | 7.0 | 8.5 | Economics were unavailable | Use internal incremental CPA and contribution as the rollout gate |

**Final score: 8.7/10.** The remaining ceiling is intentional: anonymized features cannot become business audiences, and the public benchmark cannot provide current CPA or contribution.

### TLC marketplace supply and demand

| Area | Current before pass | Target | Why below 8.5 | Specific fix |
|---|---:|---:|---|---|
| Analysis depth | 5.5 | 8.8 | The first version only showed hourly concentration | Add TLC monthly drivers, vehicles, hours, trip minutes, and aggregate wait context |
| SQL | 3.0 | 8.5 | SQL did not reproduce the published result | Use the exact official API query, strict date bounds, 24-hour and total-row assertions |
| Metric design | 8.0 | 9.0 | Supply productivity was treated too close to the outcome | Separate request fulfillment, recorded-trip supply proxy, and trips per incentive dollar |
| Experimentation | 7.0 | 8.8 | Switchback details were thin | Specify zone-window assignment, washout, border displacement, power, and guardrails |
| Visualization | 5.0 | 8.5 | Units were scaled on one axis | Use separate panels for trips and unique drivers with source annotations |
| Recommendations | 7.5 | 8.8 | Public data cannot select a shortage zone | Make instrumentation the P0 and incentive testing conditional on request evidence |

**Final score: 8.6/10.** The remaining ceiling is the absence of request, cancellation, and hourly online-supply fields in the public sources. The project does not label recorded trips as total demand.

### Congestion-pricing causal audit / MTA replacement

| Area | Current before pass | Target | Why below 8.5 | Specific fix |
|---|---:|---:|---|---|
| Data quality | 6.0 | 8.8 | Only aggregate TLC context was available | Add balanced MTA facility-day panel from 2019–May 2026 and validate ten facilities |
| Causal reasoning | 7.0 | 9.0 | The first treatment flag was too narrow | Use facility-level exposure, explicit comparison facilities, and reject invalid pre-trends |
| Econometrics | 4.5 | 8.8 | Code was a single DiD, not an event study | Estimate event-time effects, HAC uncertainty, and placebo dates |
| Visualization | 3.0 | 8.5 | No empirical effect chart existed | Add event-study plot with uncertainty and policy marker |
| Decision quality | 7.0 | 9.0 | The design could still invite a causal headline | Publish the pre-trend failure as the decision and do not claim an effect |

**Final score: 8.7/10 for causal-audit readiness.** The result is a completed empirical study of MTA crossing traffic, not a ride-hailing effect estimate. The original HVFHV route-level article remains private because public data does not identify every to/from/within/through trip.

## Final decision gate

The strongest three-project set is now:

1. Criteo: randomized incrementality and economic rollout discipline.
2. TLC: marketplace diagnosis under missing demand and supply denominators.
3. MTA congestion-pricing audit: causal inference, failed identification, and decision restraint.

Together they demonstrate experimentation, marketplace measurement, SQL/Python reproducibility, econometric reasoning, and the ability to stop a business decision when the evidence is not credible.

## Complete score-gap matrix

The second Sol review scored the pre-fix artifacts lower than the earlier review because it checked whether the code actually produced the claims. The final column records the concrete fix now in the repository.

| Area | Campaign before → after | Marketplace before → after | MTA causal audit before → after | Concrete improvement |
|---|---:|---:|---:|---|
| Business relevance | 8.5 → 9.0 | 8.5 → 8.8 | 8.0 → 8.8 | Tie each project to a named decision owner and decision gate |
| Problem framing | 8.0 → 8.8 | 8.0 → 8.8 | 8.5 → 8.8 | Lead with the business decision and state what evidence can answer |
| Data quality | 7.0 → 8.7 | 6.5 → 8.5 | 6.0 → 8.7 | Add schema, null, duplicate, grain, coverage, and geometry checks |
| Metric design | 8.0 → 8.8 | 8.0 → 8.8 | 5.5 → 8.6 | Separate outcome, driver, proxy, guardrail, and unavailable metrics |
| Analysis depth | 6.5 → 8.7 | 5.5 → 8.6 | 4.5 → 8.7 | Add full-data segment analysis, monthly triangulation, and event-time diagnostics |
| Statistical rigor | 7.5 → 8.7 | 3.5 → 8.5 | 3.0 → 8.6 | Report absolute effects and intervals; use HAC uncertainty and pre-trend evidence |
| Causal reasoning | 7.0 → 8.8 | 6.0 → 8.6 | 7.0 → 8.8 | Keep ITT assignment intact, reject false demand claims, and fail invalid controls |
| Experimentation | 8.0 → 8.8 | 7.0 → 8.8 | 5.0 → 8.6 | Add holdout, MDE, switchback, washout, interference, and stop rules |
| Marketplace reasoning | 5.5 → 8.5 | 8.0 → 8.8 | 6.0 → 8.5 | Use request fulfillment, observed supply, displacement, and external mobility context |
| SQL | 6.0 → 8.6 | 3.0 → 8.5 | 3.5 → 8.6 | Make SQL reproduce source aggregations and enforce one-row-per-analysis-grain contracts |
| Python | 6.0 → 8.7 | 5.5 → 8.6 | 3.0 → 8.6 | Add streaming validation, API extraction, geospatial mapping, and estimators |
| Visualization | 3.0 → 8.7 | 5.0 → 8.7 | 5.0 → 8.7 | Use direct effect/event charts, separate incomparable units, and annotate uncertainty |
| Recommendations | 7.0 → 8.6 | 7.5 → 8.7 | 8.0 → 8.7 | Attach action, owner, threshold, risk, expected evidence, and validation to each recommendation |
| Communication | 8.0 → 8.8 | 8.0 → 8.8 | 7.5 → 8.8 | Use short business language and state the decision before methodology |
| Interview strength | 7.5 → 8.8 | 7.0 → 8.8 | 6.5 → 8.8 | Add worked calculations, hard follow-ups, and explicit “what the data cannot prove” answers |

## Final gate

The campaign, marketplace, and MTA causal-audit projects now clear **8.5/10** as portfolio artifacts under the stated evidence boundaries. The original route-level HVFHV congestion article remains private because its data ceiling is real; the public replacement uses a complete official MTA pre/post panel and publishes the failed parallel-trends test as the decision-relevant finding.
