# Campaign incrementality and the rollout decision

## Executive summary

**Decision owner:** Head of Growth. **Decision:** should paid media scale, target differently, or stop? **Primary outcome:** incremental conversion. **Guardrails:** visit quality, cost per incremental conversion, complaint rate, and downstream value.

The official unbiased Criteo release contains **13,979,592 user rows**, 12 anonymized features, randomized treatment, exposure, visits, and conversions. A streaming pass finds treatment conversion of **0.309%** versus control conversion of **0.194%**, an absolute difference of **0.115 percentage points** (95% CI **0.108–0.122pp**, two-sided p < 0.001). Visits differ by **1.034pp** (95% CI **1.006–1.063pp**). These are ITT estimates: assignment, not observed exposure, is the causal comparison.

The result is statistically clear within this released benchmark. It should not be transported as the expected lift of a current advertiser campaign because Criteo combines several experiments and non-uniformly subsamples the data. The decision is therefore **do not infer profitable scale from this file**; use the result to define a current-campaign holdout and break-even CPA guardrail.

## Business problem

Leadership needs to know whether the campaign generated customers who would not have converted without advertising. A raw conversion rate cannot answer that because it mixes people persuaded by the campaign with people who would have converted anyway.

## Dataset

The source is the [Criteo AI Lab Uplift Prediction Dataset](https://ailab.criteo.com/criteo-uplift-prediction-dataset/). Criteo describes the file as assembled from randomized incrementality tests. The unbiased release has 13,979,592 rows, an 85% treatment ratio, a 4.6992% visit rate, and a 0.292% conversion rate. Features are anonymized and projected, so they support response segmentation but not business labels such as age or industry. The license is CC BY-NC-SA 4.0; the source terms must be retained when sharing adapted work.

## Measurement framework

```text
Incremental business value
  -> incremental conversions
    -> conversion rate by assignment
      -> visit rate, exposure, audience mix
  Guardrails: CPA, margin, complaints, downstream retention
```

## Experiment validity

The treatment share is approximately 85%, consistent with the official release description. The control group has 2,096,937 rows and the treated group has 11,882,655 rows. There are no missing values in the four outcome/assignment columns used for the ITT calculation. Exposure is present only inside treatment in this release, so it is a post-assignment variable and is not used to redefine the primary experiment.

## Analysis and evidence

The primary estimate is the difference in conversion proportions between all assigned treatment and all assigned control users. The normal approximation is appropriate at this scale. The observed conversion lift is about **59.4% relative to control within the released benchmark**, but the absolute lift is the more useful benchmark description: about **115 additional conversions per 100,000 assigned users**, before cost and value. This is not a current-campaign forecast.

The visit lift is about **1,034 additional visits per 100,000 assigned users**. A visit is not a conversion, so the campaign should not be judged on visits alone.

Feature-level uplift is exploratory because the 12 feature names are anonymized, segment boundaries are analyst choices, and many comparisons create false-positive risk. Any rollout segment must be re-tested on a fresh holdout.

As a reproducible diagnostic, I split the full `f0` distribution into four equal-sized bands. The second band showed the largest conversion difference at **0.386pp** (95% CI **0.361–0.410pp**); the other bands were **0.038pp**, **0.019pp**, and **0.010pp**. These are not customer personas: `f0` has no business meaning, the bands were selected for exploration, and the result needs multiplicity control and a new holdout. It is evidence that response may be heterogeneous, not a targeting policy.

| Exploratory band | Absolute lift | 95% CI | Economics | Current decision |
|---|---:|---:|---|---|
| `f0` lowest quartile | +0.038pp | +0.027 to +0.049pp | Not available | Do not target from this benchmark alone |
| `f0` second quartile | +0.386pp | +0.361 to +0.410pp | Not available | Retest in a pre-registered holdout |
| `f0` third quartile | +0.019pp | +0.012 to +0.027pp | Not available | Do not target from this benchmark alone |
| `f0` highest quartile | +0.010pp | +0.005 to +0.016pp | Not available | Do not target from this benchmark alone |

The table is a decision guardrail, not a spend plan. Without current CPA and contribution value, no segment can be called profitable.

## Economics and decision

Let `V` be internal contribution value per incremental conversion, and let `C` be internal spend per 100,000 assigned users. The campaign breaks even when:

```text
break-even CPA = V
incremental CPA = C / internal_incremental_conversions
```

The public data cannot supply `V`, `C`, or a transportable current-campaign incremental-conversion rate. The growth team should use an internal holdout to measure both inputs, then scale only if measured incremental CPA is below internal contribution value.

## Recommended next experiment

Run a fresh randomized holdout with pre-registered primary conversion, visit-quality, and contribution metrics. Stratify or block randomization only if the platform requires it; preserve assignment-level ITT. Predefine the minimum detectable effect, sample size, stopping rule, and treatment of multiple segments. Use segment targeting as a hypothesis, not as a post-hoc causal claim.

## Risks and limitations

- The data is an assembled benchmark, not one current advertiser campaign.
- Anonymized features cannot explain segments in business language.
- Costs, revenue, margin, and retention are absent.
- Treatment assignment is causal; exposure is not automatically causal.
- Segment searches need multiplicity control and an independent holdout.

## Interview explanation

**30 seconds:** “I used Criteo’s randomized incrementality benchmark to estimate the difference between assigned treatment and control. The released sample shows a 0.115 percentage-point conversion difference with a tight confidence interval. I would not transport that rate to a current campaign because the benchmark combines and subsamples experiments. I would use it to define a current-campaign holdout and an incremental CPA guardrail.”

**2 minutes:** Explain the ITT design, the control/treatment denominators, the conversion and visit confidence intervals, why exposure is downstream, the difference between statistical and practical significance, and the break-even economics required for a rollout decision.
