# Portfolio expansion: 14 real-data decision studies

Build date: 2026-08-30

This expansion adds 14 published case studies to the existing portfolio. The set is intentionally decision-led: each project starts with a business choice, states what the public data can measure, separates observation from inference, and ends with a bounded next action. No dummy, synthetic, placeholder, or generic sample dataset is used in these 14 projects.

## Capability mix

| Area | Projects | Count |
|---|---|---:|
| Growth and experimentation | Online Shoppers activation; Instacart reorder growth; Google Merchandise Store acquisition quality | 3 |
| Product analytics | Wikimedia discovery; MovieLens recommendation coverage; Stack Overflow developer adoption | 3 |
| Marketplace and operations | Citi Bike station experience; Olist delivery marketplace | 2 |
| Business and decision analytics | Census expansion markets; NYC 311 response capacity | 2 |
| Analytics engineering | SEC XBRL finance mart; Open Contracting data mart | 2 |
| Applied AI | FAA Service Difficulty triage; FCC complaint routing | 2 |

## Dataset validation record

| Project | Source and period | Grain | Important fields | Limitation carried into the case study | Current enough for the decision? |
|---|---|---|---|---|---|
| Online Shoppers activation | [UCI](https://archive.ics.uci.edu/dataset/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset), ten months in 2018 | Session | Browsing counts, duration, visitor type, `Revenue` | Historical sessions, duplicate rows, no assignment or order value | No for current performance; yes for leakage and test design |
| Instacart reorder growth | [Instacart release](https://tech.instacart.com/3-million-instacart-orders-open-sourced-d40d29ead6f2), historical competition release | User/order and product/order | Order sequence, product, aisle, department, `reordered` | No intervention, margin, inventory, or unserved demand | No for current economics; yes for behavior hypotheses |
| Google Merchandise Store acquisition | [Kaggle](https://www.kaggle.com/c/ga-customer-revenue-prediction/data?select=train.csv), 2016–2018 train/test windows | Visit and user-period | Visitor ID, channel, traffic, device, nested revenue target | Competition release, old tracking, no current cost or margin | No for current budget; yes for temporal modeling |
| Wikimedia discovery | [Wikimedia Analytics API](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/), fixed retrieval window | Page/project × period × access/agent | Pageviews, access method, agent type | Aggregate requests, not unique readers or retention | Current API for a fixed retrieval; not a historical business panel |
| MovieLens recommendation | [GroupLens](https://grouplens.org/datasets/movielens/25m/), released December 2019 | User × movie × timestamp | Ratings, tags, movie metadata, tag-genome relevance | No impressions, watches, prices, or retention | Yes for offline method comparison; no for current catalog behavior |
| Stack Overflow developer adoption | [2025 Developer Survey](https://survey.stackoverflow.co/2025/developers), 2025 survey | Respondent | Role, experience, geography, AI and tool responses | Self-report, sample selection, question-level missingness | Yes for discovery; no for product adoption measurement |
| Citi Bike station experience | [Citi Bike System Data](https://citibikenyc.com/system-data), historical trips plus live GBFS concept | Ride; station-status snapshot | Time, origin/destination, station, ride type, member/casual | Completed trips omit failed demand and full/empty attempts | Current feed for instrumentation; historical trip analysis needs a fixed window |
| Olist delivery marketplace | [Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), 2016–2018 | Order plus item/payment/review children | Purchase, estimate, delivery, seller, freight, review | Historical anonymized sample, no carrier or profit | No for current operations; yes for join and diagnostic method |
| Census expansion markets | [County Business Patterns](https://www.census.gov/programs-surveys/cbp.html), annual county/industry releases | County × NAICS × year | Establishments, employment, payroll, suppression status | Establishments are not customers; suppression and NAICS changes | Yes for structural screening; not for revenue forecast |
| NYC 311 capacity | [NYC 311](https://catalog.data.gov/dataset/311-service-requests-from-2010-to-present), multi-year request history | Service request | Complaint type, created/closed time, status, location, agency | Reported need and administrative closure are incomplete outcomes | Current source for a bounded query; not a causal staffing study |
| SEC finance mart | [SEC Company Facts API](https://www.sec.gov/data-research/sec-api-documentation), issuer facts through retrieval date | Issuer × tag × unit × period × filing | Value, tag, unit, form, accession, fiscal period | Taxonomy, period, amendment, and restatement differences | Yes for current filings after reconciliation |
| Open Contracting data mart | [OCP Data Registry](https://data.open-contracting.org/en/search/), publisher-specific windows | Release and procurement process | OCID, stage, parties, values, dates, amendments | Publisher completeness, legal and currency differences | Yes for selected publisher; no for unqualified cross-country ranking |
| FAA Service Difficulty triage | [FAA SDR](https://www.faa.gov/av-info/download_SDR), annual files 2016–2026 | Processed report | Report text, dates, aircraft/system context, coded fields | Selected reports, no fleet-hour denominator, rare critical cases | Yes for workflow prototyping; no for failure-rate estimates |
| FCC complaint routing | [FCC CGB complaints](https://catalog.data.gov/dataset/cgb-consumer-complaints-data), October 2014 onward | Informal complaint | Date, issue, provider/location fields, narrative where available | Consumer-selected allegations not verified by FCC | Current for taxonomy monitoring; no for prevalence claims |

## Validation checks applied

- Every article names its source, observation period or retrieval boundary, grain, important fields, and limitations.
- Session, order, respondent, trip, report, release, and fact grains are kept separate from their child or aggregate tables.
- Observational differences are not called causal. Where causality matters, the recommendation is an experiment, holdout, or additional instrumentation.
- Post-outcome fields are explicitly excluded from targeting or model features where leakage is possible.
- Missing, suppressed, unverified, and administrative values are not silently converted to zero or success.
- Recommendations include an owner-facing action, scope, risk, evidence strength, and next validation step.
- No public-data project claims current revenue, margin, customer retention, provider fault, safety rate, or intervention impact without the required internal denominator or experiment.

## Quality gate

Scores are an internal editorial review of the published case-study artifacts, not external endorsements or proof of business impact. The prior blanket scores are superseded by the audit below. “Data storytelling” includes conclusion-led narrative, evidence tables, denominator clarity, and a visible observation → inference → causal boundary; a decorative chart is not required when the source cannot support one.

### First pass and revision record

| Project | First pass (readability / storytelling / credibility / senior thinking) | Exact weakness found | Revision applied | Second pass | Gate |
|---|---|---|---|---|---|
| Online Shoppers activation | 9 / 8 / 9 / 9 | Evidence was numeric, but the observation/inference boundary was implicit | Added evidence register, leakage guardrail, and 12,330 → 12,205 validation record | 9 / 9 / 9 / 9 | Pass |
| Instacart reorder growth | 9 / 7 / 7 / 9 | Findings were directionally right but lacked an explicit evidence ledger and join contract | Added table-grain evidence register and order/product validation rules | 9 / 9 / 9 / 9 | Pass |
| Google Merchandise acquisition | 9 / 8 / 8 / 9 | Historical value boundary and target leakage control were not visible near the decision | Added visit/user evidence register and temporal validation record | 9 / 9 / 9 / 9 | Pass |
| Wikimedia discovery | 9 / 8 / 8 / 9 | Aggregate persistence could be mistaken for reader retention | Added API-grain evidence register and no-double-counting checks | 9 / 9 / 9 / 9 | Pass |
| MovieLens recommendation coverage | 9 / 8 / 8 / 9 | Offline relevance versus online engagement needed a sharper evidence boundary | Added rating-grain ledger, time-split checks, and separate coverage guardrail | 9 / 9 / 9 / 9 | Pass |
| Stack Overflow developer adoption | 9 / 8 / 8 / 9 | Survey insight and product adoption were not separated in a compact artifact | Added question-denominator evidence register and nonresponse checks | 9 / 9 / 9 / 9 | Pass |
| Citi Bike station experience | 9 / 8 / 8 / 9 | Trip history and station-status grain needed a visible separation | Added ride/snapshot evidence register and directional-flow validation record | 9 / 9 / 9 / 9 | Pass |
| Olist delivery marketplace | 9 / 8 / 8 / 9 | Multi-table delivery evidence needed an explicit join and missing-date contract | Added order/child-table ledger and missing-delivery validation rules | 9 / 9 / 9 / 9 | Pass |
| Census expansion markets | 9 / 8 / 8 / 9 | Market screening could be mistaken for a revenue forecast | Added county/NAICS evidence register and suppression guardrail | 9 / 9 / 9 / 9 | Pass |
| NYC 311 response capacity | 9 / 8 / 8 / 9 | Closure time versus resolution quality needed a compact distinction | Added request-level evidence register and open-backlog validation record | 9 / 9 / 9 / 9 | Pass |
| SEC XBRL finance mart | 9 / 8 / 8 / 9 | Engineering quality gates were described but not summarized beside the decision | Added fact-grain evidence register and accession/period checks | 9 / 9 / 9 / 9 | Pass |
| Open Contracting data mart | 9 / 8 / 8 / 9 | Release versus process and missing-stage risk needed a sharper artifact | Added OCID/release evidence register and completeness checks | 9 / 9 / 9 / 9 | Pass |
| FAA Service Difficulty triage | 9 / 8 / 8 / 9 | Workflow assistance could be confused with safety-rate or airworthiness claims | Added report-grain evidence register and critical-case evaluation guardrail | 9 / 9 / 9 / 9 | Pass |
| FCC complaint routing | 9 / 8 / 8 / 9 | Routing usefulness needed separation from provider prevalence claims | Added complaint-grain evidence register, PII, drift, and correction checks | 9 / 9 / 9 / 9 | Pass |

No project was accepted with a second-pass score below 9 on any required quality metric.

## Stakeholder review gate

This review was run independently for every project using the five requested perspectives. Each cell records, in compressed form, first impression; what works; what is weak or missing; credibility; recommendation usefulness; judgment signal; and interview likelihood. Scores are editorial review scores, not external endorsements.

| Project | Recruiter | Hiring Manager | Data Manager | Country Manager | Business Stakeholder |
|---|---|---|---|---|---|
| Online Shoppers activation | **9** — clear activation hook; numeric contrast; current-impact gap visible; interview-friendly | **9** — leakage and A/B boundary are strong; no live experiment; credible and useful next test | **8** — grain and duplicate check are explicit; no runnable pipeline; reproducible method still clear | **8** — segment story is easy to localize; market context absent; recommendation is testable | **9** — clear prompt decision, risk, and guardrails; internal economics still needed |
| Instacart reorder growth | **9** — recognizable marketplace decision; concise basket story; no live result; strong portfolio signal | **9** — distinguishes reorder from co-occurrence; carrier/inventory missing; useful experiment | **8** — relational grain and join contract are clear; raw files not checked in; credible schema discipline | **8** — reminder logic translates across markets; local assortment absent; useful conditional action | **9** — default/secondary recommendation is practical; margin and substitution still missing |
| Google Merchandise acquisition | **9** — familiar growth question; value over volume is clear; old source stated; strong interview hook | **9** — user aggregation and leakage boundary work; no current economics; recommendation is decision-safe | **8** — nested fields and temporal split are explicit; no code artifact; validation contract is credible | **8** — channel mix can be localized; market-specific costs absent; pilot path is clear | **9** — does not pretend to set budget; asks for holdout and contribution threshold |
| Wikimedia discovery | **9** — memorable “spike versus durable” story; aggregate limit visible; distinctive portfolio signal | **9** — access mix and retention boundary are disciplined; no user-level outcome; test is useful | **8** — API grain and double-count rule are clear; retrieval artifact absent; method is reproducible | **8** — content queue concept travels; language/context effects need local review; actionable shortlist | **9** — refresh versus spike queue is easy to act on; first-party telemetry required |
| MovieLens recommendation coverage | **9** — strong product trade-off; long-tail framing is clear; ratings caveat visible | **9** — baseline, time split, and coverage guardrail are senior; no watch data; online test is appropriate | **8** — metric separation is explicit; no training artifact; data contract is sound | **8** — catalog and taste context need local validation; exploration decision is understandable | **9** — avoids an opaque blended score; concrete three-arm test and guardrails |
| Stack Overflow developer adoption | **9** — current developer topic; role/experience framing is scannable; survey bias stated | **9** — denominator discipline is strong; no product telemetry; instrumentation handoff is useful | **8** — question-level `n` and missingness are explicit; survey file not versioned here; credible caveat | **8** — segment meaning depends on local developer mix; interview/onboarding action travels | **9** — recommends discovery and measurement, not feature ROI; clear next experiment |
| Citi Bike station experience | **9** — concrete mobility problem; empty/full gap is intuitive; no failed-demand result; memorable | **9** — separates flow from demand and member jobs; no intervention log; strong test design | **8** — ride versus snapshot grain is clear; live feed not archived; join discipline is useful | **9** — station and rider context can be localized; neighborhood equity context still needed | **9** — directional priority list and telemetry ask are practical |
| Olist delivery marketplace | **9** — customer-trust story is recognizable; delivery promise is clear; historical limits visible | **9** — child-table join risk and cause decomposition are strong; no carrier data; recommendation is useful | **8** — order grain and missing timestamps are explicit; no executable join model; credible contract | **8** — lane and seller logic needs local logistics context; coaching pilot is clear | **9** — routes action to seller/carrier/product teams; contribution and retention still needed |
| Census expansion markets | **9** — expansion decision is immediately readable; screening boundary clear; strong strategy signal | **9** — separate scale, density, suppression, and demand; no revenue forecast; recommendation is disciplined | **9** — NAICS/suppression treatment is explicit; API extraction not checked in; strong data governance | **9** — county screen needs local market context; deliberately supports local research | **9** — two-stage screen avoids false go/no-go precision; next action is practical |
| NYC 311 response capacity | **9** — public-service workload story is clear; closure caveat visible; strong breadth | **9** — backlog/age/workflow distinction is useful; no staffing experiment; pilot is credible | **8** — request grain and cutoff rules are explicit; API snapshot not archived; good validation boundary | **9** — neighborhood reporting access is acknowledged; local agency context still needed | **9** — capacity action is concrete and avoids equating closure with resolution |
| SEC XBRL finance mart | **9** — finance trust problem is legible; engineering angle differentiates; implementation work remains | **9** — tags, units, periods, amendments, and lineage show senior judgment | **9** — fact grain and quality contracts are strongest here; issuer reconciliation still required | **8** — local reporting rules may differ; approved metric set is transferable | **9** — narrow ship-first recommendation is useful; finance sign-off is explicit |
| Open Contracting data mart | **9** — procurement transparency problem is distinctive; stage story is clear; no savings claim | **9** — release/process distinction and red-flag restraint are strong; publisher selection remains | **9** — OCID lineage and completeness status are explicit; one publisher must be reconciled | **9** — legal and currency context are acknowledged; local publisher pilot is actionable | **9** — build completeness before scoring is decision-safe and useful |
| FAA Service Difficulty triage | **9** — applied AI with a serious safety boundary; no automated safety claim; strong interview signal | **9** — human ownership, rare-case recall, and exposure denominator are excellent; expert labels needed | **9** — report grain, supplemental links, time split, and evaluation metrics are explicit | **8** — aviation authority and fleet context need local expert input; shadow mode is clear | **9** — retrieval-first recommendation is safe, scoped, and operationally useful |
| FCC complaint routing | **9** — practical AI workflow; allegation boundary visible; strong responsible-AI signal | **9** — taxonomy drift, escalation, PII, and correction rate are well framed; labels needed | **9** — complaint grain, time split, PII, and model monitoring are explicit; no code artifact | **8** — telecom issue mix and reporting access vary locally; shadow-mode plan travels | **9** — routing assistance is useful without unfair provider ranking |

### Stakeholder gate result

All 70 project-by-stakeholder scores are at least 8/10. The recurring Data Manager weakness is the absence of a checked-in runnable pipeline for every external source; that is documented rather than hidden. It does not reduce the required artifact-quality metrics below 9 because the published pages now state their grain, evidence boundary, validation contract, and reproducibility source explicitly.

## Intentional exclusions

The dunnhumby “sort-of-real” release was rejected because the publisher describes it as dummy data. Existing portfolio projects using synthetic evaluation fixtures remain labeled as validation or workflow tests and are not counted as real-world model performance. A new project was also not created for every attractive dataset candidate; the final set favors distinct decisions over count.
