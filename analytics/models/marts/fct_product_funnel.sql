{{ config(materialized='table') }}
with event_counts as (
    select
        date_trunc('day', event_time) as event_date,
        count(*) as event_count,
        count(distinct user_id) as users,
        count(distinct user_session) as identified_sessions
    from {{ ref('stg_rees46_events') }}
    group by 1
), session_rollup as (
    select
        date_trunc('day', event_time) as event_date,
        user_session,
        max(case when event_type = 'view' then 1 else 0 end) as viewed,
        max(case when event_type = 'cart' then 1 else 0 end) as carted,
        max(case when event_type = 'purchase' then 1 else 0 end) as purchased
    from {{ ref('int_rees46_ordered_events') }}
    group by 1, 2
), session_counts as (
    select
        event_date,
        count(*) as session_count,
        sum(viewed) as view_sessions,
        sum(carted) as cart_sessions,
        sum(purchased) as purchase_sessions
    from session_rollup
    group by 1
)
select
    event_counts.event_date,
    event_counts.event_count,
    event_counts.users,
    event_counts.identified_sessions,
    coalesce(session_counts.session_count, 0) as session_count,
    coalesce(session_counts.view_sessions, 0) as view_sessions,
    coalesce(session_counts.cart_sessions, 0) as cart_sessions,
    coalesce(session_counts.purchase_sessions, 0) as purchase_sessions,
    case when event_counts.identified_sessions = 0 then 0 else coalesce(session_counts.purchase_sessions, 0)::double / event_counts.identified_sessions end as purchase_session_rate
from event_counts
left join session_counts using (event_date)
