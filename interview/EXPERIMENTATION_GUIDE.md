# Experimentation guide

## The language of a good test

- **Null hypothesis:** no difference in the primary outcome between assignments.
- **Alternative:** the treatment changes the outcome in a stated direction.
- **p-value:** how unusual the observed result would be if the null were true. It is not the probability that the hypothesis is true.
- **Confidence interval:** a range of effects compatible with the data and model assumptions.
- **Effect size:** the business-sized difference, such as 0.115 percentage points in Criteo conversion.
- **Practical significance:** whether that effect changes the decision after cost and risk.
- **Type I error:** calling a change real when it is not.
- **Type II error:** missing a real change.
- **Power / MDE:** choose sample size so the test can detect the smallest useful effect.

## Interview applications

For the Criteo campaign, assignment is the treatment and conversion is the primary metric. Use intention-to-treat, a predeclared confidence interval, and incremental CPA as the commercial guardrail. A p-value below 0.05 does not prove the campaign is profitable. A p-value of 0.08 is evidence that is inconclusive, not proof of no effect; inspect the interval and collect more evidence only under the planned stopping rule.

For marketplace incentives, individual-driver randomization may violate SUTVA because treated drivers affect the same riders and supply pool as controls. Prefer zone clusters, time-based switchbacks, or another design that contains interference. Measure request fulfillment and incremental trips per incentive dollar, not only gross rides or driver productivity.

Avoid peeking, changing the metric after results, stopping when a convenient p-value appears, and testing many segments without correction. Control the false-discovery rate or use a predeclared primary segment. Monitor novelty effects, multiple testing, seasonality, assignment balance, and guardrail regressions.

## Practical checklist

1. State the decision owner and business action.
2. Choose one primary outcome and a small set of guardrails.
3. Define the unit, assignment, eligibility, exposure window, and exclusions.
4. Check sample-ratio mismatch and baseline balance.
5. Set MDE, alpha, power, and the stopping rule before launch.
6. Estimate ITT with uncertainty.
7. Check practical value, heterogeneity, and trade-offs.
8. Replicate important segment findings in a new holdout.
