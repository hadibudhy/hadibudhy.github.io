# Portfolio completion gate — 2026-08-30

This record supersedes the publication decisions in `portfolio-expansion-2026-08.md` and `project-quality-matrix-2026-08.md`. A source description, proposed method, or conceptual workflow is not a completed project-specific result.

## Publication rule

A page is public only when checked code produces a decision-relevant result from identified real records or validated system behavior; the population or validation scope, period where relevant, grain, denominator, source identity, and limitations are stated; and at least three declared project-evidence visuals support the result. Measured data, validated model or system output, actual architecture or data flow, and data-quality evidence can count. A proposed conceptual workflow may be additional context but does not count toward the minimum.

## Current decisions

| 2026-08-30 study | Decision | Exact reason |
|---|---|---|
| Online Shoppers activation | Publish as completed | Checked computation on 12,205 exact-row-deduplicated UCI sessions; pinned source hash and metrics manifest; three measured visuals plus one experiment-design visual |
| Instacart reorder growth | Hide | No checked project-specific computation or measured result visuals |
| Google Merchandise acquisition | Hide | No checked project-specific computation or measured result visuals |
| Wikimedia discovery | Hide | No checked API extract, metric output, or measured result visuals |
| MovieLens recommendation coverage | Hide | No executed offline evaluation or measured result visuals |
| Stack Overflow developer adoption | Hide | Source-level summary statistics are not a completed project analysis |
| Citi Bike station experience | Hide | No checked trip extract, station-window result, or measured result visuals |
| Olist delivery marketplace | Hide | No checked order-level computation or measured result visuals |
| Census market expansion | Hide | No executed county ranking or measured result visuals |
| NYC 311 response capacity | Hide | No checked queue-level computation or measured result visuals |
| SEC XBRL mart | Hide | No executed mart, reconciliation output, or measured result visuals |
| Open Contracting mart | Hide | No executed mart, data-quality output, or measured result visuals |
| FAA SDR triage | Hide | No authentic held-out labels or model evaluation |
| FCC complaint routing | Hide | No authentic held-out labels or model evaluation |

## Online Shoppers quality gate

| Requirement | Status | Evidence |
|---|---|---|
| Business readability | Pass | Opens with the activation decision, states exact rates and denominators, and separates the historical finding from the proposed test |
| Data storytelling | Pass | Context, leakage conflict, and experiment decision form one clear narrative; four visuals have conclusion-led titles |
| Analytical credibility | Pass | Deduplication, all visitor-group denominators, source hash, arithmetic assertions, leakage boundary, and observational limits are explicit |
| Decision judgment | Pass | Rejects the strongest-looking downstream field, stratifies the next test, and adds experience guardrails |

The first draft failed because it had one visual and no published computation; it was revised before publication.

## Online Shoppers stakeholder gate

| Stakeholder lens | Status | What works | Remaining evidence gap |
|---|---|---|---|
| Recruiter | Pass | The 24.9% versus 14.1% contrast is scannable and the chart sequence explains the story quickly | Historical setting limits brand relevance |
| Hiring Manager | Pass | The result, leakage rejection, and next experiment demonstrate practical analyst judgment | No causal lift or customer value |
| Data Manager | Pass | Checked code, source hash, all visitor denominators, duplicate handling, and manifest make the claims auditable | No unique-user key |
| Country Manager | Pass | The segment priority and leakage risk are understandable without technical translation | No margin or current-market estimate |
| Business Stakeholder | Pass | The visuals make the target, risk, and next action easier to understand | A randomized test is required before investment |

These are internal editorial checks, not claims that external reviewers endorsed the page.

## Commands

```text
py scripts/analyze_online_shoppers.py <downloaded-csv> --output public/data/online-shoppers-metrics.json
py scripts/generate_portfolio_visuals.py
py scripts/verify_published_evidence.py
```
