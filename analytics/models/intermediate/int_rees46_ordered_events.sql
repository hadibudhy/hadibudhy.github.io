{{ config(materialized='table') }}
with ranked_events as (
    select *, row_number() over (partition by logical_event_id order by source_row_number, event_id) as duplicate_number
    from {{ ref('stg_rees46_events') }}
    where user_session is not null
), valid_sessions as (
    select user_session
    from ranked_events
    group by 1
    having count(distinct user_id) = 1
), valid_events as (
    select ranked_events.*
    from ranked_events
    inner join valid_sessions using (user_session)
    where duplicate_number = 1
)
select
    *,
    row_number() over (partition by user_session order by event_time, source_row_number, event_id) as event_number,
    lag(event_type) over (partition by user_session order by event_time, source_row_number, event_id) as previous_event_type
from valid_events
