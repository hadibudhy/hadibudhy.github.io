---
title: "Financial Metrics: Building a Reconciled Company Performance Mart"
date: 2026-09-05
categories: [analytics engineering]
tags: [financial metrics, SEC data, dimensional modeling, data quality]
excerpt: "A filing-aware metric model that keeps reported periods, units, and restatements visible before financial trends reach a dashboard."
problem: "Finance and product leaders need a consistent view of revenue, net income, and margin, but public filing data contains multiple facts, units, periods, and restated values."
result: "The model treats each reported fact as evidence with source context, then selects a documented annual view instead of assuming that the latest value is automatically comparable."
featured: true
kind: completed
artifactLabel: Engineering
published: true
caseId: financial-metrics
primaryTrack: analytics-engineering
secondaryTracks: [product-analytics]
displayOrder: 20
evidenceManifest: /data/evidence/financial-metrics.json
evidenceVisuals:
  - /images/sec-revenue-net-income.png
  - /images/sec-net-margin.png
  - /images/portfolio-sec-fact-grain.svg
header:
  teaser: /images/sec-revenue-net-income.png
---
## Project snapshot

- **Built:** Built a filing-aware annual metric mart that retains period, unit, tag, and filing context.
- **Stack:** Python, DuckDB, dbt, SQL, pytest
- **Result:** From FY2023 to FY2025, reported revenue rose from $211.9B to $281.7B and net margin from 34.1% to 36.1%.
- **Recommendation:** Use approved metric definitions and period/unit rules, retain filing identity, and reconcile selected annual values before dashboarding.
- **Code:** [dbt models](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/analytics/models) and [SEC loader](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/analytics/load_sec_company_facts.py)

## Business question

Finance and product leaders need a consistent view of revenue, net income, and margin. SEC filings contain multiple facts, periods, units, and amendments, so a dashboard can show a precise trend built from values that are not comparable.

The decision is whether the annual figures are consistent enough to support an executive trend view. This analysis uses Microsoft’s public filings; it does not represent an internal finance system.

## Data and preparation

The source is the [SEC Company Facts API](https://www.sec.gov/edgar/sec-api-documentation). Each fact includes a tag, unit, period, filing date, and value. The selected view uses documented annual facts for Microsoft and keeps quarterly and annual facts separate.

The checks cover unit compatibility, annual period selection, duplicate fact context, margin reconciliation, and source lineage. The evidence manifest records the source hash and period rule.

## Stakeholder questions

- **Did revenue and net income rise together?** Yes. Revenue rose from $211.9 billion to $281.7 billion. Net income rose from $72.4 billion to $101.8 billion.
- **Did reported net margin change?** It rose from 34.1% in FY2023 to 36.1% in FY2025.
- **Can these values explain product performance?** No. The source supports reported company-level trends, not product or customer drivers.

## Findings

### Revenue and net income both rose

![Microsoft reported results, FY2023–FY2025: revenue rose from $211.9 billion to $281.7 billion while net income rose from $72.4 billion to $101.8 billion](/images/sec-revenue-net-income.png)

Both measures increased across the selected fiscal years. Revenue shows scale; net income shows what remained after reported costs. Together they give a fuller performance picture than revenue alone.

### Reported net margin improved slightly

![Microsoft reported net margin rose from 34.1% in FY2023 to 36.1% in FY2025; the vertical scale starts at zero](/images/sec-net-margin.png)

Selected net income divided by selected revenue rose from 34.1% to 36.1%. The full zero-based scale keeps that change in proportion. This company-level result does not explain which products or costs drove it.

### Filing context is part of the metric

![SEC Company Facts grain: each reported value retains its tag, unit, fiscal period, and filing identity for audit](/images/portfolio-sec-fact-grain.svg)

Keeping the source context makes it possible to review why each value was selected instead of relying on an undocumented spreadsheet cell.

### A worked tie-out shows why filing identity stays attached

For FY2024, the selected revenue fact is **$245.122 billion** under `RevenueFromContractWithCustomerExcludingAssessedTax`, for 1 July 2023 through 30 June 2024. The same period and value appear in the FY2024, FY2025, and FY2026 10-K filings (filed 30 July 2024, 30 July 2025, and 29 July 2026). Net income is **$88.136 billion** in those filings, so the reconciled net margin is **35.96%**. The tie-out found no value change; it confirms that repeated comparative facts should not be counted as separate periods.

| Fiscal period | Selected tag | Value | Filing context | Treatment |
|---|---|---:|---|---|
| FY2024 revenue | `RevenueFromContractWithCustomerExcludingAssessedTax` | $245.122B | FY2024, FY2025, and FY2026 10-Ks | Keep one FY2024 period; retain all filing references |
| FY2024 net income | `NetIncomeLoss` | $88.136B | FY2024, FY2025, and FY2026 10-Ks | Reconcile on the same period and unit |
| FY2024 net margin | Derived | 35.96% | $88.136B ÷ $245.122B | Calculate only after period and unit alignment |

## Built

The model preserves each reported fact and its filing context. It selects annual revenue and net income, calculates net margin, and reconciles the ratio to the selected facts.

## Result

The selected annual metrics show revenue rising from $211.9 billion to $281.7 billion and net income from $72.4 billion to $101.8 billion between FY2023 and FY2025; net margin rose from 34.1% to 36.1%. The evidence supports reported company-level trends, not product, customer, or causal operating conclusions.

**Recommendation:** publish a small finance mart with approved metric definitions, period rules, units, and source links. Store filing identity with each fact, deduplicate repeated comparative periods, and reconcile the selected annual values before connecting the mart to planning or dashboards. Alert when a later filing changes a selected historical value; extend to quarterly or operating measures only after definitions are agreed.


## Data lineage and model checks

```text
SEC Company Facts JSON
  ↓ analytics/load_sec_company_facts.py
DuckDB raw.company_facts
  ↓ dbt staging
stg_sec_company_facts
  ↓ dbt mart
mart_financial_metrics
```

This excerpt from `analytics/models/marts/mart_financial_metrics.sql` selects one filing context per fiscal year before choosing reported metrics:

```sql
with annual_facts as (
    select *
    from {{ ref('stg_sec_company_facts') }}
    where fiscal_period = 'FY'
      and unit = 'USD'
      and form in ('10-K', '10-K/A')
      and period_start is not null
      and period_end is not null
      and date_diff('day', period_start, period_end) between 300 and 380
), filing_candidates as (
    select distinct fiscal_year, accession, filed_date
    from annual_facts
), chosen_filing as (
    select fiscal_year, accession
    from (
        select
            *,
            row_number() over (partition by fiscal_year order by filed_date desc nulls last, accession desc) as filing_rank
        from filing_candidates
    ) ranked_filings
    where filing_rank = 1
)
```

| Test | Protection |
|---|---|
| `stg_sec_company_facts` schema tests | Fact ID is unique and required fields, including fiscal year, value, accession, and form, are present. |
| `mart_financial_metrics` schema tests | Fiscal year is unique and required; revenue and net income are present. |
| `assert_financial_metrics_are_reconciled.sql` | Revenue is positive; net income and net margin are not null. |
| `test_sec_fact_loader_preserves_one_row_per_reported_observation` | The loader preserves each reported fact row and its form. |
| `test_sec_loader_writes_a_queryable_raw_relation` | Loaded facts are available in the DuckDB raw relation. |

The SQL test checks positive and present values; the filing selection and FY2024 tie-out are documented in the evidence manifest. CI verifies the manifest and chart hashes but does not recalculate this full-source tie-out.

[View the dbt models](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/analytics/models).

## What this can't tell you

> SEC facts support reported company-level trends, not product or customer drivers, causal operating results, or internal operations. Period, unit, tag, and filing choices remain part of each measure.

## Technical appendix

The evidence manifest records the SEC source, annual period rule, validation checks, and chart hashes. No raw filing payloads or private business data are published.
