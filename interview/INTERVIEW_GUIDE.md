# Growth and marketplace interview guide

## Campaign experiment

**Was the campaign successful?** The randomized assignment produced a positive conversion ITT with a tight confidence interval. I would call the response successful, but commercial success still depends on incremental CPA and contribution.

**What is the primary metric?** Incremental conversion by assignment. Visits are a supporting metric, and CPA, margin, complaints, and downstream retention are guardrails.

**Is statistical significance enough?** No. It answers whether the effect is distinguishable from zero under assumptions. The business needs an effect size, interval, cost, and value.

**What if p = 0.08?** Report the interval and uncertainty, do not declare a win or loss, and follow the preplanned sample-size and stopping rule.

**Why ITT?** It preserves randomization and answers the policy question “what is the effect of assigning the campaign?” Exposed-only analysis can be biased because exposure is downstream.

**What if treatment and control sizes differ?** First check the planned allocation, sample-ratio mismatch, eligibility, duplicates, and missing assignment. Do not “fix” a valid 85/15 design by dropping rows.

**What if conversion rises but revenue falls?** Stop the rollout decision, decompose mix and value, and make contribution or revenue-per-user the primary decision metric with conversion as a diagnostic.

**Would you roll it out?** Only behind a break-even CPA guardrail and a fresh holdout. The public benchmark has no economics.

## Marketplace diagnosis

**What is happening when rides rise but wait also rises?** Demand may be growing faster than supply, matching may worsen, or reporting may change. Ask for requests, cancellations, wait, and driver-hour denominators.

**Why not use completed trips as demand?** A completed trip is fulfilled demand. It omits rejected, abandoned, and unserved requests.

**Why switchback or geographic randomization?** Drivers and riders interact, so individual treatment can contaminate control. Cluster or time assignment reduces interference.

**What should be the incentive metric?** Incremental fulfilled trips per eligible driver-hour after incentive cost, with wait, cancellation, driver earnings, and neighboring-zone displacement as guardrails.

**What if the public data is incomplete?** Narrow the claim, label proxies, and identify the next data needed. “Insufficient evidence” is a valid decision.

## Statistics and causal inference

**Correlation or causation?** Correlation describes co-movement. Causation requires a design or assumptions that rule out competing explanations.

**What is a confidence interval?** A range of plausible effect values under the sampling and model assumptions, not a guarantee for one future result.

**What is a practical effect?** A change large enough to affect the decision after cost, risk, and operational constraints.

**What is MDE?** The smallest effect the test is designed to detect with chosen power and error rates.

**What invalidates difference-in-differences?** Non-parallel pre-trends, anticipation, changing composition, and spillovers between treatment and control.
