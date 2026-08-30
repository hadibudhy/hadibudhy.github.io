---
title: "SEC Company Facts: Build a Filing-Aware Finance Mart Before Comparing Growth"
date: 2026-08-30
categories: [analytics engineering]
tags: [SEC, XBRL, data modeling, finance]
excerpt: "An analytics-engineering design for turning issuer-level XBRL facts into a comparable metric mart without hiding units, fiscal periods, restatements, or taxonomy changes."
problem: "Finance stakeholders want comparable growth and margin metrics, but raw XBRL facts mix tags, units, filing forms, fiscal periods, and amended facts."
result: "The SEC Company Facts API exposes issuer facts with taxonomy tags, units, filing forms, accession metadata, and periods; the correct deliverable is a governed metric layer, not a blind sum of reported values."
published: true
---

## Business question

Can an analyst reuse reported company facts across issuers and periods without producing a metric that looks precise but mixes incompatible filings?

## Why it matters

A wrong finance metric can change an investment or management narrative. The failure is often upstream: a restatement, unit mismatch, quarter-versus-year period, or taxonomy tag is treated as if it were interchangeable.

## Decision brief

- **Recommendation:** build a filing-aware Bronze/Silver/Gold model with explicit fact selection, unit normalization, period logic, and lineage.
- **Evidence:** the [SEC Company Facts API](https://www.sec.gov/data-research/sec-api-documentation) returns company-level XBRL facts and filing metadata for public issuers.
- **Evidence strength:** High for the engineering contract; metric comparability remains conditional on tag and period validation.
- **Main risk:** taxonomy changes, amended filings, fiscal-year differences, and multiple valid tags can create silent inconsistencies.
- **Next test:** reconcile a small issuer set to filed statements and have finance sign off on metric definitions before scaling.

## Role

Role: source profiling, dimensional modeling, metric-contract design, data-quality tests, lineage, and implementation planning.

## Data used

The [SEC Company Facts API](https://www.sec.gov/data-research/sec-api-documentation) publishes JSON facts by issuer and taxonomy. Facts carry a tag, unit, value, form, filing date, accession number, fiscal period, and start/end dates where relevant. The source is official public filing data, not a pre-cleaned finance warehouse.

## Approach

1. Land raw issuer JSON unchanged with retrieval metadata.
2. Normalize facts into one row per issuer × taxonomy × tag × unit × period × filing.
3. Select approved tags and units through a metric-definition table.
4. Resolve annual versus quarterly periods and amended filings explicitly.
5. Test totals, signs, units, period overlap, and reconciliation to a filed statement.

## Key findings

### XBRL is structured, not automatically comparable

Two issuers can report similar concepts under different tags or units.

**Meaning:** a column called `revenue` is a governed business definition, not a raw source field.

**Why it matters:** the semantic model needs approved mappings and an exception queue.

### Period logic is part of the metric

An annual duration fact and a quarterly duration fact cannot be compared without fiscal-period logic.

**Meaning:** the same value can tell a different story depending on its start and end dates.

**Why it matters:** the mart should expose period type, fiscal year, fiscal quarter, and coverage days.

### Restatements are lineage events

Amended filings and later revisions can change a reported fact.

**Meaning:** replacing an old value without preserving its accession and filing date destroys auditability.

**Why it matters:** consumers need to know whether a report is “as originally filed” or “latest available.”

## Recommendation

**What:** ship a narrow approved metric set first: revenue, net income, and a derived margin with source lineage.

**Where / who:** use a small group of issuers and fiscal-year shapes for reconciliation before onboarding more companies.

**Why:** the highest value is trustworthy reuse, not maximum tag coverage.

**Risk:** an elegant mart can create false confidence if the finance definition is not approved.

**Next action:** publish data contracts, reconcile each metric to statement totals, and monitor new taxonomy or filing exceptions.

## Evidence strength and limitations

This is an analytics-engineering case study, not an investment recommendation. SEC filings are authoritative records of what issuers reported, but they do not make companies economically comparable or explain operating drivers by themselves.

## Reproducibility

Source documentation: [SEC API documentation](https://www.sec.gov/data-research/sec-api-documentation). The [portfolio expansion validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md) records source, grain, and test requirements.

## Technical appendix

The proposed tables are `raw_company_facts`, `stg_xbrl_facts`, `dim_metric_definition`, and `fct_reported_metric`. Every gold metric retains accession number, filing date, source tag, unit, fiscal period, and a quality status.

