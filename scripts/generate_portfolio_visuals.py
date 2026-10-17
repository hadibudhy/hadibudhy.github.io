"""Generate small, source-labelled SVG visuals for the published case studies.

The numeric values in this file are limited to values already validated in the
portfolio source notes or the cited public dataset pages. Workflow diagrams are
explicitly labelled conceptual designs rather than observed business outcomes.
"""

from html import escape
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.chart_theme import ACCENT, BORDER, CANVAS, FONT, HIGHLIGHT, INK, MUTED, OBSERVED_FILL, PANEL, SECONDARY, WARNING, WARNING_FILL


OUT = Path(__file__).resolve().parents[1] / "public" / "images"
W, H = 1200, 680
SURFACE = CANVAS
ACCENT_2 = SECONDARY
ORANGE = WARNING
RED = HIGHLIGHT


def text(x, y, value, size=22, fill=INK, weight=400, anchor="start"):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="{FONT}, sans-serif" font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'


def wrap(x, y, value, width=42, size=18, fill=MUTED, line_height=26, weight=400, anchor="start"):
    words = str(value).split()
    lines, line = [], []
    for word in words:
        candidate = " ".join(line + [word])
        if len(candidate) > width and line:
            lines.append(" ".join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(" ".join(line))
    return "".join(text(x, y + i * line_height, line_value, size, fill, weight, anchor) for i, line_value in enumerate(lines))


def shell(title, subtitle, source, body, footnote=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(subtitle)} Source: {escape(source)}.</desc>
  <rect width="{W}" height="{H}" fill="{SURFACE}"/>
  <rect x="48" y="42" width="10" height="90" rx="5" fill="{ACCENT}"/>
  {wrap(82, 72, title, 72, 28, INK, 34, 700)}
  {wrap(82, 150, subtitle, 96, 18, MUTED, 24)}
  {body}
  {text(82, 635, f"Source: {source}", 15, MUTED)}
  {text(1118, 635, footnote, 15, MUTED, anchor="end")}
</svg>'''


def write(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")


def facts(name, title, subtitle, items, source, footnote="Observed source metadata"):
    body = []
    x_positions = [82, 360, 638, 916]
    for x, (value, label, note) in zip(x_positions, items):
        body.append(f'<rect x="{x}" y="235" width="238" height="260" fill="{PANEL}" stroke="{BORDER}"/>')
        body.append(wrap(x + 24, 292, value, 15, 28, ACCENT, 32, 700))
        body.append(wrap(x + 24, 354, label, 18, 19, INK, 25, 700))
        body.append(wrap(x + 24, 432, note, 18, 16, MUTED, 23))
    write(name, shell(title, subtitle, source, "".join(body), footnote))


def bars(name, title, subtitle, labels, values, unit, source, footnote, highlight_index=None):
    max_value = max(values) or 1
    body = [text(82, 215, unit, 16, MUTED, 700)]
    base_y = 505
    chart_h = 250
    gap = 24 if len(values) > 4 else 80
    bar_w = (970 - gap * (len(values) - 1)) / len(values) if len(values) > 4 else 160
    chart_x = 110 if len(values) > 4 else 170
    for i, (label, value) in enumerate(zip(labels, values)):
        x = chart_x + i * (bar_w + gap)
        height = chart_h * value / max_value
        y = base_y - height
        body.append(f'<line x1="110" y1="{base_y}" x2="1080" y2="{base_y}" stroke="{BORDER}" stroke-width="2"/>')
        color = HIGHLIGHT if i == highlight_index else ACCENT
        body.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{height:.1f}" fill="{color}"/>')
        body.append(text(x + bar_w / 2, y - 18, f"{value:g}", 24, INK, 700, "middle"))
        label_width = 16 if len(values) <= 4 else max(8, int(bar_w / 9))
        body.append(wrap(x + bar_w / 2, base_y + 34, label, label_width, 17 if len(values) <= 4 else 15, INK, 22, 700, "middle"))
    write(name, shell(title, subtitle, source, "".join(body), footnote))


def horizontal_bars(name, title, subtitle, labels, values, unit, source, footnote=""):
    maximum = max(values)
    axis_max = ((maximum + 199_999) // 200_000) * 200_000
    left, right, top, bottom = 300, 1080, 250, 520
    step = 200_000
    body = [text(82, 222, unit, 16, MUTED, 700)]
    for tick in range(0, axis_max + 1, step):
        x = left + (right - left) * tick / axis_max
        body.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="{BORDER}" stroke-width="1"/>')
        body.append(text(x, 553, f"{tick:,}", 15, MUTED, 400, "middle"))
    row_gap = (bottom - top) / len(labels)
    bar_height = min(44, row_gap * 0.55)
    for i, (label, value) in enumerate(zip(labels, values)):
        center_y = top + row_gap * (i + 0.5)
        width = (right - left) * value / axis_max
        body.append(text(left - 18, center_y + 7, label, 18, INK, 400, "end"))
        body.append(f'<rect x="{left}" y="{center_y - bar_height / 2:.1f}" width="{width:.1f}" height="{bar_height:.1f}" fill="{ACCENT if i == 0 else SECONDARY}"/>')
        body.append(text(min(left + width + 12, 1110), center_y + 7, f"{value:,}", 17, INK, 700))
    write(name, shell(title, subtitle, source, "".join(body), footnote))


def timeline(name, title, subtitle, events, source, footnote="Time boundary from source documentation"):
    body = [f'<line x1="120" y1="370" x2="1080" y2="370" stroke="{BORDER}" stroke-width="5"/>']
    left, right = 140, 1060
    step = (right - left) / max(1, len(events) - 1)
    for i, (period, label, color) in enumerate(events):
        x = left + i * step
        body.append(f'<circle cx="{x}" cy="370" r="14" fill="{color}"/>')
        body.append(text(x, 315 if i % 2 == 0 else 447, period, 20, INK, 700, "middle"))
        body.append(wrap(x, 270 if i % 2 == 0 else 495, label, 22, 16, MUTED, 21, anchor="middle"))
    write(name, shell(title, subtitle, source, "".join(body), footnote))


def observability(name, title, subtitle, observed, missing, source, footnote="Observed vs not observed", observed_label="Observed in the public source"):
    body = [
        f'<rect x="82" y="220" width="480" height="310" fill="{OBSERVED_FILL}" stroke="{ACCENT_2}"/>',
        f'<rect x="638" y="220" width="480" height="310" fill="{WARNING_FILL}" stroke="{ORANGE}"/>',
        text(112, 270, observed_label, 22, ACCENT_2, 700),
        text(668, 270, "Not observed / do not claim", 22, ORANGE, 700),
    ]
    for i, value in enumerate(observed):
        body.append(text(120, 320 + i * 48, "✓", 22, ACCENT_2, 700))
        body.append(wrap(155, 320 + i * 48, value, 32, 18, INK, 23))
    for i, value in enumerate(missing):
        body.append(text(676, 320 + i * 48, "-", 22, ORANGE, 700))
        body.append(wrap(711, 320 + i * 48, value, 32, 18, INK, 23))
    write(name, shell(title, subtitle, source, "".join(body), footnote))


def flow(name, title, subtitle, steps, source, footnote="Conceptual design - not an observed outcome", conceptual=True):
    body = [text(82, 208, "CONCEPTUAL DESIGN", 15, ACCENT, 700)] if conceptual else []
    y = 300
    gap = 32 if len(steps) <= 4 else 20
    box_w = (1036 - gap * (len(steps) - 1)) / len(steps)
    for i, (label, detail) in enumerate(steps):
        x = 82 + i * (box_w + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="170" fill="{PANEL}" stroke="{BORDER}"/>')
        body.append(text(x + 24, y + 48, f"0{i + 1}", 18, ACCENT, 700))
        body.append(wrap(x + 20, y + 88, label, max(15, int(box_w / 11)), 19, INK, 23, 700))
        body.append(wrap(x + 20, y + 137, detail, max(15, int(box_w / 11)), 15, MUTED, 20))
        if i < len(steps) - 1:
            x1 = x + box_w + 8
            x2 = x + box_w + gap - 8
            body.append(f'<line x1="{x1}" y1="{y + 85}" x2="{x2}" y2="{y + 85}" stroke="{ACCENT}" stroke-width="3"/>')
            body.append(f'<path d="M {x2 - 10} {y + 76} L {x2} {y + 85} L {x2 - 10} {y + 94}" fill="none" stroke="{ACCENT}" stroke-width="3"/>')
    write(name, shell(title, subtitle, source, "".join(body), footnote))


def generate():
    # New project visuals
    event_manifest = json.loads((OUT.parent / "data" / "evidence" / "product-event-foundation.json").read_text(encoding="utf-8"))
    event_counts = event_manifest["validation"]["eventCounts"]
    event_rows = event_manifest["validation"]["eventRows"]
    missing_session_rows = event_manifest["validation"]["missingSessionRows"]
    funnel = event_manifest["validation"]["sessionFunnel"]
    assert sum(event_counts.values()) == event_rows == 885_129
    assert missing_session_rows == 165
    assert {key: funnel[key] for key in (
        "user_session_pairs", "view_sessions", "view_then_cart_sessions", "view_cart_purchase_sessions"
    )} == {
        "user_session_pairs": 490_633,
        "view_sessions": 488_586,
        "view_then_cart_sessions": 41_232,
        "view_cart_purchase_sessions": 20_699,
    }
    horizontal_bars(
        "rees46-event-mix.svg",
        "Product views make up most recorded events",
        f"Observed REES46 event rows by type; {event_rows:,} rows in the loaded file.",
        ["View", "Cart", "Purchase"],
        [event_counts["view"], event_counts["cart"], event_counts["purchase"]],
        "Recorded event rows",
        "REES46 Electronics behaviour export",
        "Event counts are not user conversion rates",
    )
    observability(
        "rees46-quality-checks.svg",
        "Keep 165 events without a session ID out of session conversion",
        "The event model validates keys and categories while preserving the missing-session boundary.",
        ["885,129 recorded events across view, cart, and purchase", "unique event_id and accepted event types", "timestamps parsed at the event grain"],
        [f"{missing_session_rows} rows have no user_session", "event totals alone do not measure unique users", "session conversion needs identified sessions"],
        "REES46 Electronics behaviour export and quality mart",
        observed_label="Validated or directly observed",
    )
    flow(
        "rees46-model-grain.svg",
        "Keep event grain before creating session and funnel metrics",
        "The implemented model separates source events, typed staging, and ordered session marts.",
        [("Raw events", "source rows, unchanged"), ("Typed staging", "keys, time, identity"), ("Product marts", "sessions, funnel, quality")],
        "REES46 Electronics behaviour export and local dbt project",
        "Implemented data model",
        conceptual=False,
    )
    horizontal_bars(
        "rees46-session-funnel.svg",
        "Only 4.2% of user-session pairs contain a full event sequence",
        "20,699 of 490,633 user-session pairs contain view, then cart, then purchase events; events are not verified transactions.",
        ["Identified sessions", "Sessions with view", "View then cart", "View, cart, purchase"],
        [funnel["user_session_pairs"], funnel["view_sessions"], funnel["view_then_cart_sessions"], funnel["view_cart_purchase_sessions"]],
        "User-session pairs in the 24 Sep 2020 to 28 Feb 2021 file",
        "REES46 Electronics behaviour export; local DuckDB sequence by event time and source row",
        "Session grain combines user_id and user_session; event sequence is not verified order conversion",
    )

    shopper_metrics = json.loads((OUT.parent / "data" / "online-shoppers-metrics.json").read_text(encoding="utf-8"))
    visitor = shopper_metrics["visitor_conversion"]
    raw_visitor = shopper_metrics["raw_visitor_conversion"]
    page_values = shopper_metrics["mean_page_values"]
    new_rate = 100 * visitor["New_Visitor"]["rate"]
    returning_rate = 100 * visitor["Returning_Visitor"]["rate"]
    conversions = sum(item["conversions"] for item in visitor.values())
    bars("portfolio-online-shoppers-visitor.svg", f"New visitors converted {new_rate - returning_rate:.1f} points more often than returning visitors", f"Revenue=True share after exact-row deduplication; n={shopper_metrics['deduplicated_sessions']:,} sessions across ten months of 2018.", [f"New visitor (n={visitor['New_Visitor']['sessions']:,})", f"Other (n={visitor['Other']['sessions']:,})", f"Returning visitor (n={visitor['Returning_Visitor']['sessions']:,})"], [round(new_rate, 1), round(100 * visitor["Other"]["rate"], 1), round(returning_rate, 1)], "Session conversion rate (%)", "UCI Online Shoppers Purchasing Intention dataset", "Descriptive, not causal")
    bars("portfolio-online-shoppers-pagevalue.svg", "PageValues strongly separates outcomes-but its timing is unverified", f"Mean PageValues by Revenue outcome after exact-row deduplication; n={shopper_metrics['deduplicated_sessions']:,} sessions.", [f"Revenue=True (n={conversions:,})", f"Revenue=False (n={shopper_metrics['deduplicated_sessions'] - conversions:,})"], [round(page_values["true"], 1), round(page_values["false"], 1)], "Mean PageValues", "UCI Online Shoppers Purchasing Intention dataset", "Unsafe until timing is verified")
    bars("portfolio-online-shoppers-sensitivity.svg", "The visitor contrast survives the exact-row deduplication choice", "Revenue=True share before and after removing 125 exact-identical rows; raw n=12,330, deduplicated n=12,205.", ["New: raw", "New: deduplicated", "Returning: raw", "Returning: deduplicated"], [round(100 * raw_visitor["New_Visitor"]["rate"], 1), round(new_rate, 1), round(100 * raw_visitor["Returning_Visitor"]["rate"], 1), round(returning_rate, 1)], "Session conversion rate (%)", "UCI Online Shoppers Purchasing Intention dataset", "Sensitivity to row treatment")
    flow("portfolio-online-shoppers-experiment.svg", "Test the observed visitor gap instead of treating it as lift", "The completed analysis identifies a segment contrast; a randomized prompt is still required to estimate incremental conversion.", [("Eligibility", "Visitor type and early browsing only"), ("Randomize", "Prompt versus no prompt"), ("Measure", "Conversion, bounce, seven-day return")], "UCI session analysis and proposed experiment")

    event_manifest = json.loads((OUT.parent / "data" / "evidence" / "product-event-foundation.json").read_text(encoding="utf-8"))
    event_counts = event_manifest["validation"]["eventCounts"]
    event_rows = event_manifest["validation"]["eventRows"]
    missing_session_rows = event_manifest["validation"]["missingSessionRows"]
    assert sum(event_counts.values()) == event_rows == 885_129
    assert missing_session_rows == 165
    facts("portfolio-instacart-scale.svg", "Instacart exposes the sequence needed for reorder analysis", "The public release is relational: the decision depends on preserving order, product, and reorder grain.", [("3.4M", "orders", "Order sequence and cadence"), ("206,209", "users", "Anonymous user histories"), ("49,688", "products", "Product and aisle metadata"), ("6", "linked tables", "Orders, products, taxonomy, and labels")], "Instacart public release and competition documentation")
    observability("portfolio-instacart-evidence.svg", "Reorder history is observable; incremental value is not", "The visual keeps the growth hypothesis separate from the economics the public release cannot measure.", ["order_number and days_since_prior_order", "product-level reordered flag", "aisle and department context"], ["reminder assignment or holdout", "inventory and substitutions", "margin and incremental orders"], "Instacart public release")
    flow("portfolio-instacart-holdout.svg", "A replenishment-first test protects against spam and substitution", "Use history to select candidates, then test whether the reminder creates an additional order.", [("Select", "Known repeat products"), ("Hold out", "No reminder control"), ("Decide", "Incremental orders and margin")], "Instacart fields and proposed growth experiment")

    timeline("portfolio-google-analytics-window.svg", "The public Google Analytics release is historical, not current budget evidence", "Feature and target windows must be kept separate before comparing acquisition quality.", [("Aug 2016–Apr 2018", "training visits", ACCENT), ("May–Oct 2018", "forward test visits", ACCENT_2), ("Dec 2018–Jan 2019", "competition target period; not in file", ORANGE)], "Google Analytics Customer Revenue Prediction source documentation")
    flow("portfolio-google-analytics-grain.svg", "Aggregate visits to users before making a value decision", "The competition target is total future revenue per user, not revenue per individual visit.", [("Visit", "Channel, device, traffic, date"), ("User-period", "Keep fullVisitorId as string"), ("Value", "Future revenue target")], "Google Analytics Customer Revenue Prediction")
    flow("portfolio-google-analytics-holdout.svg", "Channel ranking should lead to a holdout, not an automatic budget shift", "Historical prediction can shortlist tests; only incremental contribution should set spend.", [("Rank", "Calibrated user value"), ("Hold out", "Business-as-usual channel policy"), ("Scale", "Contribution above paid cost")], "Google Analytics Customer Revenue Prediction")

    facts("portfolio-wikimedia-api-grain.svg", "Wikimedia pageviews provide an explicit product-demand grain", "The API separates the dimensions needed to distinguish durable interest from a temporary spike.", [("Page", "article or project", "Content unit"), ("Period", "daily or monthly", "Trend window"), ("Access", "desktop, mobile, app", "Experience context"), ("Agent", "human or automated", "Traffic quality")], "Wikimedia Analytics API")
    observability("portfolio-wikimedia-boundary.svg", "Pageview persistence is useful context, not user retention", "The public API supports content prioritization but cannot identify a reader returning to an article.", ["pageview time series", "access and agent mix", "peak-to-baseline and recovery"], ["unique article-level readers", "comprehension or satisfaction", "causal refresh impact"], "Wikimedia Analytics API")
    flow("portfolio-wikimedia-queue.svg", "Separate spike response from durable-interest maintenance", "Use aggregate evidence to prioritize the queue, then measure reader outcomes in first-party telemetry.", [("Classify", "Spike or stable floor"), ("Refresh", "Content and related links"), ("Validate", "Depth and return in holdout")], "Wikimedia Analytics API and product test design")

    facts("portfolio-movielens-scale.svg", "MovieLens is large enough to test relevance and catalog coverage separately", "The stable GroupLens release supports offline ranking diagnostics, not watch-time claims.", [("25M", "ratings", "User × movie feedback"), ("1M", "tag applications", "Semantic signals"), ("62,000", "movies", "Catalog denominator"), ("162,000", "users", "Historical raters")], "GroupLens MovieLens 25M")
    observability("portfolio-movielens-boundary.svg", "Offline rating evidence cannot stand in for product engagement", "The recommendation decision needs a clear boundary between what the dataset measures and what an online test must add.", ["timestamped ratings", "movie and tag metadata", "offline relevance and coverage"], ["impressions and exposure", "watch completion or subscription", "online satisfaction and retention"], "GroupLens MovieLens 25M")
    flow("portfolio-movielens-test.svg", "Keep popularity as a benchmark while testing controlled exploration", "The decision is a relevance-versus-coverage trade-off, not a single opaque score.", [("Benchmark", "Popularity baseline"), ("Personalize", "History and tags"), ("Test", "Coverage and satisfaction guardrails")], "GroupLens MovieLens 25M")

    bars("portfolio-stackoverflow-audience.svg", "Professional developers are the majority, but not the whole survey audience", "2025 Stack Overflow Developer Survey; the remainder includes learners and adjacent roles.", ["Professional developers", "Aspirational/adjacent", "Other respondents"], [76, 15, 9], "Share of respondents (%)", "Stack Overflow Developer Survey 2025, n=49,019", "Unweighted descriptive context")
    bars("portfolio-stackoverflow-age.svg", "The survey’s largest age band is 25–44, not a complete product segment", "Age is one answered survey question; use its own denominator rather than the total for every question.", ["Age 25–44", "Other / not in band"], [66, 34], "Share of respondents (%)", "Stack Overflow Developer Survey 2025", "Question-specific denominator")
    flow("portfolio-stackoverflow-telemetry.svg", "Survey demand should become an onboarding experiment", "Self-reported AI use can choose the hypothesis; first-success telemetry should decide the product investment.", [("Survey", "Segment hypothesis"), ("Instrument", "Activation and task success"), ("Test", "Guidance versus control")], "Stack Overflow Developer Survey and product test design")

    observability("portfolio-citibike-grain.svg", "Citi Bike has two useful grains that must not be joined as one outcome", "Trip history and station status answer different parts of the station-experience decision.", ["one ride: time and origin/destination", "one station snapshot: bikes and docks", "member/casual and rideable type"], ["failed unlock or empty search", "full-destination abandonment", "causal rebalancing impact"], "Citi Bike System Data and GBFS")
    flow("portfolio-citibike-imbalance.svg", "Directional flow is a better rebalancing cue than station popularity", "The analytical view follows real origin and destination fields; it is not a claim that low flow equals low demand.", [("Count", "Origins and destinations"), ("Compare", "Direction by peak window"), ("Prioritize", "Moves plus rider guidance")], "Citi Bike System Data")
    flow("portfolio-citibike-test.svg", "Rebalancing needs a service-outcome holdout", "Completed trips are a lower bound on demand; failed-search and availability events make the decision measurable.", [("Instrument", "Search, unlock, dock-full"), ("Pilot", "Station-window priority"), ("Measure", "Successful rides and repeat use")], "Citi Bike System Data and GBFS")

    facts("portfolio-olist-scale.svg", "Olist’s 100,000 orders connect delivery promise to customer feedback", "The public release is a relational order history spanning 2016–2018.", [("100k", "orders", "Commercial order entity"), ("2016–2018", "observation window", "Historical marketplace"), ("9", "relational files", "Order, seller, item, payment, review"), ("1", "primary decision grain", "Order before child joins")], "Olist Brazilian E-commerce Public Dataset")
    observability("portfolio-olist-boundary.svg", "Delivery promise and review are observable; root cause and profit are not", "The diagnostic keeps seller, carrier, product, and commercial conclusions separate.", ["estimated and actual delivery dates", "seller, product, freight, review", "one-to-many order relationships"], ["carrier identity and scan events", "unplaced or cancelled demand", "order contribution margin"], "Olist Brazilian E-commerce Public Dataset")
    flow("portfolio-olist-pilot.svg", "A delivery-quality queue should route the cause before coaching the seller", "Use the public relationship as a diagnostic and validate interventions on current lanes.", [("Diagnose", "Promise gap and review"), ("Route", "Seller, carrier, or product"), ("Pilot", "Coaching versus control")], "Olist Brazilian E-commerce Public Dataset")

    facts("portfolio-census-market-measures.svg", "County Business Patterns gives three complementary market-structure measures", "The decision needs scale, density, and workforce depth-not population alone.", [("County", "geography", "Market unit"), ("NAICS", "industry", "Comparable scope"), ("Count", "establishments", "Supply density"), ("2 measures", "employment + payroll", "Operating scale")], "U.S. Census County Business Patterns")
    observability("portfolio-census-suppression.svg", "Suppression is part of the expansion decision", "A market screen must distinguish observed values from protected or unavailable small-area data.", ["annual county × NAICS records", "establishments and employment", "payroll and year-over-year context"], ["customer demand and willingness to pay", "competitor quality and share", "suppressed values as exact numbers"], "U.S. Census County Business Patterns")
    flow("portfolio-census-screen.svg", "Use Census structure to choose research markets, not to forecast revenue", "The screen narrows commercial research; a localized demand test makes the expansion decision.", [("Screen", "Scale, density, stability"), ("Enrich", "ACS and competitor context"), ("Pilot", "Localized incremental demand")], "U.S. Census County Business Patterns")

    facts("portfolio-nyc311-scale.svg", "NYC 311 is large enough to require queue-level workload metrics", "The current public dataset exposes request lifecycle and geography, but closure remains an administrative event.", [("22.2M", "rows", "Request-level public table"), ("44", "columns", "Lifecycle and location fields"), ("1", "service request", "Primary grain"), ("Daily", "updates", "Mutable public source")], "NYC Open Data 311 Service Requests, source page checked August 2026")
    observability("portfolio-nyc311-boundary.svg", "A closed request is not the same as a resolved issue", "Capacity decisions should show arrivals, backlog age, and administrative close time separately.", ["created and closed timestamps", "complaint type and agency", "status and location"], ["consistent resolution quality", "true resident need", "staff hours and first-response time"], "NYC 311 public dataset and 311 reporting definitions")
    flow("portfolio-nyc311-pilot.svg", "Move capacity toward the oldest actionable work, then test the result", "The public data supports prioritization; the pilot supplies the missing service-quality evidence.", [("Measure", "Arrivals and backlog age"), ("Pilot", "Routing or staffing change"), ("Guardrail", "Reopen and follow-up")], "NYC 311 public dataset")

    facts("portfolio-sec-fact-grain.svg", "SEC Company Facts carries the lineage needed for a trustworthy finance mart", "Reported values are reusable only when their tag, unit, period, and filing identity stay visible.", [("Tag", "reported concept", "Taxonomy meaning"), ("Unit", "USD or shares", "Scale and comparability"), ("Period", "instant or duration", "Fiscal meaning"), ("Accession", "filing identity", "Audit lineage")], "SEC Company Facts API")
    observability("portfolio-sec-period-boundary.svg", "Reported facts are authoritative records, not automatic cross-company comparables", "The mart must expose semantic and period exceptions before a dashboard compares issuers.", ["value, form, tag, unit", "fiscal period and filing date", "amendment and source lineage"], ["same operating definition across issuers", "restatement-free original history", "economic performance explanation"], "SEC Company Facts API")
    flow("portfolio-sec-mart.svg", "Ship a narrow reconciled metric layer before expanding tag coverage", "A governed finance mart is the decision artifact; maximum raw fact coverage is not.", [("Land", "Raw issuer JSON"), ("Normalize", "Fact and period grain"), ("Approve", "Finance-reconciled metrics")], "SEC Company Facts API")

    flow("portfolio-ocds-lifecycle.svg", "OCDS connects a contract’s lifecycle without collapsing its event history", "The real standard links planning, tender, award, contract, and implementation through an OCID.", [("Plan", "Need and budget"), ("Tender", "Notice and bids"), ("Award", "Supplier and value"), ("Contract", "Signed terms"), ("Implement", "Progress and payments")], "Open Contracting Data Standard")
    observability("portfolio-ocds-boundary.svg", "A missing implementation stage is not evidence of clean delivery", "Stage completeness belongs beside every procurement indicator.", ["release and record identifiers", "OCID-linked stages", "parties, dates, values, amendments"], ["complete payments for every publisher", "cross-country legal equivalence", "misconduct proven by one indicator"], "Open Contracting Data Standard and OCP Data Registry")
    flow("portfolio-ocds-gate.svg", "Check publisher completeness before scoring procurement red flags", "The first decision is whether a process is comparable enough for a human review queue.", [("Ingest", "Immutable releases"), ("Profile", "Stage completeness"), ("Review", "Flag with lineage")], "Open Contracting Data Standard")

    facts("portfolio-faa-sdr-scope.svg", "FAA Service Difficulty Reports support safety-minded triage, not a fleet failure rate", "Annual files contain submitted reports from operators and repair stations; the reporting process is selected.", [("2016–2026", "annual files", "Historical source window"), ("1", "processed report", "Analysis grain"), ("Narrative", "text evidence", "Technical description"), ("Coded context", "system fields", "Retrieval and review")], "FAA Service Difficulty Reports")
    observability("portfolio-faa-sdr-boundary.svg", "Safety triage can organize evidence while human reviewers decide action", "The source does not provide the exposure denominator or an automatic airworthiness label.", ["submitted malfunction/failure/defect text", "aircraft and system context", "report year and identifiers"], ["all flights or installed fleet", "true failure probability", "safe automatic disposition"], "FAA Service Difficulty Reports")
    flow("portfolio-faa-review.svg", "Evaluate the assistant on critical-case recall and reviewer overrides", "Rare safety cases make aggregate accuracy the wrong launch headline.", [("Retrieve", "Similar cited reports"), ("Escalate", "Low confidence or critical"), ("Decide", "Qualified human review")], "FAA Service Difficulty Reports")

    facts("portfolio-fcc-complaint-scope.svg", "FCC complaint records are useful for routing, not verified provider prevalence", "The public source contains individual informal complaints beginning October 31, 2014.", [("2014–", "observation start", "Historical complaint stream"), ("1", "informal complaint", "Primary grain"), ("Issue", "structured topic", "Routing taxonomy"), ("Not verified", "source caveat", "Allegation boundary")], "FCC CGB Consumer Complaints Data")
    observability("portfolio-fcc-boundary.svg", "The complaint source supports queue design but not a provider failure rate", "Consumer selection and unverified allegations must remain visible in the AI workflow.", ["issue and complaint fields", "date and provider/location context", "narrative where available"], ["representative consumer prevalence", "verified provider fault", "resolution quality from routing alone"], "FCC CGB Consumer Complaints Data")
    flow("portfolio-fcc-routing.svg", "Use confidence-based routing with a human path for sensitive and novel cases", "A safe workflow measures corrections and escalation, not just automated coverage.", [("Redact", "Protect complaint text"), ("Suggest", "Queue and cited fields"), ("Escalate", "Low confidence or sensitive")], "FCC CGB Consumer Complaints Data")

    # Existing published projects: add only the missing visuals needed to reach three.
    facts("portfolio-restaurant-triage.svg", "Restaurant inspection work needs an inspection-level quality queue", "The validated 2022–2025 rollup contains 73,211 inspections, including 30,037 without a recorded grade.", [("73,211", "inspection records", "One inspection grain"), ("30,037", "without grade", "Follow-up uncertainty"), ("2022–2025", "analysis window", "Comparable period"), ("1", "inspection", "Not one row per violation")], "NYC Restaurant Inspection Results")
    bars("portfolio-retail-cleaning.svg", "Cleaning customer identity changes the growth denominator", "The UCI Online Retail release contains missing customer IDs and transaction rows that must be handled before retention analysis.", ["Raw rows", "Missing CustomerID", "Identifiable customers"], [541909, 135080, 4338], "Records / customers (different units)", "UCI Online Retail validation record", "Do not compare unlike units as a rate")
    flow("portfolio-complaintflow-log.svg", "ComplaintFlow turns every AI decision into an auditable workflow record", "The reference design keeps input validation, redaction, retrieval, escalation, and logging distinct.", [("Validate", "Schema and PII"), ("Retrieve", "Approved playbook"), ("Escalate", "Uncertainty"), ("Log", "Evidence and outcome")], "ComplaintFlow reference implementation")
    flow("complaintflow-architecture.svg", "ComplaintFlow routes uncertain cases to a human before release", "The conceptual workflow validates and redacts input, retrieves approved guidance, checks output, escalates uncertainty, and records each decision.", [("Validate", "Complaint API and PII"), ("Retrieve", "Approved playbook or baseline"), ("Check", "Provider response and evidence"), ("Decide", "Answer or human escalation"), ("Log", "Audit trail and outcome")], "ComplaintFlow reference architecture")
    observability("portfolio-complaintflow-boundary.svg", "A synthetic fixture validates software behavior, not real-world model quality", "The system contract is testable; production performance needs privacy-reviewed labeled complaints.", ["routing schema and fallbacks", "provider retries and audit log", "evaluation slices in fixture"], ["representative complaint prevalence", "hosted-model production accuracy", "real customer resolution impact"], "ComplaintFlow project documentation", observed_label="Implemented / tested in the repository")
    facts("portfolio-complaintflow-fixture.svg", "The 20-case fixture passes the routing contract-not a production benchmark", "Checked local evaluation output on hand-written standard, unknown, PII, paraphrase, and short cases.", [("20", "fixture cases", "Small synthetic contract test"), ("1.00", "macro-F1", "Baseline and service"), ("100%", "routed citation coverage", "17 of 17 routed cases"), ("3", "human escalations", "All unknown cases")], "ComplaintFlow checked evaluation fixture", "Synthetic validation evidence")
    campaign_metrics = json.loads((OUT.parent / "data" / "evidence" / "experiment-metrics.json").read_text(encoding="utf-8"))["metrics"]["visit_itt"]
    visit_lift = campaign_metrics["absolute_lift_pp"]
    bars("portfolio-campaign-economics.svg", f"Advertising assignment increased visits by {visit_lift:.3f} percentage points", f"Intention-to-treat visit rates: control n={campaign_metrics['control_users']:,} and assigned advertising n={campaign_metrics['treatment_users']:,}. 95% CI for lift: +{campaign_metrics['ci95_pp'][0]:.3f} to +{campaign_metrics['ci95_pp'][1]:.3f}pp.", ["Assigned control", "Assigned advertising"], [100 * campaign_metrics["control_rate"], 100 * campaign_metrics["treatment_rate"]], "Users with a visit (%)", "Criteo Uplift Modeling Dataset", "Visits are not purchases or profit")
    bars("portfolio-campaign-f0.svg", "One anonymized feature band contains most of the exploratory lift", "Intention-to-treat conversion difference across complete f0 quartiles; n=13,979,592 benchmark rows. Bands are not customer personas.", ["f0 Q1", "f0 Q2", "f0 Q3", "f0 Q4"], [0.038, 0.386, 0.019, 0.010], "Absolute conversion lift (percentage points)", "Criteo Uplift Modeling Dataset", "Exploratory; retest before targeting", highlight_index=1)
    flow("portfolio-campaign-holdout.svg", "The next campaign decision is a randomized holdout with an economic stop rule", "Assignment remains the treatment definition; exposure, CPA, and contribution are measured after launch.", [("Assign", "Treatment or holdout"), ("Measure", "Incremental conversion"), ("Scale", "CPA below contribution")], "Criteo Uplift Modeling Dataset")
    observability("portfolio-marketplace-measurement.svg", "Recorded trips show activity, not the complete marketplace demand funnel", "The public TLC data is useful context for a pilot, not evidence for a citywide incentive rollout.", ["recorded trips by hour and zone", "monthly driver and vehicle proxies", "official source aggregation"], ["all requests and lost matches", "true wait and cancellations", "incentive ROI and contribution"], "NYC TLC public data")
    facts("portfolio-mta-panel-scope.svg", "Panel size does not validate the comparator", "The panel covers 10 facilities and 388 weeks; the pre-policy gap still needs formal review.", [("27,080", "facility-day rows", "10 facilities"), ("3,880", "facility-week rows", "388 weeks"), ("10", "facilities", "Crossing locations"), ("−26 to +26", "event weeks", "Diagnostic window")], "MTA Bridges and Tunnels Hourly Crossings")
    observability("portfolio-mta-causal-boundary.svg", "An unstable pre-policy gap is a warning, not a policy effect", "The selected comparison changes before the policy; this descriptive screen is not a formal parallel-trends test.", ["facility-day car crossings", "policy event date", "weekly comparison-gap diagnostic"], ["ride-hailing fee exposure", "validated untreated comparison", "causal effect from this comparator"], "MTA Bridges and Tunnels Hourly Crossings")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    generate()
    print("generated portfolio visuals in", OUT)
