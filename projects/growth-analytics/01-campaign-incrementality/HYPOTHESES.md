# Hypotheses

| Hypothesis | Rationale | Expected direction | Metric / test | Decision if supported |
|---|---|---|---|---|
| Advertising increases visits | The treatment is randomized and intended to create traffic | Positive | Difference in proportions with 95% CI | Keep the campaign eligible for scale if the effect is useful |
| Advertising increases conversions | More qualified visits may create customers | Positive | ITT conversion difference and CI | Compare incremental conversions with break-even CPA |
| Treatment value differs by user feature band | Audience response is rarely uniform | Mixed | Pre-declared feature bands with adjusted comparisons | Target only segments with stable positive lift |
| Exposure is not a safe primary treatment definition | Exposure is downstream of assignment | Unknown | Compare ITT with exposure descriptively | Do not replace random assignment with exposed-only analysis |
| The campaign may be statistically positive but commercially weak | Large samples detect tiny effects | Positive but small | Effect size against scenario break-even | Do not scale without economics |

Exploratory segment findings must be labelled exploratory and corrected for multiple comparisons. The current script uses four `f0` bands as a diagnostic only; it does not create a production audience definition.
