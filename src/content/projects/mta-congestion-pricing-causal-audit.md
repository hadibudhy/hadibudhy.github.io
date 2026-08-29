---
title: "Congestion Pricing: When the Causal Design Fails the Test"
date: 2026-08-29
categories: [growth analytics]
tags: [econometrics, causal inference, mobility, decision quality]
excerpt: "An event-study audit of NYC bridge and tunnel traffic that shows why a plausible policy story is not enough for a causal business decision."
problem: "Leadership wants to know whether congestion pricing changed traffic, but affected and comparison crossings may already have been on different paths."
result: "The official MTA panel contains 27,080 facility-day observations from 2019 to May 2026; pre-policy differences fail the parallel-trends check, so no causal effect is reported."
featured: true
header:
  teaser: /images/growth-mta-event-study.png
---

## Business question

Congestion pricing began in New York on **5 January 2025**. A mobility business may want to change rider pricing, driver incentives, or its city strategy after the policy.

The question is not simply whether traffic was different afterward. It is whether the policy changed traffic more than it would have changed without the policy.

## Why it matters

Traffic changes naturally. Weather, holidays, construction, commuting patterns, and facility problems can all move the numbers. If we compare only before and after, we may blame the policy for a change it did not cause.

## Decision brief

- **Recommendation:** do not use this comparison group to claim a congestion-pricing effect or change rider pricing.
- **Evidence:** the affected-comparison gap changed materially in both directions before the policy date.
- **Potential value:** none estimated; this study is a decision-quality audit.
- **Evidence strength:** High for rejecting this comparator; insufficient for estimating the policy effect.
- **Cost / resource requirement:** A credible estimate requires a new comparator, route-exposure data, and internal ride outcomes; cost cannot be estimated from this study.
- **Main risk:** pre-existing trends, spillovers, facility shocks, and the gap between traffic counts and ride-hailing outcomes.
- **Cost of inaction:** Cannot be estimated from this dataset; acting on a false causal claim could misprice rides or misallocate supply.
- **Success / stop rule:** Proceed only if pre-trends and placebo checks pass; stop the causal claim if the replacement comparator fails them.
- **Next action:** rebuild the comparator and validate it with pre-trends, placebos, route exposure, and internal ride outcomes.

## My role

I owned the event-time diagnostic, comparator audit, and recommendation to pause the causal claim. I did not control the policy, facility operations, or ride-hailing data. I would hand the decision owner a rejected comparator, a pre-registered replacement rule, and the evidence required before pricing action. [Reproducible analysis and validation notes](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/03-congestion-pricing-causal-impact) show the design and limits.

## Data used

I used the official [MTA Bridges and Tunnels Hourly Crossings dataset](https://catalog.data.gov/dataset/mta-bridges-and-tunnels-hourly-crossings-beginning-2019). It provides traffic counts by facility and vehicle class. I selected car counts and built **27,080 facility-day observations** across 10 facilities from 2019 to May 2026.

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

![MTA bridge and tunnel event study: affected crossings were already moving differently before congestion pricing, so the comparison is not reliable](/images/growth-mta-event-study.png)

**Business meaning:** the chosen comparison group does not show what would have happened to the affected crossings without the policy. The later differences cannot be assigned to congestion pricing with confidence.

### The most useful result is a decision to pause the claim

The chart can still show a post-policy difference, but that difference may reflect the pre-existing gap or another shock. A precise number is not useful if the comparison is biased.

**Business meaning:** a Country Manager should not change rider prices or driver incentives based on this result. The better next step is to build a comparison that matches the affected facilities before the policy.

## Recommendation

**What:** Do not make a causal claim from this control group.

**Where / who:** Rebuild the comparison using facilities with similar pre-policy traffic patterns. Treat nearby crossings as possible spillover areas, not automatically as clean controls.

**Why:** The pre-policy trends fail the basic test required for this type of comparison.

**Risk:** A new control may also be affected by the policy or by a facility-specific event.

**Next test:** Pre-register the control-selection rule, add weather, construction, transit, and facility-disruption data, and require acceptable pre-policy trends and placebo results before estimating a policy effect.

## What internal data would improve the decision

For a ride-hailing business, I would add requests, completed and cancelled rides, pickup delay, driver online time, passenger price, driver pay, and routes. I would then estimate effects separately for affected trips, border areas, peak periods, and airport flows. The public MTA study is useful external context, not a substitute for platform data.

## Key takeaway

The strongest analysis is sometimes the one that refuses a weak answer. This study found that the affected and comparison crossings were already on different paths, so the business should improve the comparison before changing pricing or supply policy.

## Technical appendix

### Validation record

| Check | Current evidence | Decision |
|---|---|---|
| Control selection | 3 affected facilities versus 7 comparison facilities; selected before interpreting post-policy movement | Keep as an audit, not a final estimate |
| Panel and diagnostic | 3,880 facility-week rows across 388 weeks and 10 facilities; log(1 + weekly car crossings), centered on event week −1 | Reproducible descriptive comparison |
| Pre-policy pattern | Weekly affected-comparison differences change direction and magnitude before policy | Comparator is not stable enough for causal attribution |
| Inference audit | Each displayed event week is one weekly group difference; pointwise residual-based p-values and confidence intervals are not reported | Avoids false precision from singleton event bins |
| Outcome scope | All-car crossing traffic, not ride-hailing requests, supply, trips, or revenue | Use as external context only |

The event-time script describes the difference between affected and comparison facilities by week around 5 January 2025. The unstable pre-policy gap is the reason the causal claim is blocked; the script deliberately does not attach pointwise inference to singleton weekly event bins. [Reproducible code, validation output, and zone-exposure notes](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/03-congestion-pricing-causal-impact) are available for review.
