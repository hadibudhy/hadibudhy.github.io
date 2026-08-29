# BOLT analytics interview practice

Use these as senior-level drills. For every answer: state the direct answer, reasoning, business implication, common mistake, and likely follow-up.

## A/B testing

1. **Conversion rises 0.1pp.** Answer: estimate the interval and incremental count before calling it useful. Reasoning: scale can make small effects significant. Implication: compare incremental CPA. Mistake: lead with p-value. Follow-up: what is the MDE?
2. **p = 0.08.** Answer: inconclusive, not failure. Reasoning: inspect interval and power. Implication: follow the stopping plan. Mistake: keep peeking. Follow-up: what would more sample change?
3. **SRM appears.** Answer: investigate assignment and eligibility first. Reasoning: broken randomization threatens every result. Implication: pause rollout. Mistake: reweight automatically. Follow-up: what checks do you run?
4. **Revenue up, margin down.** Answer: optimize contribution, not conversion alone. Reasoning: mix or discount may explain it. Implication: hold the rollout. Mistake: declare a win. Follow-up: which guardrails?
5. **Many segment wins.** Answer: correct for multiplicity and replicate. Reasoning: false positives grow with tests. Implication: target only stable segments. Mistake: publish the best slice. Follow-up: holdout design.
6. **Exposure is incomplete.** Answer: use ITT as primary. Reasoning: exposure is post-assignment. Implication: policy effect remains interpretable. Mistake: compare exposed users only. Follow-up: when is TOT defensible?
7. **Treatment affects control.** Answer: redesign randomization. Reasoning: interference violates independent units. Implication: use clusters or switchbacks. Mistake: ignore network effects. Follow-up: SUTVA?
8. **A metric moves after launch.** Answer: check instrumentation and novelty first. Reasoning: behavior or tracking may change. Implication: delay decision. Mistake: attribute immediately. Follow-up: what holdout?
9. **Stopping rule was missed.** Answer: treat the result as exploratory. Reasoning: optional stopping changes error rates. Implication: rerun confirmatory test. Mistake: rename analysis as planned. Follow-up: sequential testing?
10. **A guardrail worsens.** Answer: examine magnitude and trade-off before shipping. Reasoning: primary wins can harm experience. Implication: set decision thresholds. Mistake: hide it. Follow-up: who owns guardrails?
11. **No effect detected.** Answer: distinguish zero from low power. Reasoning: interval and MDE matter. Implication: stop or redesign based on useful-effect range. Mistake: claim no impact. Follow-up: power?
12. **Baseline differs.** Answer: validate randomization and pre-period balance. Reasoning: chance imbalance can exist. Implication: use preplanned covariate adjustment. Mistake: drop unmatched users. Follow-up: CUPED?
13. **Treatment is costly.** Answer: use incremental economics. Reasoning: gross lift ignores spend. Implication: scale only below break-even CPA. Mistake: optimize response. Follow-up: contribution definition?
14. **Multiple primary metrics.** Answer: select one primary and label others guardrails or secondary. Reasoning: ambiguity inflates false positives. Implication: clearer decision. Mistake: choose the winner afterward. Follow-up: hierarchy?
15. **Result differs by provider.** Answer: test interaction and consider mix. Reasoning: heterogeneous response may be real or confounded. Implication: targeted rollout if replicated. Mistake: overgeneralize. Follow-up: sample size per provider?

## Marketplace supply and demand

1. Requests +20%, trips +8%, wait +18%: likely supply or matching pressure; verify driver-hours and cancellations; shortage targeting may help; mistake is calling trips demand; follow-up is zone segmentation.
2. Requests -10%, drivers +15%, utilization -22%: likely excess supply; reduce broad incentives; mistake is adding more supply; follow-up is contribution per hour.
3. City wait flat, one zone +30%: local imbalance; target zone-window; mistake is citywide action; follow-up is adjacent-zone displacement.
4. Airport trips +15%, duration +20%: airport lane changed; measure fare and pay per driver-hour; mistake is using fare per trip; follow-up is deadhead.
5. Trips up, cancellations up: fulfilled volume may hide worsening experience; prioritize cancellation and wait; mistake is celebrating trips; follow-up is request funnel.
6. Provider A up, B down: mix shift; inspect total market and provider coverage; mistake is claiming demand growth; follow-up is license completeness.
7. Incentive cost +30%, trips +5%: weak efficiency until incremental effect is known; test control; mistake is gross lift; follow-up is cost per incremental ride.
8. Weekend peak: compare matched hours and weather; target switchback; mistake is comparing weekday average; follow-up is seasonality.
9. Low zone trips: insufficient evidence; need requests and supply; mistake is labeling low demand; follow-up is data collection.
10. CBD fare up, trips down: possible fee pass-through or composition; use control zones; mistake is causal claim; follow-up is event study.
11. Border zone trips up: substitution possible; include spillover guardrail; mistake is treating as new demand; follow-up is city total.
12. Driver earnings up, utilization down: higher pay may not mean efficient supply; decompose pay and hours; mistake is assuming driver satisfaction; follow-up is net earnings.
13. Same trips, longer duration: traffic or route mix; monitor rider and driver outcomes; mistake is capacity assumption; follow-up is distance.
14. One-hour spike: validate data quality before intervention; use rolling baseline; mistake is reacting to anomaly; follow-up is reporting lag.
15. Supply flat, requests up: plausible shortage; quantify lost rides if cancellations and wait support it; mistake is assuming every extra request is lost; follow-up is fulfillment rate.

## Statistics, SQL, Python, and econometrics

The same answer pattern applies: name the grain, denominator, uncertainty, and decision. Practice the 30 SQL questions in `SQL_INTERVIEW.md`, the assumptions in `ECONOMETRICS_GUIDE.md`, and the experiment checklist in `EXPERIMENTATION_GUIDE.md`. A senior answer should always state what the data cannot prove.

## Statistics (15)

1. **What does a p-value mean?** Direct: evidence against a null under the model; Reasoning: it is not the probability the null is true; Implication: pair it with effect size; Mistake: call p < .05 a business win; Follow-up: what does the interval say?
2. **What is a confidence interval?** Direct: plausible effect range under assumptions; Reasoning: sampling variation remains; Implication: compare the range with the decision threshold; Mistake: interpret it as a 95% probability for this fixed effect; Follow-up: which assumptions?
3. **What is Type I error?** Direct: false positive; Reasoning: repeated testing creates risk; Implication: set alpha before testing; Mistake: ignore multiple looks; Follow-up: how reduce it?
4. **What is Type II error?** Direct: missing a real effect; Reasoning: low power or noisy outcome can hide lift; Implication: use MDE and power planning; Mistake: treat non-significance as zero; Follow-up: inspect the interval.
5. **What is power?** Direct: chance of detecting a specified effect; Reasoning: depends on sample, variance, alpha, and MDE; Implication: plan before launch; Mistake: compute power after seeing results; Follow-up: what effect matters?
6. **Absolute or relative lift?** Direct: use absolute for capacity and economics, relative for context; Reasoning: small baselines inflate relative percentages; Implication: Criteo uses 0.115pp for planning; Mistake: report only 59%; Follow-up: how many incremental conversions?
7. **Why check distribution?** Direct: averages can hide skew and outliers; Reasoning: fares and duration are non-normal; Implication: use medians or robust intervals; Mistake: remove extremes without a rule; Follow-up: sensitivity check?
8. **When use a bootstrap?** Direct: for empirical uncertainty when analytic assumptions are weak; Reasoning: resample units, not rows from the same user; Implication: robust ranges; Mistake: bootstrap dependent observations as independent; Follow-up: what is the resampling unit?
9. **What is an MDE?** Direct: smallest useful effect the test can detect; Reasoning: links sample size to business value; Implication: avoid underpowered tests; Mistake: set MDE after results; Follow-up: what is break-even?
10. **Why use guardrails?** Direct: protect value from harmful trade-offs; Reasoning: conversion can rise while margin falls; Implication: block rollout when customer or cost metrics worsen; Mistake: treat guardrails as optional charts; Follow-up: who owns them?
11. **What is multiple testing?** Direct: testing many hypotheses raises false discoveries; Reasoning: one “winner” can appear by chance; Implication: predeclare or adjust; Mistake: cherry-pick segments; Follow-up: FDR or family-wise control?
12. **What is Simpson’s paradox?** Direct: aggregate and segment directions can differ; Reasoning: mix changes the weighted average; Implication: segment and decompose; Mistake: trust the headline; Follow-up: which mix shifted?
13. **Mean vs median fare?** Direct: median is better for skewed trip economics; Reasoning: a few long trips move the mean; Implication: report both when pricing; Mistake: compare means with different mix; Follow-up: weighted average?
14. **What is selection bias?** Direct: observed sample differs from the target population; Reasoning: participation or coverage is not random; Implication: limit generalization; Mistake: call public complaints representative; Follow-up: what coverage check?
15. **What is measurement error?** Direct: recorded values differ from the true construct; Reasoning: missing waits or inconsistent fields distort KPIs; Implication: validate definitions before modeling; Mistake: treat a clean schema as valid measurement; Follow-up: how audit it?

## Analytical SQL (15)

1. **Treatment rates:** Direct: `GROUP BY treatment` and divide successes by assigned users; Reasoning: assignment is the causal grain; Implication: produces ITT; Mistake: filter exposure; Follow-up: how check SRM?
2. **Top zones by hour:** Direct: aggregate zone-hour then `RANK()` within hour; Reasoning: ranking before aggregation double-counts; Implication: finds concentration; Mistake: rank raw rows; Follow-up: how identify persistence?
3. **Rolling conversion:** Direct: aggregate day then use `ROWS BETWEEN 6 PRECEDING`; Reasoning: rolling raw rows weights high-volume days; Implication: stable monitoring; Mistake: mix incomplete days; Follow-up: how flag partial periods?
4. **Prior-period change:** Direct: use `LAG()` after one row per day; Reasoning: window functions need a stable grain; Implication: shows movement; Mistake: lag duplicate trip rows; Follow-up: what timezone?
5. **Join zone lookup:** Direct: join on a validated unique LocationID; Reasoning: duplicate lookup rows multiply trips; Implication: preserves totals; Mistake: inner join away unknown zones; Follow-up: row-count reconciliation?
6. **Deduplicate users:** Direct: use a user-level CTE before joining outcomes; Reasoning: feature joins can repeat users; Implication: correct denominator; Mistake: count rows as users; Follow-up: `COUNT(DISTINCT)` cost?
7. **Cohort month:** Direct: truncate first activity date and group later activity by months since first; Reasoning: lifecycle comparisons need aligned time; Implication: retention view; Mistake: use calendar month alone; Follow-up: incomplete cohorts?
8. **Weighted fare:** Direct: `SUM(fare)/COUNT(*)`; Reasoning: average of averages misweights volume; Implication: correct city metric; Mistake: average daily means; Follow-up: trip exclusions?
9. **Concentration:** Direct: rank entities, cumulative sum with a window, divide top share by total; Reasoning: prioritization needs mass, not just rank; Implication: identifies risk; Mistake: use top count only; Follow-up: sensitivity to top 1/5/10%?
10. **Event time:** Direct: `DATE_DIFF('day', DATE '2025-01-05', service_date)`; Reasoning: policy effects align by relative time; Implication: event study; Mistake: compare calendar labels only; Follow-up: anticipation window?
11. **Missingness:** Direct: conditional counts by field and period; Reasoning: coverage can change over time; Implication: protects trend interpretation; Mistake: replace missing with zero; Follow-up: missing not at random?
12. **Experiment eligibility:** Direct: apply eligibility before assignment summary; Reasoning: post-treatment filters bias treatment; Implication: valid denominator; Mistake: exclude low performers after treatment; Follow-up: intention-to-treat?
13. **Provider mix:** Direct: group by provider and period, then compare shares; Reasoning: provider composition can explain averages; Implication: controls mix; Mistake: infer market growth from one provider; Follow-up: missing provider handling?
14. **Border spillover:** Direct: flag adjacent zones and compare changes; Reasoning: geography creates interference; Implication: estimates substitution; Mistake: remove border zones because inconvenient; Follow-up: treatment definition?
15. **Query optimization:** Direct: select needed columns and filter partitions early; Reasoning: trip data is large; Implication: lower scan cost; Mistake: `SELECT *` into memory; Follow-up: explain plan?

## Python (10)

1. **Validate schema:** Direct: assert required columns and dtypes; Reasoning: downstream metrics depend on them; Implication: fail early; Mistake: coerce silently; Follow-up: how version schemas?
2. **Read large data:** Direct: stream chunks or scan Parquet columns; Reasoning: full loading wastes memory; Implication: reproducible runs; Mistake: load all 491MB blindly; Follow-up: partition strategy?
3. **Compute an interval:** Direct: calculate two-proportion standard error or bootstrap user units; Reasoning: uncertainty belongs to the randomization unit; Implication: honest decision; Mistake: bootstrap rows after duplication; Follow-up: cluster dependence?
4. **Plot a decision chart:** Direct: title with finding, units, n, and event marker; Reasoning: charts travel without narration; Implication: faster review; Mistake: decorative dashboard; Follow-up: what action does it support?
5. **Test missingness:** Direct: profile null rates by period and segment; Reasoning: missingness may be systematic; Implication: qualify trends; Mistake: fill all nulls with zero; Follow-up: sensitivity rule?
6. **Reconcile joins:** Direct: compare row counts and totals before and after each join; Reasoning: many-to-many joins inflate value; Implication: trustworthy KPIs; Mistake: inspect only final output; Follow-up: uniqueness assertion?
7. **Use regression:** Direct: choose a model tied to the question and inspect residuals/assumptions; Reasoning: complexity does not create identification; Implication: interpretable drivers; Mistake: call coefficients causal automatically; Follow-up: omitted variables?
8. **Make analysis deterministic:** Direct: fix seeds and record versions; Reasoning: samples and models can vary; Implication: reproducible review; Mistake: overwrite outputs without manifest; Follow-up: hash raw inputs?
9. **Handle outliers:** Direct: define business and statistical rules before exclusion; Reasoning: extremes can be real risk; Implication: transparent sensitivity; Mistake: delete inconvenient points; Follow-up: winsorize or report both?
10. **Production handoff:** Direct: separate download, validation, transformation, analysis, and chart functions; Reasoning: each stage can be tested; Implication: easier reruns; Mistake: notebook-only logic; Follow-up: what fails first?

## Econometrics and causal inference (15)

1. **OLS coefficient:** Direct: conditional association; Reasoning: exogeneity is not automatic; Implication: useful baseline, not necessarily causal; Mistake: say “impact” without design; Follow-up: what confounder?
2. **Omitted-variable bias:** Direct: missing correlated driver can shift a coefficient; Reasoning: supply and demand affect fares together; Implication: use controls or design; Mistake: add every column blindly; Follow-up: causal graph?
3. **Endogeneity:** Direct: treatment relates to unobserved outcome drivers; Reasoning: incentives target weak zones; Implication: simple comparisons bias; Mistake: assume controls solve it; Follow-up: instrument or experiment?
4. **Fixed effects:** Direct: compare units after removing stable unit differences; Reasoning: zones have persistent composition; Implication: stronger panel baseline; Mistake: think it removes time-varying shocks; Follow-up: time effects?
5. **Difference-in-differences:** Direct: compare changes in treated and control groups; Reasoning: removes common shocks under parallel trends; Implication: policy estimate; Mistake: skip pre-trend checks; Follow-up: spillovers?
6. **Event study:** Direct: estimate effects by time relative to policy; Reasoning: reveals anticipation and persistence; Implication: timing informs operations; Mistake: interpret pre-period coefficients as proof without power; Follow-up: reference period?
7. **Clustered standard errors:** Direct: allow correlated errors within zones; Reasoning: trips in a zone share shocks; Implication: uncertainty is credible; Mistake: cluster at the wrong level; Follow-up: few clusters?
8. **Synthetic control:** Direct: weighted controls approximate one treated unit; Reasoning: useful for a single city/market; Implication: counterfactual transparency; Mistake: accept poor pre-fit; Follow-up: donor pool?
9. **Instrumental variables:** Direct: use exogenous treatment variation; Reasoning: requires relevance and exclusion; Implication: local causal effect; Mistake: call any predictor an instrument; Follow-up: defend exclusion.
10. **Regression discontinuity:** Direct: compare cases near a threshold; Reasoning: assignment is locally as-if random; Implication: local policy effect; Mistake: generalize globally; Follow-up: manipulation test?
11. **Parallel trends:** Direct: treated/control would have moved similarly absent policy; Reasoning: unobserved counterfactual cannot be seen; Implication: inspect leads and matching; Mistake: prove it with one pre-period; Follow-up: placebo dates?
12. **Spillover:** Direct: treatment affects controls; Reasoning: drivers and riders share the marketplace; Implication: use clusters/switchbacks and border outcomes; Mistake: ignore SUTVA; Follow-up: define exposure radius.
13. **Seasonality:** Direct: recurring patterns can mimic policy effects; Reasoning: January demand differs from other months; Implication: use longer history and calendar controls; Mistake: compare adjacent days only; Follow-up: same-week controls?
14. **Composition change:** Direct: aggregate effect can reflect mix, not behavior; Reasoning: providers, routes, and zones shift; Implication: decompose and reweight; Mistake: trust city average; Follow-up: stable cohort?
15. **No identification:** Direct: report no causal result when assumptions fail; Reasoning: uncertainty is part of evidence; Implication: collect better data; Mistake: force a headline; Follow-up: what minimum data is needed?

## Ambiguous business cases (10)

1. **Rides fell 8%.** Clarify: which market, metric, and period; Reason: could be demand, supply, or data; Implication: choose a funnel; Mistake: recommend incentives immediately; Follow-up: requests and cancellations?
2. **Conversion rose after a price cut.** Clarify: contribution and control; Reason: mix and seasonality; Implication: price test with margin guardrail; Mistake: call price causal; Follow-up: elasticity?
3. **Drivers complain about pay.** Clarify: net earnings per online hour and retention; Reason: trip pay alone is incomplete; Implication: investigate supply health; Mistake: raise incentives without displacement analysis; Follow-up: utilization?
4. **Airport demand is growing.** Clarify: requests, recorded trips, and route definition; Reason: recorded trips omit lost demand; Implication: airport lane test; Mistake: move citywide supply; Follow-up: deadhead?
5. **A dashboard shows a red zone.** Clarify: denominator and data freshness; Reason: low coverage can create false risk; Implication: validate before action; Mistake: rank raw counts; Follow-up: missingness?
6. **Marketing asks for a winner.** Clarify: primary metric, MDE, and cost; Reason: statistical lift may be unprofitable; Implication: incremental CPA decision; Mistake: select highest relative lift; Follow-up: holdout?
7. **A new policy starts next week.** Clarify: outcome, treatment, comparison, and pre-period; Reason: design must precede launch; Implication: preserve causal evidence; Mistake: decide measurement afterward; Follow-up: spillovers?
8. **The CEO wants one KPI.** Clarify: decision and time horizon; Reason: one KPI can hide trade-offs; Implication: define north star plus guardrails; Mistake: present a metric menu; Follow-up: what failure is unacceptable?
9. **Data teams disagree on trips.** Clarify: grain, filters, timezone, and join keys; Reason: definitions often explain the gap; Implication: create a metric contract; Mistake: average the answers; Follow-up: reconciliation query?
10. **No effect is detected.** Clarify: interval, power, and data quality; Reason: null could mean no effect or insufficient evidence; Implication: stop, rerun, or redesign based on useful-effect range; Mistake: claim the intervention failed; Follow-up: what effect would matter?
