# Audit of the remaining 29 project articles

Audit date: 6 September 2026. The repository contains 35 project articles. Six are published flagships and passed the senior capability gate. The other 29 were reviewed with their article, visuals, scripts, source notes, and project folders. None currently meets the 80/100 flagship threshold without inventing evidence or duplicating a stronger case.

## Gate decision

All 29 articles below remain archived from the website with `published: false`. “Archive” means the work stays available for reference and future redevelopment, but it is not presented as completed senior-level evidence. A future promotion requires an executed analysis, trustworthy metrics, supporting validation, a decision owner, and a measurement plan.

| Project | Score | Supporting work inspected | Main evidence gap | Final disposition |
|---|---:|---|---|---|
| Customer value metrics (MDS) | 63 | Article and metric-governance discussion | No executable lineage, reconciliation result, metric owner, or incident evidence | Archive; replace with Product Events and Financial Metrics |
| Netflix content strategy | 62 | Article and three conceptual visuals | Catalog availability cannot measure viewing demand, retention, or a content decision | Archive |
| Fake job detection | 76 | Article and model-comparison chart generator | No calibrated production threshold, review capacity baseline, fairness review, or live outcome | Archive |
| World Happiness | 65 | Article, longitudinal charts, public-source notes | No controllable product decision or credible intervention design | Archive |
| Restaurant quality | 73 | Article and inspection-risk chart generator | Descriptive risk concentration lacks an executed intervention and verified resolution outcome | Archive |
| NYC taxi operations | 74 | Article and completed-trip chart generator | Duplicates the marketplace story and lacks requests, lost matches, and online supply | Archive; merge concept into Marketplace |
| Clickstream product funnel | 66 | Article and conceptual funnel visuals | No stable identity, ordered event model, or trustworthy product funnel result | Archive; replace with Product Events |
| Bank marketing efficiency | 66 | Article and UCI source downloader | Observational response cannot estimate incremental value or profitable targeting | Archive; replace with Criteo |
| Airfare pricing context | 59 | Article and benchmark discussion | No executed demand, price-response, margin, or experiment evidence | Archive |
| SEC company performance | 69 | Article and company-performance visuals | Duplicates the filing-aware Financial Metrics case and lacks stronger period controls | Archive; merge into Financial Metrics |
| Airbnb marketplace health | 68 | Article and source-download notes | Listings do not observe bookings, availability, demand, or guest outcome | Archive |
| JOLTS workforce planning | 64 | Article and JOLTS chart generator | Macro series cannot identify a controllable team, workflow, or workforce intervention | Archive |
| Credit default risk | 72 | Article and UCI source-download notes | No calibration, operating threshold, fairness review, intervention result, or cost model | Archive |
| ComplaintFlow AI triage | 76 | Article, workflow visuals, and synthetic fixture documentation | Fixture validates software behavior, not real routing quality, reviewer burden, or customer impact | Archive |
| Census market expansion | 62 | Article and three conceptual visuals | Market structure is a screening input, not executed demand validation or incremental outcome | Archive |
| Citi Bike station experience | 68 | Article and station-flow conceptual visuals | No validated station-status panel, failed-search outcome, or completed rebalancing test | Archive |
| FAA service-difficulty triage | 58 | Article and safety-triage conceptual visuals | No exposure denominator, calibrated risk, or evidence that automated routing improves safety review | Archive |
| FCC complaint routing | 60 | Article and routing conceptual visuals | Complaint selection and unverified allegations cannot support provider or routing performance claims | Archive |
| Google Analytics revenue | 65 | Article and historical-window conceptual visuals | No executed user-value analysis or incremental acquisition result | Archive |
| Instacart reorder growth | 68 | Article, relational-data visuals, and proposed holdout | No executed sequence analysis, opportunity sizing, or incremental reorder result | Archive |
| MovieLens recommendation coverage | 61 | Article and offline recommendation visuals | Offline ratings cannot establish online engagement, retention, or commercial impact | Archive |
| NYC 311 response capacity | 68 | Article and conceptual capacity visuals | Methods duplicate the completed 311 service case without a separate executed result | Archive; merge into Service Metrics |
| Olist delivery marketplace | 64 | Article and relational-data visuals | Overused source and no executed root-cause or current intervention result | Archive |
| Online Shoppers activation | 76 | Article, `scripts/analyze_online_shoppers.py`, and verified metrics | Session contrast is descriptive; timing, product mechanism, and incremental activation remain unobserved | Archive |
| Open Contracting data mart | 65 | Article and lifecycle conceptual visuals | No implemented transformation, source contract, reliability result, or procurement decision | Archive |
| SEC XBRL data mart | 74 | Article and fact-grain visuals | Methods duplicate the implemented Financial Metrics mart without a separate decision result | Archive; merge into Financial Metrics |
| Stack Overflow developer adoption | 64 | Article and survey conceptual visuals | Survey attitudes cannot measure product adoption, activation, or an intervention outcome | Archive |
| Wikimedia content discovery | 63 | Article, API-boundary visuals, and conceptual queue | Pageviews do not identify readers, retention, comprehension, or causal refresh impact | Archive |
| Congestion pricing causal audit | 79 | Full growth-analytics folder, zone validation, comparator audit, and event-study code | The validated public comparator fails the evidence needed for a defensible causal claim | Archive until a valid design or better panel exists |

## Why the archive decision is correct

The articles are not being rejected because the topics are uninteresting. They are archived because the available evidence stops before a senior decision. The published flagships also propose follow-up experiments, but each one first contains a completed, reproducible analysis with an evidence-backed decision. The archived articles do not yet provide that completed evidence, or they duplicate a stronger published case. Publishing them as flagships would create one of four risks:

- presenting a descriptive pattern as a business result;
- claiming causality without a valid comparison or assignment mechanism;
- presenting a proposed architecture or experiment as implemented evidence; or
- repeating a stronger published case with a weaker dataset.

The six published flagships cover the strongest completed evidence:

1. Product Events: event grain, ordered funnel, data quality, and product experiment.
2. Financial Metrics: filing-aware period logic, metric contract, reconciliation, and lineage.
3. NYC 311 Service Metrics: mature intake cohort, closure coverage, censoring boundary, and capacity test.
4. Online Retail Retention: common eligible cohorts, segmentation, opportunity sizing, and holdout design.
5. Criteo Incrementality: randomized assignment, uncertainty, exploratory heterogeneity, and economics gate.
6. TLC Marketplace: completed-trip friction diagnosis, proxy boundary, stable-window prioritization, and switchback design.

## Promotion criteria

An archived article can return to the public case-study library only when it has:

1. a real decision owner and a measurable outcome;
2. a validated source, grain, denominator, and data-quality report;
3. executed diagnostic analysis beyond descriptive charts;
4. evidence that separates findings from hypotheses and causal claims;
5. a quantified opportunity or risk with assumptions;
6. a prioritized recommendation with trade-offs and guardrails; and
7. a reproducible measurement or experiment plan.

The archive is therefore a quality gate, not a claim that the underlying idea has no value.

## Score interpretation

The screening scores in `SENIOR_CAPABILITY_AUDIT.md` are weighted review judgments, not measured facts. The rubric is: problem framing 10%, metric design 10%, data understanding and validation 10%, analytical depth 15%, root-cause reasoning 15%, technical implementation 10%, decision quality 15%, opportunity sizing 5%, communication 5%, and limitations/rigor 5%. Each dimension is anchored as follows:

- **0–3:** absent, misleading, or unsupported;
- **4–5:** partial treatment or a proposed method without executed evidence;
- **6–7:** useful analysis with a material senior-level gap; and
- **8–10:** executed, decision-relevant, validated, and appropriately bounded evidence.

The publication gate uses the evidence and disposition, not a claim of false numerical precision. An archived project remains archived until a new analysis pass can document enough evidence to score at least 80 under these anchors.
