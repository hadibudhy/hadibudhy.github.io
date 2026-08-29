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
    treatment,
    assigned_users,
    conversions,
    visits,
    conversions / NULLIF(assigned_users, 0) AS conversion_rate,
    visits / NULLIF(assigned_users, 0) AS visit_rate
FROM assignment_summary;
