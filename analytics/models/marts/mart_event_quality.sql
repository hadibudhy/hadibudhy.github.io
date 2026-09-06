{{ config(materialized='table') }}
select
    count(*) as source_rows,
    count(distinct event_id) as distinct_event_ids,
    count(*) - count(distinct event_id) as duplicate_event_ids,
    count(*) - count(distinct logical_event_id) as exact_duplicate_rows,
    count(*) filter (where user_session is null) as missing_session_rows,
    (select count(*) from (select user_session from {{ ref('stg_rees46_events') }} where user_session is not null group by 1 having count(distinct user_id) > 1)) as multi_user_sessions,
    (select count(*) from (select user_session from {{ ref('stg_rees46_events') }} where user_session is not null group by 1 having max(event_time) - min(event_time) > interval 24 hour)) as sessions_over_24_hours,
    min(event_time) as first_event_at,
    max(event_time) as last_event_at
from {{ ref('stg_rees46_events') }}
