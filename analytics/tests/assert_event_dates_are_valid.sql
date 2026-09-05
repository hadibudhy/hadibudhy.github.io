select *
from {{ ref('stg_rees46_events') }}
where event_time is null
   or event_time < timestamp '2010-01-01'
   or event_time > current_timestamp
