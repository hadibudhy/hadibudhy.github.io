# Congestion pricing comparator audit

## Shipped result

This project ships a **descriptive comparator audit**, not a difference-in-differences estimate. It compares equal-weight weekly means of `log(1 + car crossings)` for three affected facilities and seven comparison facilities within 26 weeks of NYC congestion pricing's 5 January 2025 start.

The displayed pre-policy gap changes direction and magnitude. That is enough to pause causal attribution, but it is not a formal parallel-trends test, statistical rejection rule, or policy-effect estimate.

Run the shipped analysis from the repository root:

```bash
python projects/growth-analytics/03-congestion-pricing-causal-impact/src/analyze_mta_comparator.py
```

## Decision boundary

**Decision owner:** Marketplace and Commercial leadership. **Decision:** whether pricing, incentives, or geographic strategy should change after congestion pricing.

This audit does not support changing pricing or supply. A decision-ready study needs a pre-registered comparator rule, formal pre-trend and placebo checks, route-level policy exposure, and internal outcomes such as requests, completed rides, cancellations, pickup delay, passenger price, and driver pay.

## Data and scope

The shipped panel uses official [MTA Bridges and Tunnels Hourly Crossings](https://catalog.data.gov/dataset/mta-bridges-and-tunnels-hourly-crossings-beginning-2019): 27,080 facility-day observations, aggregated to 3,880 facility-week rows across 10 facilities and 388 weeks. The outcome is car crossings, not ride-hailing demand, supply, revenue, or customer behavior.

The affected group is RFK Bridge Manhattan, Queens-Midtown Tunnel, and Hugh L. Carey Tunnel. The seven remaining facilities form the comparison group for this audit. Group means weight each facility equally.

## Future-design scaffolds

- `src/event_study.py` and `sql/cbd_event_study.sql` are unexecuted design scaffolds for a future zone-level study; they are not current evidence.
- `src/analyze_monthly_its.py` is an aggregate diagnostic without an untreated market or route-level exposure; it does not identify the policy effect.
- `CONGESTION_ZONE_VALIDATION.md` documents a coarse zone-boundary check for future trip-level work.

No causal policy effect is reported in this repository.
