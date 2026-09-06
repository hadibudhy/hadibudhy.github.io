"""Build decision-focused aggregate evidence for the six public case studies.

Raw public datasets remain outside Git. This script reads validated snapshots,
writes only aggregate JSON, and regenerates the charts used by the articles.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from statistics import NormalDist

import duckdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_OUT = ROOT / "public" / "data" / "senior"
IMAGE_OUT = ROOT / "public" / "images"


def dbt_connection() -> duckdb.DuckDBPyConnection | None:
    if os.getenv("SENIOR_FULL_DBT") != "1":
        return None
    database = ROOT / "target" / "ae_product.duckdb"
    return duckdb.connect(str(database), read_only=True) if database.exists() else None


def source_path(relative: str) -> Path:
    candidates = [ROOT / relative, ROOT.parents[1] / relative]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Missing source {relative}; checked {candidates}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(name: str, payload: dict) -> None:
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    payload["evidence_metadata"] = {"generator": "scripts/build_senior_evidence.py", "version": "2026-09-06", "aggregate_only": True}
    (DATA_OUT / name).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def style(axis: plt.Axes) -> None:
    axis.spines[["top", "right"]].set_visible(False)
    axis.grid(axis="y", color="#d9dde3", linewidth=0.7, alpha=0.6)
    axis.set_axisbelow(True)


def product_events() -> None:
    source = source_path("analysis_data/product-events/electronics-events.csv.gz")
    connection = duckdb.connect()
    base = """
    with events as (
      select *, row_number() over () as source_row_number,
        md5(concat_ws('|', cast(event_time as varchar), cast(event_type as varchar), cast(product_id as varchar), cast(category_id as varchar), coalesce(cast(category_code as varchar), ''), coalesce(cast(brand as varchar), ''), cast(price as varchar), cast(user_id as varchar), coalesce(cast(user_session as varchar), ''))) as logical_event_id
      from read_csv_auto(?, header=true, compression='gzip')
    ), ranked as (
      select *, row_number() over(partition by logical_event_id order by source_row_number) as duplicate_number
      from events where user_session is not null
    ), valid_sessions as (
      select user_session from ranked group by 1 having count(distinct user_id)=1
    ), ordered as (
      select *, row_number() over(partition by user_session order by event_time, source_row_number) as event_number
      from ranked inner join valid_sessions using(user_session) where duplicate_number=1
    ), first_view as (
      select user_session, min(event_number) as view_number, min(event_time) as viewed_at
      from ordered where event_type='view' group by 1
    ), first_cart as (
      select ordered.user_session, min(event_number) as cart_number, min(event_time) as carted_at
      from ordered join first_view using(user_session)
      where event_type='cart' and event_number>view_number and event_time <= viewed_at + interval 24 hour group by 1
    ), first_purchase as (
      select ordered.user_session, min(event_number) as purchase_number, min(event_time) as purchased_at
      from ordered join first_cart using(user_session) join first_view using(user_session)
      where event_type='purchase' and event_number>cart_number and event_time <= viewed_at + interval 24 hour group by 1
    ), sessions as (
      select o.user_session, min(o.event_time) as started_at,
        max(v.view_number is not null)::int as viewed,
        max(c.cart_number is not null)::int as carted,
        max(p.purchase_number is not null)::int as purchased,
        max(v.viewed_at) as viewed_at, max(c.carted_at) as carted_at, max(p.purchased_at) as purchased_at
      from ordered o left join first_view v using(user_session)
      left join first_cart c using(user_session) left join first_purchase p using(user_session)
      group by 1
    )
    """
    query = base + "select * from sessions"
    sessions = connection.execute(query, [str(source)]).fetchdf()
    quality = connection.execute("""
      with events as (
        select *, md5(concat_ws('|', cast(event_time as varchar), cast(event_type as varchar), cast(product_id as varchar), cast(category_id as varchar), coalesce(cast(category_code as varchar), ''), coalesce(cast(brand as varchar), ''), cast(price as varchar), cast(user_id as varchar), coalesce(cast(user_session as varchar), ''))) as logical_event_id
        from read_csv_auto(?, header=true, compression='gzip')
      ) select count(*) as row_count, count(distinct user_id) as user_count,
        count(distinct user_session) as session_count,
        count_if(user_session is null) as missing_session_rows,
        count(*) - count(distinct logical_event_id) as exact_duplicate_rows,
        (select count(*) from (select user_session from events where user_session is not null group by 1 having count(distinct user_id)>1)) as multi_user_sessions,
        (select count(*) from (select user_session from events where user_session is not null group by 1 having max(event_time)-min(event_time)>interval 24 hour)) as sessions_over_24_hours,
        min(event_time) as first_event, max(event_time) as last_event
      from events
    """, [str(source)]).fetchone()
    categories = connection.execute("""
      with events as (
        select *, row_number() over () as source_row_number,
          md5(concat_ws('|', cast(event_time as varchar), cast(event_type as varchar), cast(product_id as varchar), cast(category_id as varchar), coalesce(cast(category_code as varchar), ''), coalesce(cast(brand as varchar), ''), cast(price as varchar), cast(user_id as varchar), coalesce(cast(user_session as varchar), ''))) as logical_event_id
        from read_csv_auto(?,header=true,compression='gzip')
      ), ranked as (
        select *, row_number() over(partition by logical_event_id order by source_row_number) as duplicate_number
        from events where user_session is not null and category_code is not null
      ), valid_sessions as (
        select user_session from ranked group by 1 having count(distinct user_id)=1
      ), category_events as (
        select ranked.* from ranked inner join valid_sessions using(user_session) where duplicate_number=1
      ), by_session as (
        select category_code,user_session,
          max(event_type='view')::int viewed,max(event_type='cart')::int carted,max(event_type='purchase')::int purchased
        from category_events group by 1,2
      )
      select category_code,count_if(viewed=1) view_sessions,count_if(carted=1) cart_sessions,count_if(purchased=1) purchase_sessions,
        count_if(purchased=1)::double/nullif(count_if(viewed=1),0) purchase_presence_rate
      from by_session group by 1 having view_sessions>=1000 order by purchase_presence_rate desc
    """, [str(source)]).fetchdf()
    total = len(sessions)
    funnel = {
        "identified_sessions": total,
        "view_sessions": int(sessions.viewed.sum()),
        "ordered_cart_sessions": int(sessions.carted.sum()),
        "ordered_purchase_sessions": int(sessions.purchased.sum()),
    }
    funnel["view_to_cart_rate"] = funnel["ordered_cart_sessions"] / funnel["view_sessions"]
    funnel["cart_to_purchase_rate"] = funnel["ordered_purchase_sessions"] / funnel["ordered_cart_sessions"]
    funnel["session_purchase_rate"] = funnel["ordered_purchase_sessions"] / total
    v2c = (sessions.carted_at - sessions.viewed_at).dt.total_seconds().div(60)
    c2p = (sessions.purchased_at - sessions.carted_at).dt.total_seconds().div(60)
    funnel["median_view_to_cart_minutes"] = float(v2c.dropna().median())
    funnel["median_cart_to_purchase_minutes"] = float(c2p.dropna().median())
    dbt = dbt_connection()
    if dbt:
        mart = dbt.execute("select sum(session_count),sum(view_sessions),sum(cart_sessions),sum(purchase_sessions) from main.fct_product_funnel").fetchone()
        quality_mart = dbt.execute("select source_rows,exact_duplicate_rows,multi_user_sessions,sessions_over_24_hours from main.mart_event_quality").fetchone()
        dbt.close()
        if tuple(map(int, mart)) != (funnel["identified_sessions"], funnel["view_sessions"], funnel["ordered_cart_sessions"], funnel["ordered_purchase_sessions"]):
            raise ValueError("Product evidence does not reconcile with the dbt funnel mart")
        if tuple(map(int, quality_mart)) != (int(quality[0]), int(quality[4]), int(quality[5]), int(quality[6])):
            raise ValueError("Product evidence does not reconcile with the dbt quality mart")
    top_categories = categories.head(8).to_dict(orient="records")
    save_json("product-events.json", {
        "source": {"url": "https://data.rees46.com/datasets/electronics-events/electronics-events.csv.gz", "retrieved_at": "2026-09-05T17:17:32Z", "sha256": digest(source)},
        "quality": {"rows": quality[0], "users": quality[1], "raw_identified_sessions": quality[2], "missing_session_rows": quality[3], "exact_duplicate_rows": quality[4], "multi_user_sessions": quality[5], "sessions_over_24_hours": quality[6], "first_event": str(quality[7]), "last_event": str(quality[8])},
        "funnel": funnel, "top_categories": top_categories,
        "limits": ["The export has no registration event or experiment assignment.", "Category rates are descriptive session event-presence rates."],
    })
    fig, ax = plt.subplots(figsize=(8, 4.8))
    labels = ["Identified\nsessions", "Viewed", "Carted after\nview", "Purchased after\ncart"]
    values = [total, funnel["view_sessions"], funnel["ordered_cart_sessions"], funnel["ordered_purchase_sessions"]]
    ax.bar(labels, np.array(values) / 1000, color=["#9fb0c6", "#5e9bea", "#2f6fc5", "#174a8b"])
    for i, value in enumerate(values): ax.text(i, value / 1000 + max(values) / 1000 * .02, f"{value:,}", ha="center", fontsize=9)
    ax.set_title("Only ordered journeys count as funnel completion", loc="left", weight="bold")
    ax.set_ylabel("Sessions (thousands)"); style(ax); fig.tight_layout()
    fig.savefig(IMAGE_OUT / "senior-product-funnel.png", dpi=160); plt.close(fig)
    shown = categories.sort_values("view_sessions", ascending=False).head(10).sort_values("purchase_presence_rate")
    fig, ax = plt.subplots(figsize=(8, 5.4))
    ax.barh(shown.category_code, shown.purchase_presence_rate * 100, color="#2f6fc5")
    ax.set_title("Purchase-event presence varies across large categories", loc="left", weight="bold")
    ax.set_xlabel("Sessions with a purchase event / sessions with a view event (%)"); style(ax); fig.tight_layout()
    fig.savefig(IMAGE_OUT / "senior-product-categories.png", dpi=160); plt.close(fig)


def online_retail() -> None:
    source = source_path("analysis_data/extracted/Online Retail.xlsx")
    raw = pd.read_excel(source)
    sales = raw[~raw.InvoiceNo.astype(str).str.startswith("C") & raw.CustomerID.notna() & (raw.Quantity > 0) & (raw.UnitPrice > 0)].copy()
    sales["revenue"] = sales.Quantity * sales.UnitPrice
    orders = sales.groupby(["CustomerID", "InvoiceNo"], as_index=False).agg(order_at=("InvoiceDate", "min"), order_value=("revenue", "sum"), country=("Country", "first"))
    orders = orders.sort_values(["CustomerID", "order_at", "InvoiceNo"])
    firsts = orders.groupby("CustomerID", as_index=False).first()[["CustomerID", "order_at", "order_value", "country"]].rename(columns={"order_at":"first_order_at", "order_value":"first_order_value"})
    later = orders.merge(firsts[["CustomerID", "first_order_at"]], on="CustomerID")
    later["days_after_first"] = (later.order_at - later.first_order_at).dt.total_seconds() / 86400
    end = orders.order_at.max()
    common_eligible = firsts[firsts.first_order_at <= end - pd.Timedelta(days=90)]
    cohort_results = []
    for window in (30, 60, 90):
        repeated = later[(later.days_after_first > 0) & (later.days_after_first <= window)].CustomerID.unique()
        retained = common_eligible.CustomerID.isin(repeated).sum()
        cohort_results.append({"window_days": window, "eligible_customers": len(common_eligible), "repeat_customers": int(retained), "repeat_rate": retained / len(common_eligible)})
    eligible30 = firsts[firsts.first_order_at <= end - pd.Timedelta(days=30)].copy()
    repeat30 = set(later[(later.days_after_first > 0) & (later.days_after_first <= 30)].CustomerID)
    eligible30["repeated_30d"] = eligible30.CustomerID.isin(repeat30)
    eligible30["cohort_month"] = eligible30.first_order_at.dt.to_period("M").astype(str)
    cohort_30d = eligible30.groupby("cohort_month").agg(eligible_customers=("CustomerID", "size"), repeat_rate=("repeated_30d", "mean")).reset_index()
    eligible90 = firsts[firsts.first_order_at <= end - pd.Timedelta(days=90)].copy()
    eligible90["first_value_band"] = pd.qcut(eligible90.first_order_value.rank(method="first"), 4, labels=["Q1 low", "Q2", "Q3", "Q4 high"])
    repeated90 = set(later[(later.days_after_first > 0) & (later.days_after_first <= 90)].CustomerID)
    eligible90["repeated_90d"] = eligible90.CustomerID.isin(repeated90)
    segments = eligible90.groupby("first_value_band", observed=True).agg(customers=("CustomerID", "size"), repeat_rate=("repeated_90d", "mean"), median_first_order=("first_order_value", "median")).reset_index()
    monthly = orders.assign(month=orders.order_at.dt.to_period("M").astype(str)).groupby("month").agg(customers=("CustomerID", "nunique"), orders=("InvoiceNo", "nunique"), revenue=("order_value", "sum"), average_order_value=("order_value", "mean")).reset_index()
    save_json("retention.json", {
        "source": {"url": "https://archive.ics.uci.edu/dataset/352/online%2Bretail", "retrieved_at": "2026-08-20T07:43:19Z", "sha256": digest(source)},
        "quality": {"raw_rows": len(raw), "cancelled_rows": int(raw.InvoiceNo.astype(str).str.startswith("C").sum()), "missing_customer_rows": int(raw.CustomerID.isna().sum()), "clean_orders": len(orders), "customers": int(orders.CustomerID.nunique()), "end_date": str(end)},
        "cohort_repeat": cohort_results, "cohort_30d": cohort_30d.to_dict(orient="records"), "first_order_value_segments": segments.to_dict(orient="records"), "monthly_decomposition": monthly.to_dict(orient="records"),
        "limits": ["First observed purchase is not guaranteed to be the customer's true first purchase.", "The source contains revenue but no cost, margin, or campaign exposure."],
    })
    fig, ax = plt.subplots(figsize=(7.5, 4.6)); x=[str(r["window_days"]) for r in cohort_results]; y=[r["repeat_rate"]*100 for r in cohort_results]
    ax.bar(x, y, color="#2f6fc5"); ax.set_title("Repeat purchase rises as the observation window expands", loc="left", weight="bold"); ax.set_xlabel("Days after first observed purchase"); ax.set_ylabel("Eligible customers with another order (%)"); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-retail-retention.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.5, 4.6)); ax.bar(segments.first_value_band.astype(str), segments.repeat_rate*100, color="#5e9bea"); ax.set_title("First-order value alone does not define the retention strategy", loc="left", weight="bold"); ax.set_ylabel("90-day repeat rate (%)"); ax.set_xlabel("First observed order value quartile"); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-retail-segments.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.8)); ax.plot(cohort_30d.cohort_month, cohort_30d.repeat_rate * 100, marker="o", color="#174a8b"); ax.set_title("30-day repeat varies across first-observed-purchase cohorts", loc="left", weight="bold"); ax.set_ylabel("Eligible customers with another order (%)"); ax.set_xlabel("First observed purchase month"); ax.tick_params(axis="x", rotation=45); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-retail-cohorts.png", dpi=160); plt.close(fig)


def service_queues() -> None:
    source = source_path("analysis_data/service/nyc311-2025-01.csv")
    frame = pd.read_csv(source, dtype=str)
    frame.created_date = pd.to_datetime(frame.created_date, errors="coerce")
    frame.closed_date = pd.to_datetime(frame.closed_date, errors="coerce")
    snapshot_at = pd.Timestamp("2026-09-05 23:59:59")
    frame["invalid_duration"] = frame.closed_date.notna() & (frame.closed_date < frame.created_date)
    frame["valid_closed"] = frame.closed_date.notna() & (frame.closed_date <= snapshot_at) & ~frame.invalid_duration
    frame["open_at_snapshot"] = frame.closed_date.isna()
    frame["close_hours"] = (frame.closed_date - frame.created_date).dt.total_seconds() / 3600
    frame["open_age_hours"] = (snapshot_at - frame.created_date).dt.total_seconds() / 3600
    grouped = frame.groupby(["agency", "complaint_type"], dropna=False).agg(
        arrivals=("unique_key", "size"),
        open_backlog=("open_at_snapshot", "sum"),
        invalid_negative_durations=("invalid_duration", "sum"),
        valid_closed_requests=("valid_closed", "sum"),
        median_close_hours=("close_hours", lambda s: float(s[frame.loc[s.index, "valid_closed"]].median())),
        p90_close_hours=("close_hours", lambda s: float(s[frame.loc[s.index, "valid_closed"]].quantile(.9))),
        median_open_age_hours=("open_age_hours", lambda s: float(s[frame.loc[s.index, "open_at_snapshot"]].median())),
    ).reset_index()
    grouped["closure_coverage"] = grouped.valid_closed_requests / (grouped.arrivals - grouped.invalid_negative_durations)
    eligible = grouped[(grouped.arrivals >= 500) & (grouped.closure_coverage >= 0.8)].copy()
    priority = eligible.sort_values(["p90_close_hours", "arrivals"], ascending=[False, False]).head(12)
    dbt = dbt_connection()
    if dbt:
        mart = dbt.execute("select agency,complaint_type,arrivals,open_backlog,invalid_negative_durations,valid_closed_requests,closure_coverage,median_close_hours,p90_close_hours,median_open_age_hours from main.mart_service_queue_metrics").fetchdf()
        dbt.close()
        check = grouped.merge(mart, on=["agency", "complaint_type"], suffixes=("_python", "_dbt"))
        fields = ["arrivals", "open_backlog", "invalid_negative_durations", "valid_closed_requests", "closure_coverage", "median_close_hours", "p90_close_hours"]
        for field in fields:
            if not np.allclose(check[f"{field}_python"].fillna(-1), check[f"{field}_dbt"].fillna(-1)):
                raise ValueError(f"Service evidence does not reconcile with dbt for {field}")
    save_json("service-queues.json", {
        "source": {"url": "https://data.cityofnewyork.us/resource/erm2-nwe9", "retrieved_at": "2026-09-05", "query_window": "2025-01-01 through 2025-01-31", "snapshot_at": str(snapshot_at), "sha256": digest(source)},
        "quality": {"rows": len(frame), "duplicate_request_ids": int(frame.unique_key.duplicated().sum()), "missing_created": int(frame.created_date.isna().sum()), "missing_closed_at_snapshot": int(frame.closed_date.isna().sum()), "invalid_negative_duration": int(frame.invalid_duration.sum())},
        "priority_queues": priority.replace({np.nan: None}).to_dict(orient="records"),
        "estimand": "Administrative closure time among valid closed requests observed by the snapshot; open requests are right-censored and excluded from closure quantiles.",
        "limits": ["Administrative closure is not verified resolution.", "Closed-request quantiles are not eventual full-cohort resolution times because open cases are right-censored."],
    })
    shown = priority.sort_values("p90_close_hours").copy(); shown["queue"] = shown.agency + " | " + shown.complaint_type.str.slice(0,28)
    fig, ax = plt.subplots(figsize=(9, 6)); ax.barh(shown.queue, shown.p90_close_hours / 24, color="#2f6fc5"); ax.set_title("Closed-request closure times are long in a small set of queues", loc="left", weight="bold"); ax.set_xlabel("90th percentile administrative closure time among valid closed requests (days)"); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-311-pressure.png", dpi=160); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 6)); ax.scatter(eligible.arrivals, eligible.p90_close_hours / 24, s=np.clip(eligible.open_backlog / 10, 15, 450), alpha=.65, color="#2f6fc5"); ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title("Volume and closed-request closure time identify different queues", loc="left", weight="bold"); ax.set_xlabel("January arrivals (log scale)"); ax.set_ylabel("P90 administrative closure time among valid closed requests (days, log scale)"); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-311-volume-time.png", dpi=160); plt.close(fig)


def financial_metrics() -> None:
    source = source_path("analysis_data/raw/sec_microsoft_companyfacts.json")
    payload = json.loads(source.read_text(encoding="utf-8"))
    observations = []
    tags = payload["facts"]["us-gaap"]
    for tag in ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "NetIncomeLoss"):
        for row in tags.get(tag, {}).get("units", {}).get("USD", []):
            start, end = pd.to_datetime(row.get("start")), pd.to_datetime(row.get("end"))
            duration = (end - start).days if pd.notna(start) and pd.notna(end) else None
            if row.get("fp") == "FY" and row.get("form") in ("10-K", "10-K/A") and duration is not None and 300 <= duration <= 380:
                observations.append({"tag": tag, "metric": "net_income" if tag == "NetIncomeLoss" else "revenue", "filing_fy": int(row["fy"]), "fiscal_year": int(end.year), "filed": row.get("filed"), "accession": row.get("accn"), "period_end": row.get("end"), "duration_days": duration, "value": row["val"]})
    facts = pd.DataFrame(observations)
    filing = facts[["fiscal_year", "accession", "filed"]].drop_duplicates().sort_values(["fiscal_year", "filed", "accession"]).groupby("fiscal_year").tail(1)
    selected = facts.merge(filing[["fiscal_year", "accession"]], on=["fiscal_year", "accession"])
    selected["tag_priority"] = np.where(selected.tag == "Revenues", 1, 2)
    selected = selected.sort_values(["fiscal_year", "metric", "tag_priority", "period_end"]).drop_duplicates(["fiscal_year", "metric"], keep="first")
    annual = selected.pivot(index="fiscal_year", columns="metric", values="value").dropna().reset_index()
    accessions = selected.groupby("fiscal_year", as_index=False).accession.first().rename(columns={"accession": "source_accession"})
    annual = annual.merge(accessions, on="fiscal_year")
    annual["net_margin"] = annual.net_income / annual.revenue
    annual["revenue_growth"] = annual.revenue.pct_change()
    annual["net_income_growth"] = annual.net_income.pct_change()
    annual = annual.tail(5)
    reference = pd.read_csv(ROOT / "analytics" / "seeds" / "ci" / "expected_financial_metrics.csv")
    checked = annual.merge(reference, on="fiscal_year", suffixes=("_actual", "_expected"), how="inner")
    if len(checked) != len(reference) or not np.allclose(checked.revenue_actual, checked.revenue_expected) or not np.allclose(checked.net_income_actual, checked.net_income_expected) or not (checked.source_accession_actual == checked.source_accession_expected).all():
        raise ValueError("Financial mart values do not reconcile with the approved filing reference")
    dbt = dbt_connection()
    if dbt:
        mart = dbt.execute("select fiscal_year,revenue,net_income,source_accession from main.mart_financial_metrics where fiscal_year between 2022 and 2026").fetchdf()
        dbt.close()
        mart_check = annual.merge(mart, on="fiscal_year", suffixes=("_python", "_dbt"))
        if len(mart_check) != len(annual) or not np.allclose(mart_check.revenue_python, mart_check.revenue_dbt) or not np.allclose(mart_check.net_income_python, mart_check.net_income_dbt) or not (mart_check.source_accession_python == mart_check.source_accession_dbt).all():
            raise ValueError("Financial evidence does not reconcile with the dbt mart")
    filing_documents = reference[["source_accession", "source_document_url", "source_document_sha256", "source_table"]].drop_duplicates().to_dict(orient="records")
    save_json("financial-metrics.json", {
        "source": {"url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json", "retrieved_at": "2026-08-20T07:42:40Z", "sha256": digest(source), "issuer": payload.get("entityName")},
        "quality": {"eligible_annual_facts": len(facts), "selected_periods": len(annual), "selected_accessions": selected[selected.fiscal_year.isin(annual.fiscal_year)].groupby("fiscal_year").accession.nunique().to_dict()},
        "annual_metrics": annual.replace({np.nan: None}).to_dict(orient="records"),
        "reconciliation": {"reference": "analytics/seeds/ci/expected_financial_metrics.csv", "matched_periods": len(checked), "variance_tolerance_usd": 1},
        "filing_documents": filing_documents,
        "selection_rule": "Latest filed 10-K/10-K-A context per fiscal year, 300-380 day duration, one coherent accession, deterministic revenue-tag priority.",
        "limits": ["Company-level filings do not identify product or customer drivers.", "The latest comparative filing context is used consistently within each fiscal year."],
    })
    fig, ax = plt.subplots(figsize=(8, 4.8)); x=annual.fiscal_year.astype(str); ax.plot(x, annual.revenue/1e9, marker="o", label="Revenue", color="#2f6fc5"); ax.plot(x, annual.net_income/1e9, marker="o", label="Net income", color="#9fb0c6"); ax.set_title("Revenue and net income need one filing-aware definition", loc="left", weight="bold"); ax.set_ylabel("USD billions"); ax.legend(frameon=False); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-sec-performance.png",dpi=160); plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.8)); ax.plot(x,annual.net_margin*100,marker="o",color="#174a8b"); ax.set_title("Net margin shows whether growth translated into earnings",loc="left",weight="bold"); ax.set_ylabel("Net income / revenue (%)"); ax.set_xlabel("Fiscal year"); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-sec-margin.png",dpi=160); plt.close(fig)


def campaign() -> None:
    source = source_path("analysis_data/growth_sources/criteo-uplift-v2.1.csv.gz")
    result_path = source_path("analysis_data/growth_sources/criteo-itt-results.json")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    sql = duckdb.connect().execute("""
      select treatment, count(*) as assigned_users, sum(conversion) as conversions, sum(visit) as visits
      from read_csv_auto(?, header=true, compression='gzip') group by 1 order by 1
    """, [str(source)]).fetchdf()
    control, treatment = sql.iloc[0], sql.iloc[1]
    sql_lift = treatment.conversions / treatment.assigned_users - control.conversions / control.assigned_users
    if not np.isclose(sql_lift, result["conversion_itt"]["absolute_difference"]):
        raise ValueError("SQL and Python campaign lift do not reconcile")
    familywise_critical = NormalDist().inv_cdf(1 - 0.05 / (2 * len(result["f0_quartile_conversion"])))
    for band in result["f0_quartile_conversion"]:
        treatment_rate, control_rate = band["treatment_rate"], band["control_rate"]
        standard_error = np.sqrt(treatment_rate * (1 - treatment_rate) / band["treatment_n"] + control_rate * (1 - control_rate) / band["control_n"])
        band["bonferroni_p_value"] = min(1.0, band["p_value"] * len(result["f0_quartile_conversion"]))
        band["familywise_ci95"] = [band["absolute_difference"] - familywise_critical * standard_error, band["absolute_difference"] + familywise_critical * standard_error]
    incremental_per_100k = result["conversion_itt"]["absolute_difference"] * 100_000
    scenarios = [{"contribution_per_conversion": value, "break_even_spend_per_100k": incremental_per_100k * value} for value in (25, 50, 100, 200)]
    save_json("campaign.json", {
        "source": {"url": "https://ailab.criteo.com/criteo-uplift-prediction-dataset/", "retrieved_at": "2026-08-29T11:27:57Z", "sha256": digest(source)},
        "experiment": result,
        "reconciliation": {"sql_matches_python": True, "control_users": int(control.assigned_users), "treatment_users": int(treatment.assigned_users), "absolute_lift": float(sql_lift)},
        "economics_scenarios": scenarios,
        "limits": ["The release combines and subsamples experiments.", "The source contains no current spend, margin, or customer value."],
    })
    bands = pd.DataFrame(result["f0_quartile_conversion"])
    fig,ax=plt.subplots(figsize=(8,4.8)); y=bands.absolute_difference*100; low=(bands.absolute_difference-bands.familywise_ci95.map(lambda x:x[0]))*100; high=(bands.familywise_ci95.map(lambda x:x[1])-bands.absolute_difference)*100; ax.errorbar(bands.band.astype(str),y,yerr=[low,high],fmt="o",capsize=5,color="#174a8b"); ax.axhline(0,color="#737373",linewidth=1); ax.set_title("One anonymized band contains most measured lift",loc="left",weight="bold"); ax.set_xlabel("Exploratory f0 quartile"); ax.set_ylabel("Absolute conversion lift (percentage points)"); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-campaign-segments.png",dpi=160); plt.close(fig)


def marketplace() -> None:
    source = source_path("analysis_data/growth_sources/fhvhv_tripdata_2025-01.parquet")
    connection = duckdb.connect()
    quality = connection.execute("""
      select count(*) as row_count, count_if(request_datetime is null) missing_request,
      count_if(pickup_datetime is null) missing_pickup,
      count_if(pickup_datetime<request_datetime) negative_delay,
      count_if(date_diff('minute',request_datetime,pickup_datetime)>120) delay_over_120,
      min(request_datetime),max(request_datetime)
      from read_parquet(?)
    """, [str(source)]).fetchone()
    analysis_rows = connection.execute("""
      select count(*)
      from read_parquet(?)
      where request_datetime >= timestamp '2025-01-01'
        and request_datetime < timestamp '2025-02-01'
    """, [str(source)]).fetchone()[0]
    segments = connection.execute("""
      with valid as (
        select hvfhs_license_num provider, PULocationID pickup_zone, cast(request_datetime as date) request_date, extract('hour' from request_datetime)::int request_hour,
          date_diff('second',request_datetime,pickup_datetime)/60.0 pickup_delay_minutes,
          driver_pay,base_passenger_fare
        from read_parquet(?)
        where request_datetime >= timestamp '2025-01-01'
          and request_datetime < timestamp '2025-02-01'
          and pickup_datetime>=request_datetime
          and date_diff('minute',request_datetime,pickup_datetime)<=120
      )
      select provider,pickup_zone,request_hour,count(*) completed_trips,median(pickup_delay_minutes) median_delay,
        quantile_cont(pickup_delay_minutes,.9) p90_delay,avg(driver_pay) avg_driver_pay,avg(base_passenger_fare) avg_fare
      from valid group by 1,2,3 having completed_trips>=500 order by p90_delay desc
    """, [str(source)]).fetchdf()
    zones = pd.read_csv(source_path("analysis_data/growth_sources/taxi_zone_lookup.csv"))[["LocationID", "Zone"]].rename(columns={"LocationID":"pickup_zone", "Zone":"zone_name"})
    segments = segments.merge(zones, on="pickup_zone", how="left")
    stability = connection.execute("""
      with valid as (
        select hvfhs_license_num provider, PULocationID pickup_zone, cast(request_datetime as date) request_date, extract('hour' from request_datetime)::int request_hour,
          date_diff('second',request_datetime,pickup_datetime)/60.0 pickup_delay_minutes
        from read_parquet(?)
        where request_datetime >= timestamp '2025-01-01'
          and request_datetime < timestamp '2025-02-01'
          and pickup_datetime>=request_datetime
          and date_diff('minute',request_datetime,pickup_datetime)<=120
      ), daily as (
        select provider,pickup_zone,request_hour,request_date,count(*) completed_trips,quantile_cont(pickup_delay_minutes,.9) p90_delay
        from valid group by 1,2,3,4 having completed_trips>=20
      ) select provider,pickup_zone,request_hour,count(*) observed_daily_windows,
        count_if(p90_delay>=12) days_p90_at_least_12,
        median(p90_delay) median_daily_p90_delay
      from daily group by 1,2,3
    """, [str(source)]).fetchdf()
    segments = segments.merge(stability, on=["provider", "pickup_zone", "request_hour"], how="left")
    hourly = connection.execute("""
      select extract('hour' from request_datetime)::int request_hour,count(*) completed_trips,
        median(date_diff('second',request_datetime,pickup_datetime)/60.0) median_delay,
        quantile_cont(date_diff('second',request_datetime,pickup_datetime)/60.0,.9) p90_delay
      from read_parquet(?)
      where request_datetime >= timestamp '2025-01-01'
        and request_datetime < timestamp '2025-02-01'
        and pickup_datetime>=request_datetime
        and date_diff('minute',request_datetime,pickup_datetime)<=120
      group by 1 order by 1
    """, [str(source)]).fetchdf()
    for frame in (segments, hourly):
        for column in ("median_delay", "p90_delay", "avg_driver_pay", "avg_fare", "median_daily_p90_delay"):
            if column in frame:
                frame[column] = frame[column].round(6)
    priority = segments[(segments.observed_daily_windows >= 20)].sort_values(
        ["p90_delay", "completed_trips", "provider", "pickup_zone", "request_hour"],
        ascending=[False, False, True, True, True],
        kind="mergesort",
    ).head(20)
    save_json("marketplace.json", {
        "source": {"url": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page", "retrieved_at": "2026-08-29T12:24:06Z", "sha256": digest(source)},
        "quality": {"rows": quality[0], "analysis_rows": analysis_rows, "missing_request": quality[1], "missing_pickup": quality[2], "negative_delay": quality[3], "delay_over_120_minutes": quality[4], "first_request": str(quality[5]), "last_request": str(quality[6])},
        "analysis_window": {"start": "2025-01-01T00:00:00", "end": "2025-02-01T00:00:00", "timestamp_field": "request_datetime"},
        "selection_rule": "Within the January request-time window, require at least 500 completed trips in the month and at least 20 observed daily windows, then rank by completed-trip P90 pickup delay.",
        "hourly": hourly.to_dict(orient="records"), "priority_zone_hours": priority.to_dict(orient="records"),
        "limits": ["Pickup delay is conditional on completed trips.", "The file does not contain unmatched requests, cancellations, or online driver hours."],
    })
    fig, ax1 = plt.subplots(figsize=(8, 4.8)); ax1.plot(hourly.request_hour,hourly.completed_trips/1000,color="#9fb0c6",linewidth=2,label="Completed trips (000s)"); ax1.set_ylabel("Completed trips (thousands)"); ax2=ax1.twinx(); ax2.plot(hourly.request_hour,hourly.p90_delay,color="#174a8b",linewidth=2,label="P90 pickup delay"); ax2.set_ylabel("P90 request-to-pickup minutes"); ax1.set_title("Busy hours and long pickup delays do not fully overlap",loc="left",weight="bold"); ax1.set_xlabel("Request hour"); ax1.spines[["top"]].set_visible(False); ax2.spines[["top"]].set_visible(False); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-marketplace-hourly.png",dpi=160); plt.close(fig)
    shown=priority.head(12).sort_values("p90_delay"); shown["label"]=shown.provider+" | "+shown.zone_name.fillna("Zone "+shown.pickup_zone.astype(str))+" | "+shown.request_hour.astype(str).str.zfill(2)+":00"; fig,ax=plt.subplots(figsize=(8,5.6)); ax.barh(shown.label,shown.p90_delay,color="#2f6fc5"); ax.set_title("Airport windows dominate the longest pickup-delay tail",loc="left",weight="bold"); ax.set_xlabel("90th percentile request-to-pickup minutes"); style(ax); fig.tight_layout(); fig.savefig(IMAGE_OUT / "senior-marketplace-priority.png",dpi=160); plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="product,financial,retention,campaign,service,marketplace")
    args = parser.parse_args()
    cases = {"product": product_events, "financial": financial_metrics, "retention": online_retail, "campaign": campaign, "service": service_queues, "marketplace": marketplace}
    for name in args.cases.split(","):
        cases[name.strip()]()
        print(f"built {name.strip()}")


if __name__ == "__main__":
    main()
