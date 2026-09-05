{{ config(materialized='incremental', unique_key='event_id', on_schema_change='fail') }}
with source_rows as (
    select * from {{ source('rees46', 'events') }}
    {% if is_incremental() %}
      where event_time >= (select coalesce(max(event_time), timestamp '1900-01-01') from {{ this }})
    {% endif %}
), typed as (
    select
        md5(concat_ws('|', cast(event_time as varchar), cast(event_type as varchar), cast(product_id as varchar), cast(user_id as varchar), coalesce(cast(user_session as varchar), ''))) as event_id,
        cast(event_time as timestamp) as event_time,
        cast(event_type as varchar) as event_type,
        cast(product_id as varchar) as product_id,
        cast(category_id as varchar) as category_id,
        nullif(cast(category_code as varchar), '') as category_code,
        nullif(cast(brand as varchar), '') as brand,
        cast(price as double) as price,
        cast(user_id as varchar) as user_id,
        nullif(cast(user_session as varchar), '') as user_session,
        current_timestamp as loaded_at
    from source_rows
)
select * from typed
