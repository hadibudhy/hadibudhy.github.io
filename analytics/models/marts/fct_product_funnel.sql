{{ config(materialized='table') }}
select
    date_trunc('day', event_time) as event_date,
    event_type,
    count(*) as event_count,
    count(distinct user_session) as sessions,
    count(distinct user_id) as users,
    count(distinct case when user_session is not null then user_session end) as identified_sessions
from {{ ref('stg_rees46_events') }}
group by 1, 2
