"""Reconcile the headline public claims with generated aggregate evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public" / "data" / "senior"
PROJECTS = ROOT / "src" / "content" / "projects"


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def require(page: str, snippets: list[str]) -> None:
    text = (PROJECTS / page).read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        raise AssertionError(f"{page} is missing generated claims: {missing}")


def main() -> None:
    product = load("product-events.json")
    product_funnel = product["funnel"]
    assert product["quality"]["raw_identified_sessions"] > product_funnel["identified_sessions"]
    assert product_funnel["ordered_purchase_sessions"] <= product_funnel["ordered_cart_sessions"] <= product_funnel["view_sessions"]
    require("2026-09-05-product-event-foundation.md", [
        f"{product_funnel['identified_sessions']:,}", f"{product_funnel['ordered_cart_sessions']:,}", f"{product_funnel['ordered_purchase_sessions']:,}",
        f"{product_funnel['view_to_cart_rate'] * 100:.1f}%", f"{product_funnel['cart_to_purchase_rate'] * 100:.1f}%", f"{product_funnel['session_purchase_rate'] * 100:.1f}%",
    ])

    financial = load("financial-metrics.json")
    fy2026 = next(row for row in financial["annual_metrics"] if row["fiscal_year"] == 2026)
    assert fy2026["revenue"] == 331_839_000_000
    require("2026-09-05-financial-metrics.md", [f"${fy2026['revenue'] / 1e9:.1f}B", f"${fy2026['net_income'] / 1e9:.1f}B", f"{fy2026['net_margin'] * 100:.1f}%"])

    retention = load("retention.json")
    assert [round(row["repeat_rate"] * 100, 1) for row in retention["cohort_repeat"]] == [22.2, 37.5, 47.5]
    cohort_rates = [round(row["repeat_rate"] * 100, 1) for row in retention["cohort_repeat"]]
    assert cohort_rates == [22.2, 37.5, 47.5]
    require("2026-08-15-online-retail-customer-growth.md", [*(f"{rate:.1f}%" for rate in cohort_rates), *(f"{row['eligible_customers']:,}" for row in retention["cohort_repeat"])])
    assert max(row["repeat_rate"] for row in retention["cohort_30d"]) - min(row["repeat_rate"] for row in retention["cohort_30d"]) > 0.1

    service = load("service-queues.json")
    assert service["quality"]["rows"] == 348_180
    taxi = next(row for row in service["priority_queues"] if row["agency"] == "TLC" and row["complaint_type"] == "Taxi Complaint")
    fhv = next(row for row in service["priority_queues"] if row["agency"] == "TLC" and row["complaint_type"] == "For Hire Vehicle Complaint")
    require("2026-09-05-service-metric-reliability.md", [f"{service['quality']['rows']:,}", f"{service['quality']['missing_closed_at_snapshot']:,}", f"{service['quality']['invalid_negative_duration']} records", f"{taxi['p90_close_hours'] / 24:.1f} days", f"{fhv['p90_close_hours'] / 24:.1f} days"])

    campaign = load("campaign.json")
    assert campaign["reconciliation"]["sql_matches_python"] is True
    lift = campaign["experiment"]["conversion_itt"]["absolute_difference"]
    require("campaign-incrementality.md", [f"{lift * 100:.3f} percentage points", f"{lift * 100000:.0f} extra conversions", "$5,759", f"{lift * 100:.4f} percentage-point"])

    marketplace = load("marketplace.json")
    assert marketplace["quality"]["rows"] == 20_405_666
    top = marketplace["priority_zone_hours"][0]
    require("marketplace-supply-demand.md", [f"{marketplace['quality']['rows']:,}", f"{marketplace['quality']['negative_delay']:,}", f"{top['p90_delay']:.1f} minutes", f"{top['completed_trips']:,}", f"{int(top['days_p90_at_least_12'])} of {int(top['observed_daily_windows'])}"])

    print("senior claims reconcile with six generated evidence files")


if __name__ == "__main__":
    main()
