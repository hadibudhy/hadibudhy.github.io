-- Business question: when do completed HVFHV trips concentrate?
-- This is a completed-trip proxy, not total rider demand.
WITH trips AS (
    SELECT
        DATE_TRUNC('hour', pickup_datetime) AS pickup_hour,
        PULocationID AS pickup_zone,
        hvfhs_license_num AS provider,
        SR_Flag AS shared_ride
    FROM read_parquet('analysis_data/growth_sources/fhvhv_tripdata_2025-01.parquet')
)
SELECT
    EXTRACT(hour FROM pickup_hour) AS pickup_hour_of_day,
    pickup_zone,
    provider,
    COUNT(*) AS completed_trips,
    AVG(shared_ride) AS shared_ride_share
FROM trips
GROUP BY 1, 2, 3
ORDER BY completed_trips DESC;
