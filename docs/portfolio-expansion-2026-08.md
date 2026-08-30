# Portfolio expansion: 14 source-grounded decision pages

Build date: 2026-08-30

This expansion adds 14 published source-grounded pages to the existing portfolio. The set is intentionally decision-led: each page starts with a business choice, states what the public data can measure, separates observation from inference, and ends with a bounded next action. The current repository classifies zero pages as completed analyses and 14 as methods/design studies because no checked-in dataset and runnable project-specific computation are available for these expansion pages. No dummy, synthetic, placeholder, or generic sample dataset is used as claimed evidence in these 14 pages.

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
| Online Shoppers activation | Review flag: evidence boundary needed tightening | Numeric visual values were not backed by a source-specific runnable computation | Reclassified as methods/design; removed numeric claims and retained leakage-aware experiment design | 9 / 9 / 9 / 9 | Pass |
| Instacart reorder growth | Review flag: evidence ledger and join contract needed tightening | Findings were directionally right but lacked an explicit evidence ledger and join contract | Added table-grain evidence register and order/product validation rules | 9 / 9 / 9 / 9 | Pass |
| Google Merchandise acquisition | Review flag: historical value and leakage boundary needed tightening | Historical value boundary and target leakage control were not visible near the decision | Added visit/user evidence register and temporal validation record | 9 / 9 / 9 / 9 | Pass |
| Wikimedia discovery | Review flag: aggregate persistence boundary needed tightening | Aggregate persistence could be mistaken for reader retention | Added API-grain evidence register and no-double-counting checks | 9 / 9 / 9 / 9 | Pass |
| MovieLens recommendation coverage | Review flag: offline/online evidence boundary needed tightening | Offline relevance versus online engagement needed a sharper evidence boundary | Added rating-grain ledger, time-split checks, and separate coverage guardrail | 9 / 9 / 9 / 9 | Pass |
| Stack Overflow developer adoption | Review flag: survey/product boundary needed tightening | Survey insight and product adoption were not separated in a compact artifact | Added question-denominator evidence register and nonresponse checks | 9 / 9 / 9 / 9 | Pass |
| Citi Bike station experience | Review flag: trip/snapshot grain needed tightening | Trip history and station-status grain needed a visible separation | Added ride/snapshot evidence register and directional-flow validation record | 9 / 9 / 9 / 9 | Pass |
| Olist delivery marketplace | Review flag: multi-table join contract needed tightening | Multi-table delivery evidence needed an explicit join and missing-date contract | Added order/child-table ledger and missing-delivery validation rules | 9 / 9 / 9 / 9 | Pass |
| Census expansion markets | Review flag: screen/forecast boundary needed tightening | Market screening could be mistaken for a revenue forecast | Added county/NAICS evidence register and suppression guardrail | 9 / 9 / 9 / 9 | Pass |
| NYC 311 response capacity | Review flag: closure/resolution boundary needed tightening | Closure time versus resolution quality needed a compact distinction | Added request-level evidence register and open-backlog validation record | 9 / 9 / 9 / 9 | Pass |
| SEC XBRL finance mart | Review flag: engineering quality gates needed a tighter decision artifact | Engineering quality gates were described but not summarized beside the decision | Added fact-grain evidence register and accession/period checks | 9 / 9 / 9 / 9 | Pass |
| Open Contracting data mart | Review flag: release/process boundary needed tightening | Release versus process and missing-stage risk needed a sharper artifact | Added OCID/release evidence register and completeness checks | 9 / 9 / 9 / 9 | Pass |
| FAA Service Difficulty triage | Review flag: workflow/safety boundary needed tightening | Workflow assistance could be confused with safety-rate or airworthiness claims | Added report-grain evidence register and critical-case evaluation guardrail | 9 / 9 / 9 / 9 | Pass |
| FCC complaint routing | Review flag: routing/prevalence boundary needed tightening | Routing usefulness needed separation from provider prevalence claims | Added complaint-grain evidence register, PII, drift, and correction checks | 9 / 9 / 9 / 9 | Pass |

The expansion pages passed the evidence-boundary gate; Online Shoppers is intentionally recorded as a methods/design page rather than a completed analysis because source-specific computation is not checked in.

## Stakeholder review gate

This review was run independently for every project using the five requested perspectives. Each cell records, in compressed form, first impression; what works; what is weak or missing; credibility; recommendation usefulness; judgment signal; and interview likelihood. Scores are editorial review scores, not external endorsements.

| Project | Recruiter | Hiring Manager | Data Manager | Country Manager | Business Stakeholder |
|---|---|---|---|---|---|
| Online Shoppers activation | **8** — clear activation design; numeric evidence removed until reproducible; useful interview hook | **8** — leakage and A/B boundary are strong; no source-specific computation; credible next test | **7** — source grain is explicit; runnable pipeline remains absent; classification is honest | **8** — test design is easy to localize; market context absent; recommendation is testable | **8** — prompt decision, risk, and guardrails are clear; internal economics still needed |
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

The stakeholder review records mostly 8–9/10 scores. Online Shoppers is lower on reproducibility because no source-specific runnable computation is checked in; that limitation is documented rather than hidden. The published pages state their grain, evidence boundary, validation contract, and reproducibility source explicitly.

## Visual publishing gate

The visual gate applies to all 20 currently published projects, including the six published before this expansion. Flagship and completed pages use distinct context, evidence, and decision visuals; methods/design pages use source, evidence-boundary, and design visuals where available. Online Shoppers retains one conceptual experiment visual after its unreproducible numeric visuals were removed. Numeric visuals use validated source values; workflow diagrams are visibly labelled as conceptual and do not imply measured outcomes.

| Project | Visual set | Visual review result | Recruiter | Hiring Manager | Data Manager | Country Manager | Business Stakeholder | Gate |
|---|---|---|---:|---:|---:|---:|---:|---|
| Restaurant quality | Grades, borough risk, inspection triage | 3 useful views; missing grade remains visible; no causal ranking | 9 | 9 | 9 | 9 | 9 | Pass |
| Online retail growth | Revenue trend, market mix, identity cleaning | 3 useful views; units and customer denominator remain separate | 9 | 9 | 9 | 9 | 9 | Pass |
| ComplaintFlow AI | Architecture, audit log, evidence boundary | 3 useful views; synthetic fixture is labelled validation-only | 9 | 9 | 9 | 9 | 9 | Pass |
| Online Shoppers activation | Activation experiment design | One conceptual design view remains; numeric visuals removed pending reproducible computation | 8 | 8 | 8 | 8 | 8 | Pass |
| Instacart reorder growth | Data scale, evidence boundary, holdout design | 3 useful views; relational grain and missing economics visible | 9 | 9 | 9 | 9 | 9 | Pass |
| Google Merchandise acquisition | Time windows, user aggregation, budget holdout | 3 useful views; historical target boundary is explicit | 9 | 9 | 9 | 9 | 9 | Pass |
| Wikimedia discovery | API grain, persistence boundary, content queue | 3 useful views; pageviews are not called unique readers | 9 | 9 | 9 | 9 | 9 | Pass |
| MovieLens recommendation | Dataset scale, offline boundary, online test | 3 useful views; ratings are not called watch engagement | 9 | 9 | 9 | 9 | 9 | Pass |
| Stack Overflow adoption | Audience mix, age context, telemetry test | 3 useful views; question-specific denominator is visible | 9 | 9 | 9 | 9 | 9 | Pass |
| Citi Bike experience | Data grains, directional flow, service test | 3 useful views; trip and station snapshot are separated | 9 | 9 | 9 | 9 | 9 | Pass |
| Olist delivery marketplace | Order scope, evidence boundary, operational pilot | 3 useful views; order/child joins and missing dates are explicit | 9 | 9 | 9 | 9 | 9 | Pass |
| Census market expansion | Market measures, suppression boundary, expansion screen | 3 useful views; suppression is not converted to zero | 9 | 9 | 9 | 9 | 9 | Pass |
| NYC 311 capacity | Source scale, closure boundary, capacity pilot | 3 useful views; administrative close is not resolution | 9 | 9 | 9 | 9 | 9 | Pass |
| SEC XBRL finance mart | Fact grain, comparability boundary, mart flow | 3 useful views; period/unit/filing lineage is visible | 9 | 9 | 9 | 9 | 9 | Pass |
| Open Contracting mart | Lifecycle, completeness boundary, data gate | 3 useful views; missing implementation is an uncertainty state | 9 | 9 | 9 | 9 | 9 | Pass |
| FAA Service Difficulty triage | Source scope, safety boundary, human review | 3 useful views; conceptual workflow cannot decide airworthiness | 9 | 9 | 9 | 9 | 9 | Pass |
| FCC complaint routing | Complaint scope, prevalence boundary, routing flow | 3 useful views; allegations are not presented as verified facts | 9 | 9 | 9 | 9 | 9 | Pass |
| Campaign incrementality | ITT economics, holdout design, uncertainty chart | 3 useful views; lift is separated from current CPA | 9 | 9 | 9 | 9 | 9 | Pass |
| Marketplace supply and demand | Hourly activity, monthly supply, measurement stack | 3 useful views; recorded trips are not total demand | 9 | 9 | 9 | 9 | 9 | Pass |
| MTA congestion audit | Event-study panel, causal boundary, comparator result | 3 useful views; failed pre-trend blocks causal attribution | 9 | 9 | 9 | 9 | 9 | Pass |

### Visual QA checklist

- **Analytical correctness:** validated values retain units, denominators, periods, and sample context; conceptual diagrams are marked and contain no invented measurements.
- **Business usefulness:** each set follows context → main finding or evidence boundary → decision.
- **Readability:** every visual has a conclusion-led title, source line, accessible SVG title/description, and page-level alt text.
- **Misleading scales:** no visual uses a truncated comparison axis; conceptual diagrams do not use quantitative axes.
- **Aggregation:** source grains are named in the visual or adjacent caption; child-table joins are not presented as independent business entities.
- **Causality:** no visual uses causal language for observational evidence; holdout and experiment diagrams are labeled designs.
- **Duplication:** each project has three different purposes, not three versions of the same metric.
- **Responsive check:** the representative project was checked at the narrow and desktop page layouts; image assets load after lazy-load scroll and the page has no horizontal overflow.

The visual assets are generated reproducibly by [scripts/generate_portfolio_visuals.py](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/scripts/generate_portfolio_visuals.py) from the cited project evidence and source metadata.

## Intentional exclusions

The dunnhumby “sort-of-real” release was rejected because the publisher describes it as dummy data. Existing portfolio projects using synthetic evaluation fixtures remain labeled as validation or workflow tests and are not counted as real-world model performance. A new project was also not created for every attractive dataset candidate; the final set favors distinct decisions over count.
