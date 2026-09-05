select *
from {{ ref('stg_rees46_events') }}
where event_type = 'purchase'
  and (price is null or price < 0)
