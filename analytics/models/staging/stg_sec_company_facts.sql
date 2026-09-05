{{ config(materialized='view') }}
select
    cast(fact_id as varchar) as fact_id,
    cast(tag as varchar) as tag,
    cast(unit as varchar) as unit,
    cast(fy as integer) as fiscal_year,
    cast(fp as varchar) as fiscal_period,
    nullif(cast(frame as varchar), '') as frame,
    try_cast(filed as date) as filed_date,
    try_cast(end_date as date) as period_end,
    try_cast(start_date as date) as period_start,
    try_cast(value as double) as value,
    cast(accession as varchar) as accession,
    cast(form as varchar) as form
from {{ source('sec', 'company_facts') }}
