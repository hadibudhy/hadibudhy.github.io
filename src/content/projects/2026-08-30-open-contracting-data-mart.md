---
title: "Open Contracting: Make Procurement Data Usable Before Scoring Red Flags"
date: 2026-08-30
categories: [analytics engineering]
tags: [procurement, OCDS, data quality, governance]
excerpt: "A procurement-data mart design that preserves the lifecycle of a public contract and makes missing stages visible before anyone ranks supplier or integrity risk."
problem: "Procurement analysts want to compare competition, awards, and delivery, but public contracting data arrives as nested releases with different stages and publisher-specific completeness."
result: "The Open Contracting Data Standard links planning, tender, award, contract, and implementation releases with an OCID; it provides a real shared model for a governed procurement mart."
published: true
---

## Business question

Can a procurement team compare competition and delivery across publishers without mistaking missing implementation data for a clean contract outcome?

## Why it matters

A red-flag score built from incomplete lifecycle data can unfairly target suppliers or buyers. The first decision is whether the data is complete enough to support a comparison.

## Decision brief

- **Recommendation:** build a release-level ingestion and record-level semantic layer that exposes stage coverage and data-quality status before calculating indicators.
- **Evidence:** the [Open Contracting Data Standard](https://www.open-contracting.org/data-standard/) is a free, non-proprietary model used by 50+ governments and links contracting stages through a unique OCID.
- **Evidence strength:** High for the data-model decision; low for any integrity conclusion without a publisher-specific completeness audit.
- **Main risk:** publisher coverage, field definitions, currency, procurement law, and missing implementation updates differ across jurisdictions.
- **Next test:** select one publisher, validate release-to-record joins, and reconcile a sample to public notices before comparing suppliers.

## Role

Role: nested-data modeling, contract-grain definition, schema validation, completeness metrics, and responsible analytics design.

## Data used

The project uses datasets from the [OCP Data Registry](https://data.open-contracting.org/en/search/) in the [OCDS format](https://standard.open-contracting.org/latest/en/guidance/build/hosting/). OCDS publishes releases as immutable events and uses an `ocid` to connect the procurement process. The record grain is a procurement process; the release grain is an event in that process.

The data is real public procurement information, but it is not a complete view of every purchase or supplier relationship.

## Approach

1. Store raw release packages without flattening away event identity.
2. Validate `ocid`, release IDs, dates, parties, values, and stage tags.
3. Build process-level tables for tender, award, contract, and implementation.
4. Publish stage coverage and missingness by publisher, buyer, and time.
5. Only then calculate competition, amendment, and delivery indicators.

## Key findings

## Visual evidence

### Context: a contract is a lifecycle of releases

![Open Contracting lifecycle: planning, tender, award, contract, and implementation connected through an OCID](/images/portfolio-ocds-lifecycle.svg)

The standard’s process model is the foundation for a trustworthy procurement mart.

### Main finding: missing implementation data is an uncertainty state

![Open Contracting evidence boundary: OCID-linked releases and parties are observed, while complete payments and proven misconduct are not](/images/portfolio-ocds-boundary.svg)

The visual prevents missing data from being interpreted as a clean outcome.

### Decision: profile completeness before red-flag scoring

![Conceptual Open Contracting data gate: ingest immutable releases, profile stage completeness, then send lineage-backed indicators to review](/images/portfolio-ocds-gate.svg)

This makes data quality part of the procurement decision.

### A procurement process is not one row

A release represents an event, while a record represents the joined contracting process.

**Meaning:** collapsing every release into one latest row can erase amendments and process history.

**Why it matters:** audit and delivery questions need event lineage.

### Missing stages are decision-relevant

A publisher may have strong tender and award coverage but little implementation or payment data.

**Meaning:** absence of a field is not evidence of no amendment, no payment, or no delivery problem.

**Why it matters:** the mart must display completeness alongside every KPI.

### A red flag is a prompt for review

High concentration, a single bidder, or an amendment can have legitimate explanations.

**Meaning:** indicators prioritize human review; they do not prove corruption or poor value.

**Why it matters:** the output needs an explanation trail and appeal path.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | OCDS releases connect planning, tender, award, contract, and implementation events through an OCID | Build process and stage-completeness views |
| Inferred | A red-flag score is only useful after publisher completeness is visible | Prioritize data-quality work first |
| Not established | A single bidder, amendment, or concentration proves misconduct | Send indicators to human review |

## Validation record

- **Grain:** immutable release and procurement process; releases are events, records are joined processes.
- **Checks:** OCIDs, release IDs, stage tags, dates, parties, values, and publisher completeness are validated.
- **Guardrail:** missing implementation data is not converted to “no implementation issue.”

## Recommendation

**What:** ship the ingestion and completeness layer before a supplier-risk score.

**Where / who:** begin with one OCP publisher and one procurement category so semantics can be reconciled.

**Why:** trustworthy coverage is a prerequisite for fair comparison.

**Risk:** standardization can hide local legal and workflow differences.

**Next action:** agree with procurement owners on the minimum evidence required for a review flag and publish source lineage with each flag.

## Evidence strength and limitations

The standard supports consistent modeling, not complete data. Cross-country comparisons can be confounded by laws, thresholds, reporting practices, and currency. No integrity or savings claim is made from the schema alone.

## Reproducibility

Sources: [OCP Data Registry](https://data.open-contracting.org/en/search/) and [OCDS data guidance](https://www.open-contracting.org/data/data-use/). The [expansion validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md) records the stage and grain rules.

## Technical appendix

The core contracts are `stg_release`, `fct_procurement_process`, `fct_award`, `fct_contract_amendment`, and `dq_process_completeness`. Every indicator stores the source `ocid`, release IDs, publisher, retrieval date, and completeness status.
