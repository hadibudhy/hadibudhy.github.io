-- Business question: when do recorded HVFHV trips concentrate?
-- This is a fulfilled-trip proxy, not total rider demand.
WITH trips AS (
    SELECT CAST(hour AS INTEGER) AS pickup_hour, CAST(trips AS BIGINT) AS recorded_trips
    FROM read_json_auto('analysis_data/growth_sources/hvf_hourly_2019.json')
)
SELECT
    pickup_hour,
    recorded_trips
FROM trips
ORDER BY pickup_hour;
