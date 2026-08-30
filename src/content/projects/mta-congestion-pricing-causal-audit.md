---
title: "Congestion Pricing: A Comparator Audit Before Causal Claims"
date: 2026-08-29
categories: [growth analytics]
tags: [causal design, comparator audit, mobility, decision quality]
excerpt: "A descriptive audit of NYC bridge and tunnel traffic that shows why a plausible policy story is not enough for a causal business decision."
problem: "Leadership wants to know whether congestion pricing changed traffic, but affected and comparison crossings may already have been on different paths."
result: "The official MTA panel contains 27,080 facility-day observations from 2019 to May 2026; the displayed pre-policy gap is visibly unstable, so this comparator is not used for causal attribution."
featured: true
kind: flagship
evidenceVisuals:
  - /images/growth-mta-event-study.png
  - /images/portfolio-mta-panel-scope.svg
  - /images/portfolio-mta-causal-boundary.svg
header:
  teaser: /images/growth-mta-event-study.png
---

## Business question

Congestion pricing began in New York on **5 January 2025**. A mobility business may want to change rider pricing, driver incentives, or its city strategy after the policy.

The question is not simply whether traffic was different afterward. It is whether the policy changed traffic more than it would have changed without the policy.

## Why it matters

Traffic changes naturally. Weather, holidays, construction, commuting patterns, and facility problems can all move the numbers. Comparing only before and after can attribute a natural or unrelated change to the policy.

## Decision brief

- **Recommendation:** do not use this comparison group to claim a congestion-pricing effect or change rider pricing.
- **Evidence:** the affected-comparison gap changed materially in both directions before the policy date; this is a descriptive instability flag, not a formal test.
- **Potential value:** none estimated; this study is a decision-quality audit.
- **Evidence strength:** Moderate for flagging comparator instability; insufficient for formally rejecting parallel trends or estimating the policy effect.
- **Cost / resource requirement:** A credible estimate requires a new comparator, route-exposure data, and internal ride outcomes; cost cannot be estimated from this study.
- **Main risk:** pre-existing trends, spillovers, facility shocks, and the gap between traffic counts and ride-hailing outcomes.
- **Cost of inaction:** Cannot be estimated from this dataset; acting on a false causal claim could misprice rides or misallocate supply.
- **Success / stop rule:** Proceed only if pre-trends and placebo checks pass; stop the causal claim if the replacement comparator fails them.
- **Next action:** rebuild the comparator and validate it with pre-trends, placebos, route exposure, and internal ride outcomes.

## Role

Role: event-time diagnostic, comparator audit, and recommendation to pause the causal claim. The analysis does not control policy, facility operations, or ride-hailing data. Decision-owner handoff: a rejected comparator, a pre-registered replacement rule, and the evidence required before pricing action. [Reproducible analysis and validation notes](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/03-congestion-pricing-causal-impact) show the design and limits.

## Data used

The analysis uses the official [MTA Bridges and Tunnels Hourly Crossings dataset](https://catalog.data.gov/dataset/mta-bridges-and-tunnels-hourly-crossings-beginning-2019). It provides traffic counts by facility and vehicle class. Car counts form **27,080 facility-day observations** across 10 facilities from 2019 to May 2026.

Three facilities provide access toward the central business district: RFK Bridge Manhattan, Queens-Midtown Tunnel, and Hugh L. Carey Tunnel. Seven other facilities act as comparison crossings. This is a traffic study, not a ride-hailing study. It does not measure platform requests, driver supply, or revenue.

## Approach

1. Compare affected and comparison facilities before the policy.
2. Check whether they were moving in a similar way.
3. Compare their changes around the policy date.
4. Inspect whether apparent breaks also occur before the policy.
5. Stop the causal conclusion if the comparison group is not credible.

The method is a descriptive event-time diagnostic. In plain language, it compares the gap between the two groups week by week around the policy instead of relying on one before-and-after average. Each event week is only one weekly group difference, so the chart does not report pointwise confidence intervals or p-values.

## Key findings

### The comparison group was already moving differently

Before congestion pricing began, the affected-comparison gap changed materially in both directions rather than staying near a stable baseline.

In plain English: the comparison was already moving around before the policy, so its later movement cannot be cleanly attributed to congestion pricing.

![MTA bridge and tunnel event study: affected crossings were already moving differently before congestion pricing, so the comparison is not reliable](/images/growth-mta-event-study.png)

**Business meaning:** the chosen comparison group does not provide a stable descriptive baseline for the affected crossings. The later differences cannot be assigned to congestion pricing with confidence.

### The most useful result is a decision to pause the claim

The chart can still show a post-policy difference, but that difference may reflect the pre-existing gap or another shock. A precise number is not useful if the comparison is biased.

**Business meaning:** a Country Manager should not change rider prices or driver incentives based on this result. The better next step is to build a comparison that matches the affected facilities before the policy.

## Additional visual evidence

### Context: the audited panel has broad facility and week coverage

![MTA congestion-pricing audit scope: 27,080 facility-day observations, 3,880 facility-week observations, 10 facilities, and a plus-or-minus 26-week diagnostic window](/images/portfolio-mta-panel-scope.svg)

The panel is large enough for a diagnostic; size alone does not make the comparator valid.

### Decision: stop the causal claim when the pre-trend fails

![MTA causal evidence boundary: facility crossings and a policy date are observed, but ride-hailing fee exposure and a parallel untreated counterfactual are not](/images/portfolio-mta-causal-boundary.svg)

This is the decision-relevant result: improve identification before attributing an effect.

## Recommendation

**What:** Do not make a causal claim from this control group.

**Where / who:** Rebuild the comparison using facilities with similar pre-policy traffic patterns. Treat nearby crossings as possible spillover areas, not automatically as clean controls.

**Why:** The displayed pre-policy gap is visibly unstable, and this descriptive audit does not formally test the parallel-trends assumption.

**Risk:** A new control may also be affected by the policy or by a facility-specific event.

**Next test:** Pre-register the control-selection rule, add weather, construction, transit, and facility-disruption data, and require acceptable pre-policy trends and placebo results before estimating a policy effect.

## What internal data would improve the decision

For a ride-hailing business, the missing decision inputs are requests, completed and cancelled rides, pickup delay, driver online time, passenger price, driver pay, and routes. Effects should then be estimated separately for affected trips, border areas, peak periods, and airport flows. The public MTA study is useful external context, not a substitute for platform data.

## Key takeaway

A useful analysis can refuse a weak answer. This study found an unstable pre-policy gap, so the business should improve and formally validate the comparison before changing pricing or supply policy.

## Technical appendix

### Validation record

| Check | Current evidence | Decision |
|---|---|---|
| Control selection | 3 affected facilities versus 7 comparison facilities; selected before interpreting post-policy movement | Keep as an audit, not a final estimate |
| Panel and diagnostic | 3,880 facility-week rows across 388 weeks and 10 facilities; equal-weight group means of log(1 + weekly car crossings), centered on event week −1 and shown within ±26 weeks | Reproducible descriptive comparison |
| Pre-policy pattern | Weekly affected-comparison differences change direction and magnitude before policy | Do not use this comparator for causal attribution without formal design validation |
| Inference audit | Each displayed event week is one weekly group difference; pointwise residual-based p-values and confidence intervals are not reported | Avoids false precision from singleton event bins |
| Outcome scope | All-car crossing traffic, not ride-hailing requests, supply, trips, or revenue | Use as external context only |

The event-time script describes the difference between affected and comparison facilities by week around 5 January 2025. The unstable pre-policy gap is the reason the causal claim is blocked; the script deliberately does not attach pointwise inference to singleton weekly event bins. [Reproducible code, validation output, and zone-exposure notes](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/03-congestion-pricing-causal-impact) are available for review.
