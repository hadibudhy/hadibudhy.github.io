---
title: "Congestion Pricing: A Comparator Audit Before Causal Claims"
date: 2026-08-29
categories: [growth analytics]
tags: [causal design, comparator audit, mobility, decision quality]
excerpt: "A descriptive audit of NYC bridge and tunnel traffic that shows why a plausible policy story is not enough for a causal business decision."
problem: "Leadership wants to know whether congestion pricing changed traffic, but affected and comparison crossings may already have been on different paths."
result: "The official MTA panel contains 27,080 facility-day observations from 2019 to May 2026; the displayed pre-policy gap is visibly unstable, so this comparator is not used for causal attribution."
featured: true
kind: completed
published: true
caseId: mta-comparator-audit
primaryTrack: experimentation-growth
secondaryTracks: [product-analytics, analytics-engineering]
displayOrder: 60
evidenceManifest: /data/evidence/mta-congestion-audit.json
evidenceVisuals:
  - /images/growth-mta-event-study.png
  - /images/growth-mta-pretrend-test.png
  - /images/portfolio-mta-panel-scope.svg
  - /images/portfolio-mta-causal-boundary.svg
header:
  teaser: /images/growth-mta-event-study.png
---
## Project brief

- **Project:** Audit a proposed comparison group for a congestion-pricing traffic analysis.
- **Question:** Is the comparison stable enough to support a causal claim?
- **Built:** A facility-week panel, pre-policy gap chart, and source-scope audit.
- **Result:** The affected-versus-comparison gap changed before the policy. This audit does not use the group for causal attribution.

## Business question

Congestion pricing began in New York on **5 January 2025**. A mobility business may want to change rider pricing, driver incentives, or its city strategy in response. A simple before-and-after comparison cannot tell whether the policy caused a change or whether affected roads were already moving differently.

The decision is whether this comparison group is reliable enough to support a causal claim.

## Data and preparation

The source is the official [MTA Bridges and Tunnels Hourly Crossings dataset](https://catalog.data.gov/dataset/mta-bridges-and-tunnels-hourly-crossings-beginning-2019). The checked panel contains **27,080 facility-day observations**, grouped into **3,880 facility-week rows** across **10 facilities**, from 2019 through May 2026. Three affected crossings are compared with seven other facilities, with each facility weighted equally.

The outcome is the weekly facility-level log of one plus car crossings. The event-study chart uses a ±26-week window and sets event week −1 as the reference. A separate linear slope diagnostic covers 314 pre-policy weeks and uses HAC standard errors with 26 weekly lags. This is a trend diagnostic, not a causal estimate.

## Stakeholder questions

- **Did the comparison gap stay stable before the policy?** No. It changed direction and magnitude.
- **Does the pre-policy trend test establish that parallel trends hold or fail?** No. The slope estimate is uncertain, and a non-significant result does not prove the comparator is valid.
- **Can MTA crossing counts measure ride-hailing outcomes?** No. The source does not include route toll exposure, platform requests, rides, or revenue.

## Findings

### The comparison gap was already unstable before the policy

![MTA crossing audit: the affected-minus-comparison traffic gap moved in both directions before 5 January 2025, so this group is not a reliable causal baseline](/images/growth-mta-event-study.png)

Each point is the affected-minus-comparison difference in log(1 + weekly car crossings), relative to event week −1. A positive value means the gap was larger than in the reference week; a negative value means it was smaller. The gap changes direction and size before the policy date, which motivates a separate trend check.

Across **314 pre-policy weeks**, the fitted slope was **+0.0155 log points per year** (95% HAC interval: **−0.0047 to +0.0358**, p=**0.133**; 26 weekly lags). The interval includes zero and also allows a positive trend. This test neither establishes a pre-trend nor validates parallel trends; it is not a policy-effect estimate.

![MTA comparator pre-policy linear slope: +0.0155 log points per year, 95% HAC interval −0.0047 to +0.0358 across 314 weeks; the interval includes zero](/images/growth-mta-pretrend-test.png)

### The panel supports a traffic audit, not a ride-hailing outcome

![MTA audit scope: 27,080 daily observations become 3,880 facility-week rows across 10 crossings and 388 weeks; the event-study diagnostic uses a separate ±26-week window around the policy date](/images/portfolio-mta-panel-scope.svg)

The panel gives broad facility and time coverage for checking the comparison. A large panel does not make an unsuitable control group valid.

### Important exposure and outcome data are missing

![MTA evidence boundary: facility-level car counts and the policy date are observed, but route-level toll exposure, ride-hailing requests, and a parallel counterfactual are not](/images/portfolio-mta-causal-boundary.svg)

The traffic records cannot show which trips incurred a fee or how riders, drivers, or platform economics changed. Those questions require route exposure and internal trip outcomes.

## Built

The project aggregates crossings to facility-week rows, compares three affected facilities with seven other facilities, checks the pre-policy trend with a HAC interval, and documents scope and inference limits. It does not estimate a policy effect.

## Result

**Measured result:** the pre-policy slope estimate is +0.0155 log points per year, with a 95% HAC interval from −0.0047 to +0.0358. The event-week gap also moves in both directions. This audit does not use the selected group to estimate a policy effect.

**Not established:** the slope test is a simple linear diagnostic and does not prove parallel trends. The project does not estimate a causal effect or measure ride-hailing demand, supply, revenue, or customer behavior.

**Recommendation:** do not change rider prices or driver incentives based on this comparison. Before a new study, pre-register the comparator and trend checks, examine placebo dates, and account for weather, construction, transit, and facility disruptions. Add route-level toll exposure and internal measures such as requests, rides, cancellations, pickup delay, passenger price, and driver pay.

**Limitations:** nearby crossings may be affected by spillovers, facility-specific shocks, or broader travel changes. The public MTA panel is useful traffic context, not a substitute for platform data.

## Technical appendix

The event-study outcome is the weekly facility-level log of one plus car crossings. The chart shows the affected-minus-comparison difference relative to event week −1 within ±26 weeks. The slope diagnostic fits the pre-policy weekly gap against elapsed calendar years; HAC standard errors use 26 lags. Neither analysis estimates the congestion-pricing effect.

| Check | Evidence | Decision |
|---|---|---|
| Groups | 3 affected facilities and 7 comparison facilities | Keep as a descriptive audit |
| Panel | 3,880 facility-week rows across 388 weeks and 10 facilities | Reproducible weekly comparison |
| Pre-policy pattern | The weekly gap changes direction and magnitude | Do not use this group for causal attribution without further validation |
| Inference | One group difference per event week; no pointwise intervals or p-values | Avoid false precision |
| Outcome scope | All-car crossings, not ride-hailing requests, supply, trips, or revenue | Use as external context only |

The [analysis code and validation notes](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/03-congestion-pricing-causal-impact) document the weekly aggregation and decision boundary. Unexecuted future-design scaffolds in that folder are not evidence for this result.
