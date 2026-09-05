{{ config(materialized='table') }}
with event_counts as (
    select
        date_trunc('day', event_time) as event_date,
        count(*) as event_count,
        count(distinct user_id) as users
    from {{ ref('stg_rees46_events') }}
    group by 1
), session_rollup as (
    select
        date_trunc('day', min(event_time)) as event_date,
        user_session,
        min(case when event_type = 'view' then event_time end) as viewed_at,
        min(case when event_type = 'cart' then event_time end) as carted_at,
        min(case when event_type = 'purchase' then event_time end) as purchased_at
    from {{ ref('int_rees46_ordered_events') }}
    group by user_session
), session_counts as (
    select
        event_date,
        count(*) as session_count,
        count(*) filter (where viewed_at is not null) as view_sessions,
        count(*) filter (where viewed_at is not null and carted_at >= viewed_at) as cart_sessions,
        count(*) filter (where viewed_at is not null and carted_at >= viewed_at and purchased_at >= carted_at) as purchase_sessions
    from session_rollup
    group by 1
)
select
    event_counts.event_date,
    event_counts.event_count,
    event_counts.users,
    coalesce(session_counts.session_count, 0) as identified_sessions,
    coalesce(session_counts.session_count, 0) as session_count,
    coalesce(session_counts.view_sessions, 0) as view_sessions,
    coalesce(session_counts.cart_sessions, 0) as cart_sessions,
    coalesce(session_counts.purchase_sessions, 0) as purchase_sessions,
    case when coalesce(session_counts.session_count, 0) = 0 then 0 else coalesce(session_counts.purchase_sessions, 0)::double / session_counts.session_count end as purchase_session_rate
from event_counts
left join session_counts using (event_date)
