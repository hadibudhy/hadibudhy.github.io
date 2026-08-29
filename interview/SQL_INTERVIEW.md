# SQL interview questions from the projects

Each question is a business question first. The expected answer should state the grain, denominator, join risk, and validation check before writing SQL.

1. What is the Criteo conversion rate by treatment assignment?
2. How many incremental conversions occur per 100,000 assigned users?
3. How would you calculate a treatment/control confidence interval in SQL?
4. How would you check sample-ratio mismatch?
5. How would you compare visit and conversion rates without filtering to exposed users?
6. How would you rank feature bands by exploratory uplift?
7. How would you apply a minimum segment size before ranking?
8. How would you calculate a rolling seven-day conversion rate?
9. How would you use `LAG` to compare daily conversion with the prior day?
10. How would you find the first event date for each user?
11. How would you avoid double-counting users after joining outcomes to feature bands?
12. How would you calculate completed HVFHV trips by hour and pickup zone?
13. How would you rank the top five pickup zones within each hour?
14. How would you calculate a zone’s share of city trips using a window function?
15. How would you compare weekday and weekend trip patterns?
16. How would you calculate airport-origin trip share?
17. How would you measure provider mix without treating missing providers as zero?
18. How would you join trips to the taxi-zone lookup without changing row count?
19. How would you detect duplicate trip identifiers or duplicate rows?
20. How would you create a zone-hour table for an incentive experiment?
21. How would you identify zones with persistent rather than one-day concentration?
22. How would you calculate pre/post policy means around 5 January 2025?
23. How would you create event time with `DATE_DIFF`?
24. How would you join a zone treatment map while preserving unmatched zones for QA?
25. How would you calculate treatment and control changes for a difference-in-differences table?
26. How would you attach weather by local date without duplicating trips?
27. How would you calculate a weighted average fare rather than an average of daily averages?
28. How would you use `QUALIFY` or a CTE to keep one record per zone-day?
29. How would you flag incomplete reporting periods?
30. How would you compare a query plan before and after partition and column pruning?

## Query patterns

```sql
WITH daily AS (
  SELECT DATE_TRUNC('day', pickup_datetime) AS service_date,
         PULocationID AS pickup_zone,
         COUNT(*) AS trips
  FROM hvfhv_trip_clean
  GROUP BY 1, 2
), ranked AS (
  SELECT *, RANK() OVER (PARTITION BY service_date ORDER BY trips DESC) AS zone_rank
  FROM daily
)
SELECT * FROM ranked WHERE zone_rank <= 5;
```

This answers where recorded trips concentrate, not where unmet demand exists. The join and denominator checks are part of the answer.
