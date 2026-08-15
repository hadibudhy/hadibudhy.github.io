# Senior analysis quality gate

This checklist records the minimum standard applied to the ten dataset case studies. Scores are an editorial readiness check, not a claim that every dataset can answer every business question.

| Project | Business problem | Analytical depth | Root-cause discipline | Data validation | Business judgment | Insight quality | Recommendation | Impact / scenario | Limitations | Storytelling | Executive readability | Decision usefulness | Main remaining limitation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Online Retail | 9 | 9 | 8 | 10 | 9 | 9 | 9 | 8 | 9 | 9 | 9 | 9 | No margin or shipping cost |
| NYC Taxi | 9 | 9 | 8 | 10 | 9 | 9 | 9 | 8 | 9 | 9 | 9 | 9 | One-month operating snapshot |
| Restaurant Quality | 9 | 9 | 8 | 10 | 9 | 9 | 9 | 8 | 10 | 9 | 9 | 9 | Missing grades and inspection-mix bias |
| Clickstream Funnel | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 8 | 10 | 9 | 9 | 9 | No confirmed order or revenue link |
| Bank Marketing | 9 | 9 | 8 | 9 | 9 | 9 | 9 | 8 | 9 | 9 | 9 | 9 | No contact cost or deposit value |
| Airfare Pricing | 9 | 8 | 9 | 9 | 9 | 8 | 9 | 8 | 9 | 9 | 9 | 8 | National benchmark lacks route elasticity |
| SEC Company Performance | 9 | 9 | 8 | 9 | 9 | 9 | 9 | 8 | 9 | 9 | 9 | 9 | Segment and cash-flow drivers need a filing deep dive |
| Airbnb Marketplace | 9 | 9 | 8 | 9 | 9 | 9 | 9 | 8 | 10 | 9 | 9 | 9 | Listings are not bookings |
| BLS Workforce | 9 | 8 | 9 | 9 | 9 | 8 | 9 | 8 | 9 | 9 | 9 | 8 | Aggregate context lacks employee-level causes |
| Credit Default Risk | 9 | 9 | 9 | 9 | 10 | 9 | 9 | 8 | 10 | 9 | 9 | 9 | Historical data requires current fairness validation |

## Editorial checks applied to every project

- The decision owner and decision are stated before the methodology.
- A north-star KPI, driver metrics, and guardrails are named.
- The unit of analysis and important data-quality limitations are explicit.
- Findings distinguish evidence from likely explanation and unproven hypothesis.
- Segmentation or concentration is used where the dataset supports it.
- Opportunity scenarios are labeled as arithmetic scenarios, not forecasts.
- Recommendations are prioritized as P0, P1, and P2.
- Trade-offs and guardrails are stated.
- Experiments include a target, treatment, control, primary metric, and guardrails where causality is not established.
- Sensitivity checks identify alternate windows, definitions, or benchmarks.
- The executive summary is readable without Python, SQL, or statistics knowledge.

## Portfolio-level judgment

The ten projects now demonstrate different decisions rather than ten versions of descriptive EDA: retention investment, taxi capacity, food-safety prioritization, product funnel measurement, campaign targeting, airfare pricing governance, financial performance review, marketplace resilience, workforce planning, and credit-risk support. Several pages deliberately stop short of a financial forecast because the public data does not contain margin, bookings, employee-level, or intervention-outcome fields. That limitation is part of the analysis rather than a hidden assumption.
