{{ config(materialized='table') }}
with source_rows as (
    select * from {{ source('rees46', 'events') }}
), typed as (
    select
        md5(concat_ws('|', cast(source_batch_id as varchar), cast(source_row_number as varchar))) as event_id,
        md5(concat_ws('|', cast(event_time as varchar), cast(event_type as varchar), cast(product_id as varchar), cast(category_id as varchar), coalesce(cast(category_code as varchar), ''), coalesce(cast(brand as varchar), ''), cast(price as varchar), cast(user_id as varchar), coalesce(cast(user_session as varchar), ''))) as logical_event_id,
        cast(source_batch_id as varchar) as source_batch_id,
        cast(source_row_number as bigint) as source_row_number,
        cast(event_time as timestamp) as event_time,
        cast(event_type as varchar) as event_type,
        cast(product_id as varchar) as product_id,
        cast(category_id as varchar) as category_id,
        nullif(cast(category_code as varchar), '') as category_code,
        nullif(cast(brand as varchar), '') as brand,
        cast(price as double) as price,
        cast(user_id as varchar) as user_id,
        nullif(cast(user_session as varchar), '') as user_session,
        cast(current_timestamp as timestamp) as loaded_at
    from source_rows
)
select * from typed
