{{ config(materialized='table') }}
with event_counts as (
    select
        date_trunc('day', event_time) as event_date,
        count(*) as event_count,
        count(distinct user_id) as users
    from {{ ref('stg_rees46_events') }}
    group by 1
), first_view as (
    select
        user_session,
        min(event_number) as view_event_number,
        min(event_time) as viewed_at
    from {{ ref('int_rees46_ordered_events') }}
    where event_type = 'view'
    group by 1
), first_cart as (
    select
        ordered.user_session,
        min(ordered.event_number) as cart_event_number,
        min(ordered.event_time) as carted_at
    from {{ ref('int_rees46_ordered_events') }} as ordered
    inner join first_view using (user_session)
    where ordered.event_type = 'cart'
      and ordered.event_number > first_view.view_event_number
    group by 1
), first_purchase as (
    select
        ordered.user_session,
        min(ordered.event_number) as purchase_event_number,
        min(ordered.event_time) as purchased_at
    from {{ ref('int_rees46_ordered_events') }} as ordered
    inner join first_cart using (user_session)
    where ordered.event_type = 'purchase'
      and ordered.event_number > first_cart.cart_event_number
    group by 1
), session_rollup as (
    select
        date_trunc('day', coalesce(first_view.viewed_at, base.session_start_at)) as event_date,
        base.user_session,
        first_view.view_event_number,
        first_cart.cart_event_number,
        first_purchase.purchase_event_number
    from (
        select user_session, min(event_time) as session_start_at
        from {{ ref('int_rees46_ordered_events') }}
        group by 1
    ) as base
    left join first_view using (user_session)
    left join first_cart using (user_session)
    left join first_purchase using (user_session)
), session_counts as (
    select
        event_date,
        count(*) as session_count,
        count(*) filter (where view_event_number is not null) as view_sessions,
        count(*) filter (where cart_event_number is not null) as cart_sessions,
        count(*) filter (where purchase_event_number is not null) as purchase_sessions
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
