{{ config(materialized='table') }}
with annual_facts as (
    select *
    from {{ ref('stg_sec_company_facts') }}
    where fiscal_period = 'FY'
      and unit = 'USD'
), selected as (
    select
        fiscal_year,
        max(case when tag in ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax') then value end) as revenue,
        max(case when tag = 'NetIncomeLoss' then value end) as net_income
    from annual_facts
    group by 1
)
select
    fiscal_year,
    revenue,
    net_income,
    case when revenue is null or revenue = 0 then null else net_income / revenue end as net_margin
from selected
where revenue is not null and net_income is not null
