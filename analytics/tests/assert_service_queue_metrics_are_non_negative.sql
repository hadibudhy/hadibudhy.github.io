select *
from {{ ref('mart_service_queue_metrics') }}
where arrivals < 0
   or open_backlog < 0
   or median_close_hours < 0
   or p90_close_hours < 0
