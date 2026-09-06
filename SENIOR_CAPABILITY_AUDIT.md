# Senior Analytics Engineer / Product Analyst capability audit

Audit date: 6 September 2026. Scope: all 35 project articles, their available SQL/Python, source records, models, tests, charts, and public evidence. Scores reflect evidence in the repository, not project length or terminology.

## Scoring method

| Dimension | Weight |
|---|---:|
| Problem framing | 10 |
| Metric design | 10 |
| Data understanding and validation | 10 |
| Analytical depth | 15 |
| Root-cause and hypothesis reasoning | 15 |
| Technical implementation | 10 |
| Decision quality | 15 |
| Impact or opportunity sizing | 5 |
| Communication | 5 |
| Limitations and rigor | 5 |

A flagship must score at least 80 and show a meaningful problem, analytical reasoning, trustworthy metrics, evidence-backed findings, an actionable decision, and honest limitations.

## Project-by-project audit

| Project | Target role | Baseline | Final | Seniority | Strongest evidence | Main gap at baseline | Action |
|---|---|---:|---:|---|---|---|---|
| Product Events | AE + Product | 72 | 85 | Senior | Full-source ordered funnel, identity and duplicate controls | No computed funnel or segment diagnosis | UPGRADE completed |
| Financial Metrics | AE | 70 | 86 | Senior | Filing-aware mart, period correction, reference reconciliation | Architecture described without exposing the period-definition failure | MERGE + UPGRADE completed |
| NYC 311 Service Metrics | AE + Product | 64 | 83 | Senior | Mature 348,180-request cohort with closure coverage | No real queue result; recommendation preceded evidence | MERGE + UPGRADE completed |
| Online Retail Retention | Product | 76 | 86 | Senior | Eligible cohorts, cohort mix, and experiment target | Lifetime repeat behaviour mixed unequal observation windows | UPGRADE completed |
| Criteo Incrementality | Product / Growth | 88 | 92 | Strong Senior | Randomized ITT, SRM, uncertainty, heterogeneity, economics | Economics and multiplicity were secondary | KEEP + improve |
| TLC Marketplace Experience | Product / Marketplace | 72 | 86 | Senior | 20.4M-trip delay diagnosis with daily stability rule | Disconnected 2019/2024–25 evidence and no friction outcome | MERGE + UPGRADE completed |
| MDS Customer Metrics | AE | 63 | 63 | Mid-Level | Metric consistency concern | No executable lineage, owner, reconciliation, or incident result | REPLACE |
| Netflix Content Strategy | Product | 62 | 62 | Mid-Level | Clear descriptive catalog story | Catalog mix cannot establish demand or product impact | REPLACE |
| Fake Job Detection | Product / Risk | 76 | 76 | Borderline | Threshold trade-off and model comparison | No production queue baseline, capacity impact, or deployed measurement | ARCHIVE |
| World Happiness | General analysis | 65 | 65 | Mid-Level | Longitudinal descriptive context | No product owner or controllable decision | REMOVE |
| Restaurant Quality | Product / Operations | 73 | 73 | Borderline | Inspection-grain cleaning and missing-grade caution | Weak root-cause and intervention evidence | ARCHIVE |
| NYC Taxi Operations | Marketplace | 74 | 74 | Borderline | Large real trip file and airport segmentation | Completed trips alone cannot support capacity action | MERGE into TLC |
| Clickstream Funnel | Product | 66 | 66 | Mid-Level | Journey framing | No stable identity, ordered event model, or causal next step | REPLACE with Product Events |
| Bank Marketing | Product / Growth | 66 | 66 | Mid-Level | Response-versus-profit caveat | Observational campaign data cannot measure incrementality | REPLACE with Criteo |
| Airfare Pricing | Product / Commercial | 59 | 59 | Junior/Mid | Benchmark caution | Design narrative without executed evidence | REMOVE |
| SEC Company Performance | AE / Finance | 69 | 69 | Mid-Level | Revenue and earnings read together | Duplicate of stronger filing-aware case | MERGE into Financial Metrics |
| Airbnb Marketplace | Product / Marketplace | 68 | 68 | Mid-Level | Supply concentration | Listings do not observe demand, bookings, or availability outcome | ARCHIVE |
| JOLTS Workforce | Product / Operations | 64 | 64 | Mid-Level | Hiring-versus-turnover distinction | Macro series has no product decision or controllable segment | ARCHIVE |
| Credit Default Risk | Product / Risk | 72 | 72 | Borderline | Risk segmentation and limitations | No calibration, operating threshold, fairness, or intervention outcome | ARCHIVE |
| ComplaintFlow | AE / Applied AI | 76 | 76 | Borderline | Auditable workflow and failure handling | Synthetic fixture does not establish real routing quality or value | ARCHIVE |
| Census Market Expansion | Product / Strategy | 62 | 62 | Mid-Level | Suppression awareness | Methods-only; no executed market choice or outcome | ARCHIVE |
| Citi Bike Station Experience | Marketplace | 68 | 68 | Mid-Level | Directional imbalance concept | No station-status panel or completed intervention analysis | ARCHIVE |
| FAA Triage | Risk / AI | 58 | 58 | Junior/Mid | Human-review boundary | Methods-only and insufficient decision evidence | REMOVE |
| FCC Complaint Routing | Product / AI | 60 | 60 | Mid-Level | Allegation-versus-prevalence distinction | No real routing evaluation or queue result | REMOVE |
| Google Analytics Revenue | Product / Growth | 65 | 65 | Mid-Level | User-grain value framing | Methods-only; no completed acquisition analysis | ARCHIVE |
| Instacart Reorder Growth | Product | 68 | 68 | Mid-Level | Replenishment-versus-discovery distinction | No executed sequence analysis or experiment sizing | ARCHIVE |
| MovieLens Coverage | Product | 61 | 61 | Mid-Level | Popularity baseline caveat | No online product outcome or business decision | REMOVE |
| NYC 311 Response Capacity | AE / Operations | 68 | 68 | Mid-Level | Workload-versus-volume framing | Methods-only duplicate | MERGE into Service Metrics |
| Olist Delivery | Marketplace | 64 | 64 | Mid-Level | Order-grain join caution | Overused data and no executed root-cause result | REMOVE |
| Online Shoppers Activation | Product | 76 | 76 | Borderline | Leakage check and sensitivity | Session rows lack ordered events and product mechanism | ARCHIVE |
| Open Contracting Mart | AE | 65 | 65 | Mid-Level | Lifecycle and missing-stage reasoning | No implemented transformation or reliability result | ARCHIVE |
| SEC XBRL Mart | AE | 74 | 74 | Borderline | Fact grain and restatement concepts | Methods-only duplicate | MERGE into Financial Metrics |
| Stack Overflow Adoption | Product | 64 | 64 | Mid-Level | Denominator caution | Survey attitudes cannot establish product adoption behaviour | REMOVE |
| Wikimedia Discovery | Product | 63 | 63 | Mid-Level | Spike-versus-durable-interest distinction | Pageviews cannot measure retention or intervention effect | ARCHIVE |
| Congestion Pricing Audit | Product / Causal | 79 | 79 | Borderline | Correct decision to stop when pre-trends fail | No defensible alternative causal estimate | ARCHIVE |

## Baseline diagnostic scores, 0–10

Abbreviations: PQ problem quality; PF problem framing; MD metric design; DU data understanding; DV data validation; AD analytical depth; HI hypothesis investigation; RC root cause; SG segmentation; SR statistical rigor; DQ decision quality; IQ impact quantification; CQ communication; VZ visualization.

| Project | PQ | PF | MD | DU | DV | AD | HI | RC | SG | SR | DQ | IQ | CQ | VZ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Product Events | 8 | 8 | 8 | 9 | 8 | 6 | 6 | 5 | 4 | 5 | 7 | 3 | 8 | 7 |
| Financial Metrics | 8 | 8 | 8 | 9 | 7 | 6 | 6 | 5 | 4 | 4 | 7 | 3 | 8 | 7 |
| NYC 311 Service Metrics | 8 | 7 | 7 | 8 | 6 | 5 | 5 | 4 | 4 | 3 | 6 | 2 | 8 | 6 |
| Online Retail Retention | 8 | 8 | 6 | 8 | 8 | 7 | 6 | 6 | 7 | 4 | 7 | 5 | 8 | 8 |
| Criteo Incrementality | 10 | 9 | 9 | 9 | 9 | 9 | 9 | 8 | 8 | 10 | 9 | 7 | 9 | 9 |
| TLC Marketplace Experience | 9 | 8 | 6 | 8 | 7 | 6 | 6 | 5 | 5 | 4 | 7 | 2 | 8 | 7 |
| MDS Customer Metrics | 7 | 7 | 6 | 6 | 4 | 5 | 4 | 4 | 3 | 2 | 6 | 2 | 7 | 3 |
| Netflix Content Strategy | 7 | 7 | 6 | 6 | 5 | 6 | 5 | 4 | 6 | 3 | 6 | 3 | 8 | 7 |
| Fake Job Detection | 8 | 8 | 8 | 8 | 8 | 8 | 7 | 6 | 6 | 8 | 8 | 6 | 8 | 8 |
| World Happiness | 5 | 6 | 6 | 7 | 6 | 7 | 6 | 4 | 7 | 6 | 4 | 2 | 8 | 8 |
| Restaurant Quality | 8 | 8 | 7 | 8 | 8 | 7 | 6 | 6 | 7 | 4 | 7 | 4 | 8 | 7 |
| NYC Taxi Operations | 8 | 8 | 7 | 8 | 8 | 7 | 6 | 6 | 8 | 4 | 7 | 4 | 8 | 8 |
| Clickstream Funnel | 7 | 7 | 6 | 6 | 5 | 6 | 5 | 4 | 5 | 3 | 6 | 3 | 8 | 7 |
| Bank Marketing | 7 | 7 | 6 | 7 | 6 | 6 | 5 | 4 | 7 | 5 | 6 | 3 | 8 | 7 |
| Airfare Pricing | 6 | 6 | 5 | 5 | 4 | 4 | 4 | 3 | 5 | 3 | 5 | 2 | 7 | 5 |
| SEC Company Performance | 7 | 7 | 7 | 8 | 6 | 6 | 5 | 4 | 4 | 3 | 6 | 3 | 8 | 7 |
| Airbnb Marketplace | 7 | 7 | 6 | 7 | 6 | 6 | 5 | 4 | 7 | 3 | 6 | 3 | 8 | 7 |
| JOLTS Workforce | 6 | 6 | 6 | 7 | 6 | 6 | 5 | 4 | 6 | 4 | 5 | 3 | 8 | 6 |
| Credit Default Risk | 8 | 7 | 7 | 8 | 7 | 7 | 6 | 5 | 7 | 7 | 7 | 4 | 8 | 7 |
| ComplaintFlow | 8 | 8 | 7 | 7 | 7 | 7 | 7 | 6 | 5 | 5 | 8 | 4 | 8 | 8 |
| Census Market Expansion | 7 | 7 | 6 | 7 | 6 | 5 | 5 | 4 | 6 | 3 | 6 | 2 | 8 | 7 |
| Citi Bike Station Experience | 8 | 8 | 7 | 7 | 6 | 6 | 6 | 5 | 7 | 3 | 7 | 3 | 8 | 7 |
| FAA Triage | 6 | 6 | 5 | 6 | 5 | 4 | 4 | 3 | 4 | 3 | 6 | 2 | 7 | 6 |
| FCC Complaint Routing | 7 | 7 | 6 | 7 | 5 | 5 | 5 | 4 | 5 | 3 | 6 | 2 | 8 | 6 |
| Google Analytics Revenue | 7 | 7 | 6 | 7 | 5 | 5 | 5 | 4 | 6 | 4 | 6 | 3 | 8 | 7 |
| Instacart Reorder Growth | 8 | 8 | 7 | 7 | 6 | 6 | 6 | 5 | 7 | 4 | 7 | 3 | 8 | 7 |
| MovieLens Coverage | 6 | 6 | 6 | 7 | 5 | 5 | 5 | 4 | 6 | 4 | 5 | 2 | 7 | 6 |
| NYC 311 Response Capacity | 8 | 8 | 7 | 8 | 6 | 5 | 5 | 4 | 6 | 3 | 7 | 2 | 8 | 7 |
| Olist Delivery | 7 | 7 | 6 | 7 | 6 | 5 | 5 | 4 | 6 | 3 | 6 | 3 | 8 | 6 |
| Online Shoppers Activation | 8 | 8 | 7 | 8 | 8 | 7 | 7 | 5 | 7 | 6 | 8 | 3 | 8 | 8 |
| Open Contracting Mart | 8 | 8 | 7 | 8 | 6 | 5 | 5 | 4 | 6 | 3 | 7 | 2 | 8 | 7 |
| SEC XBRL Mart | 8 | 8 | 8 | 9 | 7 | 6 | 6 | 5 | 5 | 3 | 7 | 3 | 8 | 7 |
| Stack Overflow Adoption | 6 | 7 | 6 | 7 | 6 | 5 | 5 | 4 | 6 | 4 | 6 | 2 | 8 | 7 |
| Wikimedia Discovery | 7 | 7 | 6 | 7 | 6 | 5 | 5 | 4 | 6 | 3 | 6 | 2 | 8 | 7 |
| Congestion Pricing Audit | 9 | 9 | 8 | 8 | 8 | 8 | 9 | 7 | 7 | 8 | 9 | 3 | 8 | 8 |

## Final dimension scores for retained cases

| Project | Frame | Metrics | Data | Depth | Hypotheses | Tech | Decision | Impact | Comms | Rigor | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Product Events | 9 | 9 | 9 | 12 | 11 | 10 | 12 | 3 | 5 | 5 | 85 |
| Financial Metrics | 9 | 9 | 10 | 11 | 11 | 10 | 13 | 4 | 4 | 5 | 86 |
| NYC 311 Service Metrics | 9 | 9 | 9 | 11 | 11 | 9 | 12 | 3 | 4 | 5 | 83 |
| Online Retail Retention | 9 | 9 | 9 | 12 | 12 | 8 | 13 | 4 | 5 | 5 | 86 |
| Criteo Incrementality | 10 | 10 | 10 | 13 | 13 | 9 | 14 | 4 | 5 | 4 | 92 |
| TLC Marketplace Experience | 9 | 9 | 9 | 12 | 12 | 9 | 13 | 4 | 5 | 4 | 86 |

## KEEP

- **Criteo Incrementality:** already met the senior threshold. The revised version adds metric definitions, commercial thresholds, multiple-comparison context, and a more explicit decision rule.

## UPGRADE

- **Product Events:** full-source ordered funnel, category comparison, metric contract, duplicate and session-validity controls, static full refresh, and test design are now implemented.
- **Online Retail Retention:** lifetime repeat behaviour is replaced by eligible 30/60/90-day cohorts and a bounded 30-day experiment target.
- **TLC Marketplace:** the current period now combines completed volume and pickup-delay outcomes at provider-zone-hour grain and leads to a switchback design.

## MERGE

- **SEC Company Performance + SEC XBRL Mart → Financial Metrics.** The merged case demonstrates why filing context changes the metric and how the error was corrected.
- **NYC 311 Response Capacity → Service Metrics.** The merged case adds the real snapshot, queue results, and pilot design missing from the methods page.
- **NYC Taxi Operations → TLC Marketplace.** Airport and temporal segmentation now support one current-period marketplace decision.

## REPLACE OR ARCHIVE

Projects marked REMOVE are not aligned with the target roles or cannot support a decision with their available variables. Projects marked ARCHIVE contain useful reasoning but add less evidence than the retained set. Their source files remain in the repository; they are not public flagships.

## Improvement specifications for projects below 80

Each specification includes: (1) problem, (2) question, (3) metrics, (4) analysis, (5) hypotheses, (6) segmentation, (7) validation, (8) technical work, (9) required findings, (10) recommendation, (11) measurement, and (12) visuals.

### Product Events — baseline 72

1. **Problem:** choose the product journey step to improve. 2. **Question:** where does the ordered journey lose eligible sessions? 3. **Metrics:** identified session, ordered view/cart/purchase, step conversion, completion time. 4. **Analysis:** execute the full event model and category comparison. 5. **Hypotheses:** pre-cart loss, post-cart continuation, category mix. 6. **Segments:** high-volume product categories. 7. **Validation:** keys, identity, timestamps, event values, funnel monotonicity. 8. **Technical:** full-refresh static-source model, source-batch keys, logical duplicate controls, 24-hour event window, dbt tests. 9. **Findings:** publish measured counts and rates. 10. **Recommendation:** instrument missing drivers and test the largest step. 11. **Measurement:** session-randomized test with purchase and latency guardrails. 12. **Visuals:** ordered funnel, category rates, lineage.

### Financial Metrics — baseline 70

1. **Problem:** stop inconsistent filing facts from reaching management reporting. 2. **Question:** which fact belongs to each annual period? 3. **Metrics:** annual revenue, net income, margin, reconciliation variance. 4. **Analysis:** inspect period, duration, form, unit, tag, and accession. 5. **Hypotheses:** source `fy` misassigns comparative values; mixed contexts change trends. 6. **Segments:** fiscal period and filing context. 7. **Validation:** reconcile to filing, duplicate contexts, units, duration. 8. **Technical:** typed staging, deterministic selection, tests, lineage. 9. **Findings:** quantify the corrected trend and the original error. 10. **Recommendation:** version the metric contract and block unreconciled output. 11. **Measurement:** freshness, variance, backfill reproducibility. 12. **Visuals:** corrected performance, margin, fact lineage.

### NYC 311 Service Metrics — baseline 64

1. **Problem:** decide where to test response capacity. 2. **Question:** which queues combine persistent backlog and slow valid closure? 3. **Metrics:** arrivals, open share, open age, median/P90 close time. 4. **Analysis:** fixed-cutoff queue comparison. 5. **Hypotheses:** volume and pressure differ; pressure is concentrated. 6. **Segments:** agency × complaint type with minimum volume. 7. **Validation:** unique request, missing closure, negative duration, cutoff leakage. 8. **Technical:** request mart, aggregate evidence, CI tests. 9. **Findings:** publish shortlist with counts and timing. 10. **Recommendation:** verify workflow, then test one queue. 11. **Measurement:** backlog, first response, reopen, cost and displacement. 12. **Visuals:** volume/time comparison, priority queues, evidence boundary.

### Online Retail Retention — baseline 76

1. **Problem:** choose when and for whom to test a repeat-purchase experience. 2. **Question:** what share returns within equal observation windows? 3. **Metrics:** eligible 30/60/90-day repeat rates. 4. **Analysis:** order and customer cohorts plus value-band sensitivity. 5. **Hypotheses:** repeat accumulates over time; first value identifies different baselines. 6. **Segments:** first-order-value quartiles and cohort eligibility. 7. **Validation:** cancellations, identity, duplicate invoices, partial period. 8. **Technical:** reproducible transaction→order→customer pipeline. 9. **Findings:** publish counts, rates, and association limits. 10. **Recommendation:** test before day 30. 11. **Measurement:** repeat, timing, margin, returns and holdout through day 90. 12. **Visuals:** cohort windows, value segments, cleaning boundary.

### TLC Marketplace — baseline 72

1. **Problem:** decide where a supply intervention deserves a test. 2. **Question:** where is completed-ride pickup friction persistent? 3. **Metrics:** completed trips, median/P90 request-to-pickup, fare and driver-pay context. 4. **Analysis:** aligned January 2025 provider-zone-hour diagnosis. 5. **Hypotheses:** busy hours differ from slow hours; airport friction is concentrated. 6. **Segments:** provider, zone, hour. 7. **Validation:** missing/negative/extreme timestamps and period spillover. 8. **Technical:** DuckDB scan of 20.4M records. 9. **Findings:** publish priority windows and boundaries. 10. **Recommendation:** airport switchback, no citywide subsidy. 11. **Measurement:** fulfilment, wait, cost, displacement and total rides. 12. **Visuals:** hourly volume/delay, priority windows, observed/unavailable metrics.

### MDS Customer Metrics

1. Define a real cross-team metric dispute. 2. Ask which definition changes a decision. 3. Specify grain, owners, numerator, denominator and effective dates. 4. Reproduce conflicting outputs. 5. Test join, filter and calendar hypotheses. 6. Segment by metric consumer. 7. Add reconciliation and source freshness. 8. Implement versioned marts and contracts. 9. Quantify the disagreement. 10. Choose one governed definition. 11. Monitor drift and adoption. 12. Show lineage and before/after reconciliation.

### Netflix Content Strategy

1. Tie catalog freshness to a programming decision. 2. Ask which audience need is underserved. 3. Define availability, viewing, completion and retention. 4. Join catalog with real engagement data. 5. Test age, genre, region and licensing explanations. 6. Segment by audience and market. 7. Validate title availability windows. 8. Build title-period models. 9. Quantify viewing or retention differences. 10. Recommend a bounded content test. 11. Measure incremental viewing and churn. 12. Replace catalog counts with decision charts.

### Fake Job Detection

1. Define the review-operations decision. 2. Ask which threshold minimizes harm under capacity. 3. Define recall, precision, false-negative cost and queue capacity. 4. Add calibration and time-split validation. 5. Test language drift and employer-history hypotheses. 6. Segment by source and job type. 7. Check leakage, imbalance, drift and fairness. 8. Build monitored scoring and review logs. 9. Quantify prevented exposure and review load. 10. Select a threshold by cost. 11. Measure appeals, misses and reviewer agreement. 12. Show calibration and capacity trade-offs.

### World Happiness

1. Choose a policy decision owner. 2. Ask which controllable factor has credible evidence. 3. Define population outcome and intervention metric. 4. Add policy or natural-experiment data. 5. Test competing macro explanations. 6. Segment by comparable country groups. 7. Validate survey comparability and missing years. 8. Build a panel with uncertainty. 9. Report effect estimates, not rank movement. 10. Recommend only supported policy tests. 11. Measure population outcome and distribution. 12. Use uncertainty and event-study charts.

### Restaurant Quality

1. Define inspection-resource allocation. 2. Ask which establishments have repeated controllable risk. 3. Define inspection episode, critical violation and recurrence. 4. Add repeat-inspection cohorts. 5. Test cuisine, borough, operator and inspection-type explanations. 6. Segment by comparable establishments. 7. Validate episode construction and missing grades. 8. Build establishment history marts. 9. Quantify repeat-risk concentration. 10. Prioritize outreach or inspection tests. 11. Measure recurrence and false targeting. 12. Show recurrence and concentration.

### NYC Taxi Operations

1. Define a dispatch or airport-capacity decision. 2. Ask where completed-trip experience weakens. 3. Define volume, pickup delay, utilization proxy and economics. 4. Use aligned trip-level periods. 5. Test airport, time, route and provider explanations. 6. Segment by zone-hour-route. 7. Validate timestamps and selection. 8. Use partitioned DuckDB models. 9. Quantify priority windows. 10. Test a targeted intervention. 11. Monitor displacement and cost. 12. Merge into the stronger TLC case.

### Clickstream Funnel

1. Define a product step decision. 2. Ask where ordered users leave. 3. Define identity, eligibility, sequence and window. 4. Rebuild sessions from events. 5. Test device, page and category hypotheses. 6. Segment purposefully. 7. Validate event duplication and missing steps. 8. Add event contracts and ordered marts. 9. Quantify step losses. 10. Propose one experiment. 11. Add conversion and latency guardrails. 12. Replace page counts with an ordered funnel.

### Bank Marketing

1. Define budget allocation under contact constraints. 2. Ask which contacts are incremental. 3. Define randomized conversion and contact cost. 4. Obtain treatment/control data. 5. Test channel and frequency hypotheses. 6. Segment only with pre-treatment fields. 7. Check SRM, leakage and balance. 8. Build experiment marts. 9. Estimate uplift and economics. 10. Set rollout thresholds. 11. Monitor complaints and long-term value. 12. Use effect and cost charts.

### Airfare Pricing

1. Define a route-pricing decision. 2. Ask where price changes alter contribution. 3. Define fare, bookings, load factor, cost and elasticity window. 4. Add time and competitor variation. 5. Test route mix, seasonality and inventory. 6. Segment comparable routes. 7. Validate fare class and availability. 8. Build route-date panels. 9. Estimate price response with uncertainty. 10. Recommend a bounded pricing test. 11. Monitor margin and displacement. 12. Show demand curves and scenarios.

### SEC Company Performance / SEC XBRL Mart

Use the twelve-part Financial Metrics specification above. These projects are merged because separate cards would repeat the same decision and evidence.

### Airbnb Marketplace

1. Define host-supply or guest-conversion action. 2. Ask where availability fails demand. 3. Define searches, available nights, bookings and price. 4. Add calendar and booking data. 5. Test seasonality, regulation and host concentration. 6. Segment by neighbourhood and listing type. 7. Validate duplicates and availability semantics. 8. Build listing-date facts. 9. Quantify unserved demand. 10. Design a host intervention. 11. Measure bookings, price and displacement. 12. Replace listing counts with supply-demand charts.

### JOLTS Workforce

1. Define a workforce planning decision. 2. Ask which roles or units face controllable gaps. 3. Define openings, hires, exits, cost and time-to-fill. 4. Combine internal workforce data. 5. Test labour-market versus internal causes. 6. Segment by role and location. 7. Validate definitions and revisions. 8. Build monthly workforce marts. 9. Quantify vacancy cost. 10. Recommend hiring or retention action. 11. Measure fill and retention. 12. Show decomposition and scenarios.

### Credit Default Risk

1. Define approval or support policy. 2. Ask which threshold balances loss and access. 3. Define default horizon, exposure, loss and approval. 4. Add calibration and policy simulation. 5. Test affordability and behavioural hypotheses. 6. Segment by product and protected-risk review groups. 7. Check leakage, drift and fairness. 8. Build scored cohorts and monitoring. 9. Quantify expected loss and affected customers. 10. Recommend a threshold or manual review. 11. Measure loss, approval and fairness. 12. Show calibration and policy curves.

### ComplaintFlow

1. Define queue time and risk decision. 2. Ask which cases can be routed safely. 3. Define routing accuracy, escalation, latency and review cost. 4. Evaluate on a real labelled sample. 5. Test taxonomy drift and low-confidence cases. 6. Segment by complaint type and language. 7. Validate privacy, leakage and reviewer agreement. 8. Add monitored production evaluation. 9. Quantify saved review time with uncertainty. 10. Set human-review thresholds. 11. Measure misses, overrides and drift. 12. Replace synthetic-fixture success with real evaluation charts.

### Census Market Expansion

1. Define an expansion owner and constraint. 2. Ask which market clears a business threshold. 3. Define reachable demand, density, competition and cost. 4. Join real commercial inputs. 5. Test suppression and mix explanations. 6. Segment comparable counties. 7. Validate suppressed cells and vintage. 8. Build market-period marts. 9. Quantify ranked opportunity ranges. 10. Select a research shortlist. 11. Measure pilot acquisition and contribution. 12. Show uncertainty-aware ranking.

### Citi Bike Station Experience

1. Define rebalancing action. 2. Ask where riders face empty/full stations. 3. Define station availability, failed rental proxy and rebalancing cost. 4. Add station-status time series. 5. Test commute, weather and neighbouring-station effects. 6. Segment station-hour clusters. 7. Validate status gaps and station IDs. 8. Build station-hour panels. 9. Quantify shortage duration. 10. Test rebalancing windows. 11. Monitor displacement and cost. 12. Show availability heatmaps and experiment results.

### FAA Triage / FCC Routing

1. Define human-review priority. 2. Ask which records can be routed without suppressing risk. 3. Define recall, escalation, queue time and error cost. 4. Obtain labelled real outcomes. 5. Test taxonomy and language drift. 6. Segment by issue class and source. 7. Validate leakage, bias and privacy. 8. Build monitored routing. 9. Quantify queue and miss impact. 10. Set review thresholds. 11. Measure overrides and harm. 12. Use calibration and capacity visuals.

### Google Analytics Revenue

1. Define acquisition-budget choice. 2. Ask which channel creates incremental contribution. 3. Define user-level value, cost and holdout window. 4. Execute user cohorts and channel comparison. 5. Test mix, device and repeat-visit hypotheses. 6. Segment by pre-treatment attributes. 7. Validate IDs, attribution and window leakage. 8. Build user-period marts. 9. Quantify value with uncertainty. 10. Propose channel holdouts. 11. Measure incremental contribution. 12. Show cohort and experiment charts.

### Instacart Reorder Growth

1. Define next-basket product decision. 2. Ask when a prompt helps replenishment. 3. Define eligible item, reorder window, basket value and substitution. 4. Execute sequence and timing analysis. 5. Test habitual versus discovery items. 6. Segment by product cadence and customer tenure. 7. Validate order sequence and censoring. 8. Build user-item history marts. 9. Quantify eligible opportunities. 10. Test a timed prompt. 11. Measure incremental reorder and basket guardrails. 12. Show timing and opportunity charts.

### MovieLens Coverage

1. Define recommendation objective. 2. Ask whether exploration improves engagement. 3. Define exposure, click, completion and retention. 4. Add online interaction data. 5. Test novelty and popularity hypotheses. 6. Segment by user history. 7. Validate exposure denominators. 8. Build recommendation logs. 9. Quantify coverage-quality trade-off. 10. Test an exploration policy. 11. Measure long-term engagement. 12. Use policy and uncertainty charts.

### Olist Delivery

1. Define marketplace delivery action. 2. Ask which controllable step drives late orders. 3. Define promised, shipped, carrier and delivered intervals. 4. Join order entities at correct grain. 5. Test seller, carrier, distance and seasonality. 6. Segment comparable routes and products. 7. Validate duplicates and censored orders. 8. Build order milestone facts. 9. Quantify loss concentration. 10. Prioritize a seller/carrier intervention. 11. Measure on-time delivery, cost and cancellation. 12. Show driver decomposition.

### Online Shoppers Activation

1. Define an in-session product prompt. 2. Ask which early signal is available before outcome. 3. Define eligible session, prompt time and conversion. 4. Obtain event timestamps or tracking data. 5. Test visitor mix and page-intent hypotheses. 6. Segment by device and traffic source. 7. Validate leakage and duplicates. 8. Build timestamp-safe features. 9. Quantify pre-outcome opportunity. 10. Test a prompt. 11. Measure conversion and annoyance guardrails. 12. Show timestamp-safe funnel evidence.

### Open Contracting Mart

1. Define procurement-review action. 2. Ask which records are incomplete enough to need review. 3. Define release, process, contract and implementation grain. 4. Execute lifecycle reconstruction. 5. Test publisher and stage-missingness causes. 6. Segment by buyer and procurement method. 7. Validate identifiers and late releases. 8. Implement incremental snapshots and tests. 9. Quantify review queues. 10. Route records to review. 11. Measure corrected completeness. 12. Show lineage and failure states.

### Stack Overflow Adoption

1. Define a developer-product onboarding decision. 2. Ask which behaviour predicts successful adoption. 3. Define activation and retained usage from telemetry. 4. Combine survey context with product events. 5. Test experience and learning hypotheses. 6. Segment by role and product goal. 7. Validate survey and user linkage bias. 8. Build consent-safe event models. 9. Quantify activation gaps. 10. Test onboarding variants. 11. Measure activation and retention. 12. Use behavioural funnel charts.

### Wikimedia Discovery

1. Define a content-maintenance decision. 2. Ask which updates improve durable readership. 3. Define page exposure, return reading and quality. 4. Add revision and experiment data. 5. Test news spikes and seasonality. 6. Segment by topic and access channel. 7. Validate bot/platform filters. 8. Build page-day panels. 9. Quantify durable opportunity. 10. Test selected refreshes. 11. Measure incremental readership and quality. 12. Show event-adjusted trends.

### Congestion Pricing Audit

1. Define pricing, supply, or geography response. 2. Ask which marketplace outcome changed after policy. 3. Define treatment, exposure, control, period and spillovers. 4. Build a valid route/zone panel. 5. Test pre-trends, anticipation and substitution. 6. Segment boundary, peak and trip type. 7. Validate zone mapping and concurrent shocks. 8. Implement event study with robust errors. 9. Report only estimates that pass identification checks. 10. Recommend action or no action. 11. Monitor trip, fare, driver-pay and displacement outcomes. 12. Show pre-trends and effects with intervals.

## Portfolio capability matrix

| Capability | Evidence |
|---|---|
| Event tracking and contracts | Product Events |
| Ordered funnel | Product Events |
| Retention cohorts | Online Retail Retention |
| Experimentation and statistics | Criteo Incrementality |
| Product opportunity sizing | Retention and Criteo |
| Marketplace diagnosis | TLC Marketplace |
| Metric governance | Financial Metrics |
| Data quality and cutoff logic | NYC 311 and Financial Metrics |
| dbt layers, lineage, tests | Product Events, Financial Metrics, NYC 311 |
| Incremental processing and backfills | Financial Metrics operating plan; Product Events documents why a static snapshot is full-refreshed until a producer event ID exists |
| Large-data SQL / DuckDB | TLC Marketplace and Product Events |
| Causal restraint | Criteo, TLC, and archived Congestion Audit |

Remaining evidence gaps are production orchestration, warehouse cost benchmarks, slowly changing dimensions, and a true signup-to-activation product dataset. They should be discussed honestly rather than represented by another methods-only card.

## Final hiring-manager assessment

| Perspective | Baseline | Final | Decision |
|---|---:|---:|---|
| Senior Product Analytics Manager | 7.3/10 | 8.3/10 | Interview: the retained cases now diagnose funnels, cohorts, experiments, and marketplace friction with clear evidence limits. |
| Senior Analytics Engineering Manager | 7.1/10 | 8.2/10 | Interview: the portfolio now shows metric correction, contracts, tested models, lineage, and reproducible evidence. |
| Recruiter | 8.0/10 | 8.5/10 | Interview: six focused cases support the positioning without relying on project count. |

The remaining caveat is experience evidence: public projects demonstrate senior thinking, but production scale and ownership still depend on professional-history verification during hiring.
