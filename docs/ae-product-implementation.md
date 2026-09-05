# Analytics Engineer and Product Analyst implementation

Approved plan: six independent cases on local dbt Core + DuckDB.
Raw data -> staging -> intermediate -> facts/dimensions -> metric views -> evidence -> decisions.

## Work ledger

- [x] Shared pinned analytics environment definition, source acquisition path, dbt layers and tests.
- [x] REES46 product events, ordered funnel and proposed activation contract.
- [x] Microsoft filing-aware metrics and NYC311 current-state reliability.
- [x] Online Retail fixed-window retention, Criteo experiment metrics and TLC pickup experience.
- [x] Six-case publication manifests, evidence visuals, audit and plain-English articles.
- [x] Positioning, grouped homepage/library, About, metadata and publication validation.
- [ ] Full-data reruns, incremental parity, browser QA, independent review and deployment.

## Execution decisions

| Shared boundary | Producer / consumer | Rule |
|---|---|---|
| Evidence | analytics output / site loader | caseId, primaryTrack, evidenceManifest; explicit published:true |
| Models | ingestion / dbt | raw DuckDB schema, stable source keys, ingestion batches |
| Metrics | dbt / narratives/charts | published aggregates generated from marts; no hand-authored result chart data |
| Sources | historical snapshots / monitoring | retrieved_at is ingestion time, not source freshness or event time |
| Tests | QA fixtures / public results | fixtures validate behavior; full-data runs validate published findings |
| New cases | architecture / product findings | one case per business decision; no splitting one warehouse into extra cards |

Ruling: worktree creation, implementation, integration and deployment are authorized by the approved user plan.
Ruling: preserve the original checkout's ignored raw files using an explicit existing-data path; new downloads stay local.
Ruling: test scenarios may inject faults but are labeled engineering validation, never actual incidents or customer findings.
Ruling: one UI worker has a disjoint source write set while the main agent owns all analytics and project Markdown.

## Six cases

product-event-foundation (analytics-engineering), financial-metrics (analytics-engineering),
service-metric-reliability (analytics-engineering), customer-retention (product-analytics),
marketplace-experience (product-analytics), experiment-metrics (experimentation-growth).

## Global constraints

Historical job titles remain accurate. No interview copy, invented impact, fabricated events presented as customer data,
or restored methods-only projects. Preserve all archived code. Public source IDs and raw records stay outside static output.
Every page includes context, question, data, architecture, metric definitions, analysis, findings, recommendation,
measurement plan, implementation and limitations. Keep plain English and claim-specific evidence.
