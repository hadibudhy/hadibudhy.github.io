select *
from {{ ref('mart_service_queue_metrics') }}
where arrivals < 0
   or open_backlog < 0
   or invalid_negative_durations < 0
   or closure_coverage < 0
   or closure_coverage > 1
   or median_close_hours < 0
   or p90_close_hours < 0
   or median_open_age_hours < 0
