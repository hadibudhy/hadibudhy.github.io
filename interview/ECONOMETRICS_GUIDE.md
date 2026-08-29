# Econometrics guide

| Method | Business question | Why choose it | Key assumption / failure | Manager explanation |
|---|---|---|---|---|
| OLS | How is an outcome associated with several drivers? | Clear baseline and effect size | Omitted variables, endogeneity, and wrong functional form | “Holding included factors constant, this is the average association.” |
| Fixed effects | How do changes within a zone or day relate to outcomes? | Removes stable unobserved differences | Time-varying confounders remain | “We compare a zone with itself over time.” |
| Difference-in-differences | Did treated areas change more than comparable controls? | Policy or rollout with treatment/control groups | Parallel trends and no harmful spillovers | “We subtract the change seen in comparable areas.” |
| Event study | When did effects begin and how long did they last? | Tests dynamics and pre-trends | Anticipation, staggered effects, and weak pre-period | “We show effects around the event, including whether they started early.” |
| Instrumental variables | What is the effect when treatment is endogenous? | Uses external variation in treatment | Relevance and exclusion restriction | “We use a variable that changes treatment but has no direct outcome path.” |
| Regression discontinuity | What happens around a threshold? | Assignment rule creates local comparison | No manipulation and local validity | “We compare observations just on either side of the rule.” |
| Synthetic control | What would the treated market have done without policy? | One treated unit and many controls | Good pre-fit and no spillover | “We construct a weighted comparison that looks like the treated unit before policy.” |
| Panel data | How do units change over time? | Repeated zone or provider observations | Missingness and dependence | “We use repeated observations while accounting for unit and time differences.” |
| Clustered errors | How should uncertainty reflect grouped observations? | Trips in the same zone are related | Correct cluster level | “Trips in one zone are not independent, so uncertainty must be wider when needed.” |

For congestion pricing, start with an event-study difference-in-differences. Exposure must reflect trips to, from, within, or through the charge zone; pickup-only treatment is too narrow. Inspect pre-trends, placebo dates, border spillovers, provider mix, weather, holidays, and reporting changes. If the assumptions fail, the correct conclusion is that the causal effect is not identified.

Do not call an OLS coefficient causal simply because controls were added. Endogeneity remains when pricing, driver supply, and demand respond to one another. Explain which assumption carries the result and what evidence would challenge it.
