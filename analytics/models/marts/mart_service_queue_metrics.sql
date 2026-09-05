{{ config(materialized='table') }}
with cutoff as (
    select cast('{{ var("analysis_cutoff", "2025-01-31 23:59:59") }}' as timestamp) as cutoff_at
), scoped as (
    select requests.*
    from {{ ref('stg_nyc311_requests') }} as requests
    cross join cutoff
    where created_at <= cutoff.cutoff_at
), queue_metrics as (
    select
        agency,
        complaint_type,
        count(*) as arrivals,
        count(*) filter (where closed_at is null or closed_at > (select cutoff_at from cutoff)) as open_backlog,
        median(date_diff('hour', created_at, closed_at)) filter (where closed_at is not null and closed_at >= created_at) as median_close_hours,
        quantile_cont(date_diff('hour', created_at, closed_at), 0.9) filter (where closed_at is not null and closed_at >= created_at) as p90_close_hours
    from scoped
    group by 1, 2
)
select * from queue_metrics
