-- Business question: did the policy change outcomes inside the CBD relative to a control?
-- The zone treatment map and controls must be created before this is run.
WITH daily AS (
    SELECT
        DATE_TRUNC('day', pickup_datetime) AS service_date,
        pickup_zone,
        is_cbd,
        COUNT(*) AS completed_trips,
        AVG(passenger_fare) AS mean_fare,
        AVG(driver_pay) AS mean_driver_pay
    FROM hvfhv_trip_clean
    GROUP BY 1, 2, 3
),
event_time AS (
    SELECT *, service_date - DATE '2025-01-05' AS days_from_policy
    FROM daily
)
SELECT
    service_date,
    pickup_zone,
    is_cbd,
    days_from_policy,
    completed_trips,
    mean_fare,
    mean_driver_pay
FROM event_time
ORDER BY service_date, pickup_zone;
