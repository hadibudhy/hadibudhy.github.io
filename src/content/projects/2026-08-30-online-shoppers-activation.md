---
title: "Online Shoppers: Finding Intent Without Leaking the Outcome"
date: 2026-08-30
categories: [growth analytics]
tags: [activation, conversion, leakage, UCI]
excerpt: "A session-level conversion study that separates useful early intent signals from fields that only appear after a shopper has already shown value."
problem: "The product team wants to improve conversion, but a targeting rule can look excellent simply because it uses information created after the shopper has already progressed."
result: "After removing 125 exact duplicates, all 12,205 sessions are accounted for: new visitors converted at 24.9%, Other at 19.8%, and returning visitors at 14.1%."
published: true
kind: completed
evidenceVisuals:
  - /images/portfolio-online-shoppers-visitor.svg
  - /images/portfolio-online-shoppers-pagevalue.svg
  - /images/portfolio-online-shoppers-sensitivity.svg
---

## Business question

Which session signals should receive the next activation experiment, and which fields must be excluded because they are downstream of the decision?

## Why it matters

A high-performing conversion model can still be useless if it reads the answer from the future. The team needs a rule that can be evaluated at the moment an intervention is possible, not after checkout intent is already visible.

## Decision brief

- **Recommendation:** test a light-touch activation prompt using pre-intervention browsing depth and visitor type; keep `PageValues` out of targeting.
- **Evidence:** among 12,205 deduplicated sessions, new visitors converted at 24.9% (422/1,693), “Other” at 19.8% (16/81), and returning visitors at 14.1% (1,470/10,431); no treatment assignment is included.
- **Evidence strength:** Moderate for descriptive segmentation; low for causal product impact because no treatment assignment or user-level experiment exists.
- **Main risk:** the sample is historical and session-level. A returning visitor may appear in many rows, and the dataset does not show margin or long-term value.
- **Next test:** randomize prompt eligibility, pre-register conversion and guardrail metrics, and report results by new/returning visitor without using post-intervention fields.

## Role

Role: data validation, leakage review, session segmentation, metric definition, and experiment design. The analysis does not claim that any segment caused conversion or that a prompt will improve revenue.

## Data used

The [UCI Online Shoppers Purchasing Intention dataset](https://archive.ics.uci.edu/dataset/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset) contains 12,330 sessions from an online retailer across ten months of 2018. Each row is a session with browsing counts, duration, device and traffic fields, and a `Revenue` outcome. The downloaded CSV has 18 columns, no missing values, and 125 duplicate rows.

The data is real observation-level web traffic, but it is not a current product log. There is no experiment assignment, customer identity, order value, or post-session retention.

## Approach

1. Validate row grain, missingness, duplicates, and the binary outcome.
2. Remove exact duplicate sessions before calculating rates.
3. Compare conversion by visitor type and inspect the strongest browsing-signal contrast.
4. Mark variables that are unavailable or unsafe at intervention time.
5. Turn the strongest descriptive contrasts into a bounded randomized test.

## Completed result

After removing **125 exact duplicate rows**, the analysis retained **12,205 sessions**. New visitors converted at **24.9%** (422 of 1,693), the source’s **“Other” group converted at 19.8%** (16 of 81), and returning visitors converted at **14.1%** (1,470 of 10,431). The headline new-versus-returning gap is **10.8 percentage points**; the 81 “Other” sessions are shown but are not used in that two-group contrast. These differences are useful for experiment stratification, not proof that visitor status causes conversion.

### Main finding: new visitors had the highest observed conversion rate

![Among 12,205 deduplicated sessions, new visitors converted at 24.9%, Other at 19.8%, and returning visitors at 14.1%](/images/portfolio-online-shoppers-visitor.svg)

The finding changes the test design: do not assume returning traffic is the easiest activation audience, and report the randomized result separately by visitor type. Month, traffic source, device, region, browsing depth, and campaign mix may differ across these groups, so the unadjusted comparison is a hypothesis—not an activation effect estimate.

### Leakage check: PageValues is unsafe until its timing is verified

![Mean PageValues was 27.3 for converted sessions and 2.0 for non-converted sessions, but its availability at intervention time is not established](/images/portfolio-online-shoppers-pagevalue.svg)

Converted sessions averaged **27.3 PageValues**, versus **2.0** for non-converted sessions. That strong separation is analytically useful but operationally unsafe until the business verifies the field's derivation and timestamp availability. The analysis therefore excludes it from eligibility rather than claiming it is definitely late.

### Sensitivity: the visitor contrast survives the row-treatment choice

![New-visitor conversion was 24.9% before and after exact-row deduplication, while returning-visitor conversion moved from 13.9% to 14.1%](/images/portfolio-online-shoppers-sensitivity.svg)

The conclusion is not an artifact of treating exact-identical rows as duplicates. New-visitor conversion remains **24.9%** in both the raw and deduplicated files; returning-visitor conversion moves from **13.9% to 14.1%**. Because the source has no session identifier, the page reports this as a sensitivity decision—not proof that the 125 identical rows are erroneous.

## Experiment design

### Decision: test early signals with a randomized prompt

![Conceptual activation experiment: pre-intervention eligibility flows to randomized prompt assignment and conversion guardrails](/images/portfolio-online-shoppers-experiment.svg)

The decision visual shows the measurement design required before making a product claim.

### Decision: test the observed gap with a timestamp-safe prompt

Visitor type and early browsing behavior are candidate inputs for an activation test. `Revenue` is the outcome; `PageValues` remains excluded from eligibility until its derivation and timestamp availability are verified.

**Meaning:** feature availability must be defined at the moment the prompt could appear.

**Why it matters:** a targeting rule that reads downstream value can overstate expected lift.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | Session-level visitor, browsing, calendar, PageValues, and Revenue fields are available in the UCI release | Define candidate inputs and outcome fields |
| Inferred | Visitor type and early browsing behavior may be useful eligibility signals | Design a stratified, randomized prompt test |
| Not established | Any prompt caused conversion, or that `PageValues` is available before intervention | Do not use post-outcome fields for targeting |

## Validation record

- **Grain:** one session; 12,330 raw rows became 12,205 after removing 125 exact duplicates.
- **Denominators:** visitor-type rates use all deduplicated rows in each visitor group; counts are printed by the checked analysis script.
- **Checks completed:** pinned source hash, exact schema, missing cells, allowed `Revenue` and visitor categories, raw row count, exact-identical rows, group counts, and arithmetic assertions.
- **Guardrail:** `PageValues` is retained for diagnosis but excluded from a pre-intervention feature set.

## Recommendation

**What:** run a randomized activation experiment based on fields available before the prompt, such as visitor type, product-page depth, and time-on-site.

**Where / who:** start with high-volume sessions where the prompt is relevant and accessible; analyze new and returning visitors separately.

**Why:** the public data identifies meaningful descriptive differences, but it cannot show whether an intervention caused them.

**Risk:** a prompt can increase short-term conversion while harming experience or repeat use. Add dismissal, bounce, and seven-day return guardrails.

**Next action:** define the eligibility timestamp, primary denominator, minimum detectable effect, and stop rule before launch.

**Decision status:** Completed descriptive analysis; activation experiment proposed, not launched or measured.

## Evidence strength and limitations

This is an observational session analysis. It supports hypotheses and measurement design, not a causal claim. It cannot identify unique people reliably, connect sessions to order value, or measure treatment spillover. The source is historical, and the 125 duplicates may represent repeated or duplicated records rather than independent sessions.

## Reproducibility

Source and file documentation: [UCI dataset page](https://archive.ics.uci.edu/dataset/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset). The result is reproducible with [`scripts/analyze_online_shoppers.py`](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/scripts/analyze_online_shoppers.py); pass the downloaded `online_shoppers_intention.csv` path and `--output public/data/online-shoppers-metrics.json`. The checked [metrics manifest](/data/online-shoppers-metrics.json) records the source hash, grain, period, denominators, and chart values.

## Technical appendix

Rates use deduplicated session rows as the denominator. `Revenue=True` is the outcome. No feature selection or model metric is used as evidence of incremental conversion. The recommended test is an A/B test because the public source has no treatment assignment.
