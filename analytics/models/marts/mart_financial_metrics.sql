{{ config(materialized='table') }}
with annual_facts as (
    select *
    from {{ ref('stg_sec_company_facts') }}
    where fiscal_period = 'FY'
      and unit = 'USD'
      and form in ('10-K', '10-K/A')
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
), normalized as (
    select
        facts.fiscal_year,
        facts.period_end,
        facts.accession,
        case
            when facts.tag in ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax') then 'revenue'
            when facts.tag = 'NetIncomeLoss' then 'net_income'
        end as metric_name,
        case when facts.tag = 'Revenues' then 1 else 2 end as tag_priority,
        facts.value
    from annual_facts as facts
    inner join chosen_filing using (fiscal_year, accession)
    where facts.tag in ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'NetIncomeLoss')
), ranked as (
    select
        *,
        row_number() over (partition by fiscal_year, metric_name order by tag_priority, period_end desc nulls last) as metric_rank
    from normalized
), selected as (
    select
        fiscal_year,
        max(case when metric_name = 'revenue' then value end) as revenue,
        max(case when metric_name = 'net_income' then value end) as net_income
    from ranked
    where metric_rank = 1
    group by 1
)
select
    fiscal_year,
    revenue,
    net_income,
    case when revenue is null or revenue = 0 then null else net_income / revenue end as net_margin
from selected
where revenue is not null and net_income is not null
