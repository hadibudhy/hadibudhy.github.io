---
title: "Online Shoppers: Finding Intent Without Leaking the Outcome"
date: 2026-08-30
categories: [growth analytics]
tags: [activation, conversion, leakage, UCI]
excerpt: "A session-level conversion study that separates useful early intent signals from fields that only appear after a shopper has already shown value."
problem: "The product team wants to improve conversion, but a targeting rule can look excellent simply because it uses information created after the shopper has already progressed."
result: "After deduplicating 12,205 sessions, new visitors converted at 24.9% versus 14.1% for returning visitors, while positive PageValues sessions converted at 56.3% and zero-PageValues sessions at 3.9%."
published: true
---

## Business question

Which session signals should receive the next activation experiment, and which fields must be excluded because they are downstream of the decision?

## Why it matters

A high-performing conversion model can still be useless if it reads the answer from the future. The team needs a rule that can be evaluated at the moment an intervention is possible, not after checkout intent is already visible.

## Decision brief

- **Recommendation:** test a light-touch activation prompt using pre-intervention browsing depth and visitor type; keep `PageValues` out of targeting.
- **Evidence:** the cleaned file contains 12,205 sessions after removing 125 duplicate rows. New visitors converted at **24.9%** (422/1,693) versus **14.1%** (1,470/10,431) for returning visitors.
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
3. Compare conversion by visitor type, weekend status, month, and browsing signals.
4. Mark variables that are unavailable or unsafe at intervention time.
5. Turn the strongest descriptive contrasts into a bounded randomized test.

## Key findings

### New visitors were not the lowest-intent group

New visitors converted at **24.9%**, while returning visitors converted at **14.1%** in this file.

**Meaning:** visitor type is a useful descriptive cut, but it is not a customer-value ranking. The result may reflect traffic mix, campaign timing, or how the dataset defines a new session.

**Why it matters:** a blanket “returning visitors deserve the prompt” rule would be poorly supported. Test the interaction between visitor type and early browsing behavior instead.

### PageValues is a powerful diagnostic and a dangerous targeting feature

Sessions with positive `PageValues` converted at **56.3%** (1,538/2,730), compared with **3.9%** (370/9,475) when the value was zero.

**Meaning:** the field is strongly associated with the outcome, but it summarizes value-producing pages in the session. It is not a clean pre-intervention feature for a conversion prompt.

**Why it matters:** using it would create leakage and overstate expected lift. Keep it for diagnosis and guardrail analysis, not eligibility.

### The outcome moved with season and calendar mix

November converted at **25.5%**, while May converted at **11.0%**. Weekend sessions converted at **17.5%**, versus **15.1%** on weekdays.

**Meaning:** traffic context matters, and a single pooled conversion rate is not a stable planning assumption.

**Why it matters:** the next test needs time-stratified randomization and a calendar-aware readout so a seasonal mix shift is not mistaken for product impact.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | 12,205 deduplicated sessions; new visitors converted at 24.9% and returning visitors at 14.1% | Choose hypotheses for the next activation test |
| Inferred | Visitor type and early browsing behavior may be useful eligibility signals | Design a stratified, randomized prompt test |
| Not established | Any prompt caused conversion, or that `PageValues` is available before intervention | Do not use post-outcome fields for targeting |

## Validation record

- **Grain:** one session; rates use deduplicated rows.
- **Checks:** 12,330 raw rows, 125 exact duplicate rows, 0 missing values, binary `Revenue` outcome.
- **Guardrail:** `PageValues` is retained for diagnosis but excluded from a pre-intervention feature set.

## Recommendation

**What:** run a randomized activation experiment based on fields available before the prompt, such as visitor type, product-page depth, and time-on-site.

**Where / who:** start with high-volume sessions where the prompt is relevant and accessible; analyze new and returning visitors separately.

**Why:** the public data identifies meaningful descriptive differences, but it cannot show whether an intervention caused them.

**Risk:** a prompt can increase short-term conversion while harming experience or repeat use. Add dismissal, bounce, and seven-day return guardrails.

**Next action:** define the eligibility timestamp, primary denominator, minimum detectable effect, and stop rule before launch.

## Evidence strength and limitations

This is an observational session analysis. It supports hypotheses and measurement design, not a causal claim. It cannot identify unique people reliably, connect sessions to order value, or measure treatment spillover. The source is historical, and the 125 duplicates may represent repeated or duplicated records rather than independent sessions.

## Reproducibility

Source and file documentation: [UCI dataset page](https://archive.ics.uci.edu/dataset/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset). The portfolio’s [expansion validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md) records the checked file, grain, and validation decisions.

## Technical appendix

Rates use deduplicated session rows as the denominator. `Revenue=True` is the outcome. No feature selection or model metric is used as evidence of incremental conversion. The recommended test is an A/B test because the public source has no treatment assignment.
