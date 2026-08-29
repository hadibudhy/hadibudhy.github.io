-- Business question: did policy-exposed zone-days change relative to untreated zones?
-- `is_policy_exposed` must be built from origin, destination, and documented
-- charge rules. A pickup-only flag is not a valid exposure definition.
WITH daily_raw AS (
    SELECT
        DATE_TRUNC('day', pickup_datetime) AS service_date,
        pickup_zone,
        COUNT(DISTINCT is_policy_exposed) AS exposure_values,
        MAX(is_policy_exposed) AS is_policy_exposed,
        COUNT(*) AS recorded_trips,
        AVG(passenger_fare) AS mean_fare,
        AVG(driver_pay) AS mean_driver_pay
    FROM hvfhv_trip_clean
    GROUP BY 1, 2
), daily AS (
    SELECT * FROM daily_raw WHERE exposure_values = 1
),
event_time AS (
    SELECT *, DATE_DIFF('day', DATE '2025-01-05', service_date) AS days_from_policy,
           CASE WHEN service_date >= DATE '2025-01-05' THEN 1 ELSE 0 END AS post_policy
    FROM daily
)
SELECT
    service_date,
    pickup_zone,
    is_policy_exposed,
    days_from_policy,
    post_policy,
    recorded_trips,
    mean_fare,
    mean_driver_pay
FROM event_time
ORDER BY service_date, pickup_zone;
