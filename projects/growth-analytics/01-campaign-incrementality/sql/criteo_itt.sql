-- Business question: what is the conversion lift from assignment to advertising?
-- Keep assignment as the unit; do not filter to exposure for the primary estimate.
WITH assignment_summary AS (
    SELECT
        treatment,
        COUNT(*) AS assigned_users,
        SUM(conversion) AS conversions,
        SUM(visit) AS visits
    FROM criteo_uplift_unbiased
    GROUP BY treatment
)
SELECT
    t.assigned_users AS treatment_users,
    c.assigned_users AS control_users,
    t.conversions AS treatment_conversions,
    c.conversions AS control_conversions,
    t.conversions * 1.0 / NULLIF(t.assigned_users, 0) AS treatment_conversion_rate,
    c.conversions * 1.0 / NULLIF(c.assigned_users, 0) AS control_conversion_rate,
    t.conversions * 1.0 / NULLIF(t.assigned_users, 0) - c.conversions * 1.0 / NULLIF(c.assigned_users, 0) AS absolute_conversion_lift,
    (t.conversions * 1.0 / NULLIF(t.assigned_users, 0) - c.conversions * 1.0 / NULLIF(c.assigned_users, 0)) * 100000 AS benchmark_incremental_conversions_per_100k
FROM assignment_summary t
JOIN assignment_summary c ON c.treatment = 0
WHERE t.treatment = 1;
