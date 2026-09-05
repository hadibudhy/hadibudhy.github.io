{{ config(materialized='table') }}
select
    count(*) as source_rows,
    count(distinct event_id) as distinct_event_ids,
    count(*) - count(distinct event_id) as duplicate_event_ids,
    count(*) filter (where user_session is null) as missing_session_rows,
    min(event_time) as first_event_at,
    max(event_time) as last_event_at
from {{ ref('stg_rees46_events') }}
