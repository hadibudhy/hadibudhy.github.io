{{ config(materialized='table') }}
select
    *,
    row_number() over (partition by user_session order by event_time, source_row_number, event_id) as event_number,
    lag(event_type) over (partition by user_session order by event_time, source_row_number, event_id) as previous_event_type
from {{ ref('stg_rees46_events') }}
where user_session is not null
