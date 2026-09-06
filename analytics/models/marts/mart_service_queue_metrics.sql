{{ config(materialized='table') }}
with snapshot as (
    select cast('{{ var("snapshot_at", "2026-09-05 23:59:59") }}' as timestamp) as snapshot_at
), scoped as (
    select requests.*
    from {{ ref('stg_nyc311_requests') }} as requests
    where created_at >= timestamp '2025-01-01'
      and created_at < timestamp '2025-02-01'
), queue_metrics as (
    select
        agency,
        complaint_type,
        count(*) as arrivals,
        count(*) filter (where closed_at is null) as open_backlog,
        count(*) filter (where closed_at < created_at) as invalid_negative_durations,
        count(*) filter (where closed_at is not null and closed_at >= created_at and closed_at <= (select snapshot_at from snapshot)) as valid_closed_requests,
        count(*) filter (where closed_at is not null and closed_at >= created_at and closed_at <= (select snapshot_at from snapshot))::double / nullif(count(*) - count(*) filter (where closed_at < created_at), 0) as closure_coverage,
        median(date_diff('second', created_at, closed_at) / 3600.0) filter (where closed_at is not null and closed_at >= created_at and closed_at <= (select snapshot_at from snapshot)) as median_close_hours,
        quantile_cont(date_diff('second', created_at, closed_at) / 3600.0, 0.9) filter (where closed_at is not null and closed_at >= created_at and closed_at <= (select snapshot_at from snapshot)) as p90_close_hours,
        median(date_diff('second', created_at, (select snapshot_at from snapshot)) / 3600.0) filter (where closed_at is null) as median_open_age_hours
    from scoped
    group by 1, 2
)
select * from queue_metrics
