{{ config(materialized='table') }}
with annual_facts as (
    select *
    from {{ ref('stg_sec_company_facts') }}
    where fiscal_period = 'FY'
      and unit = 'USD'
), normalized as (
    select
        fiscal_year,
        filed_date,
        accession,
        case
            when tag in ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax') then 'revenue'
            when tag = 'NetIncomeLoss' then 'net_income'
        end as metric_name,
        value
    from annual_facts
    where tag in ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'NetIncomeLoss')
), ranked as (
    select
        *,
        row_number() over (partition by fiscal_year, metric_name order by filed_date desc nulls last, accession desc nulls last) as metric_rank
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
