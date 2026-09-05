{{ config(materialized='view') }}
select
    cast(request_id as varchar) as request_id,
    cast(created_at as timestamp) as created_at,
    try_cast(closed_at as timestamp) as closed_at,
    cast(status as varchar) as status,
    cast(agency as varchar) as agency,
    cast(complaint_type as varchar) as complaint_type,
    nullif(cast(borough as varchar), '') as borough
from {{ source('nyc311', 'requests') }}
