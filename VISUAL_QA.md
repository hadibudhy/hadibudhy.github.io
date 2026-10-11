# Visual QA

## Published pages

The portfolio has 12 published case-study routes. The seven established pages were previously captured at desktop (1440px) and mobile (375px) widths; their full-page screenshots remain in `visual-tests/actual/`. The three source-backed legacy analyses and two new public-data analyses were opened from the local static export at desktop and mobile widths during this revision.

| Published route | Desktop | Mobile | Charts |
|---|---|---|---:|
| `/projects/2026-09-05-product-event-foundation` | Pass | Pass | 3 |
| `/projects/2026-09-05-financial-metrics` | Pass | Pass | 3 |
| `/projects/2026-09-05-service-metric-reliability` | Pass | Pass | 3 |
| `/projects/2026-08-15-online-retail-customer-growth` | Pass | Pass | 3 |
| `/projects/marketplace-supply-demand` | Pass | Pass | 3 |
| `/projects/campaign-incrementality` | Pass | Pass | 3 |
| `/projects/mta-congestion-pricing-causal-audit` | Pass | Pass | 3 |
| `/projects/2026-05-03-netflix-content-strategy` | Pass | Pass | 4 |
| `/projects/2026-05-10-world-happiness-report` | Pass | Pass | 5 |
| `/projects/2026-05-10-fake-job-detection` | Pass | Pass | 4 |
| `/projects/2026-10-12-commercial-electricity-costs` | Pass | Pass | 3 |
| `/projects/2026-10-12-college-program-outcome-coverage` | Pass | Pass | 3 |

All 12 routes are generated in the static export. Browser inspection confirmed the five newly published pages render their Problem, Hypotheses, Analysis, and Result sections, with chart images carrying descriptive alt text. Their mobile headers and tag groups wrap without clipping, and their charts use focusable horizontal scroll regions with an accessible scroll hint. The project listing exposes all five new links under Completed Analyses.

## Repository-wide chart inventory

The repository has 37 current Next.js project articles and four archived Jekyll posts. Across all 41 content files there are 98 unique image references, including one decorative MDS teaser. The public image directory contains 115 image files total; 17 are unreferenced legacy or support assets. The 109 earlier files were included in the previous atlas review. The four regenerated Fake Job V2 charts and six new public-data charts were inspected individually after this revision.

- 87 chart and diagram assets were regenerated from available source files or restyled from existing analysis outputs. Data assertions cover available source files.
- Eleven unreferenced chart or diagram assets were also restyled or refreshed to keep the public image directory coherent.
- `/images/portfolio-nyc311-metrics.svg` was reviewed and retained because its light palette and observed, derived, and unavailable metric groups already fit the shared system. The MDS teaser is a decorative illustration, not a data chart.
- The published Fake Job article now uses four regenerated V2 charts, based on a rerun of the model from the recovered source snapshot. Two unused V1 charts remain as unreferenced legacy assets: `fake-job-model-comparison.png` and `fake-job-confusion-matrices.png`.
- The commercial electricity case uses three charts from a complete 2019 to 2025 EIA state and U.S. snapshot. The College Scorecard case uses three charts from the June 2026 field-of-study file after collapsing repeated branch-campus outcomes.

Airfare, Airbnb host concentration, happiness, clickstream, bank response, credit default, taxi, restaurant, JOLTS, Netflix, REES46, Fake Job, and the generated evidence diagrams were regenerated from available source files or official reported values. Chart source checks include original input hashes and assertions for key reported figures. The Airbnb, happiness, taxi, Netflix, Fake Job, and airfare article values were checked against their source calculations.

## Validation

- `python scripts/verify_published_evidence.py`: 12 published projects verified.
- `npm run lint`: passed.
- `npm run build`: passed and generated all 12 published case-study routes.
- Python syntax checks for the updated chart and case-study scripts: passed.
- No U+2014 em dash characters were found in active checkout text files. Ignored nested worktrees contain their own historical copies and were left unchanged.
- No original source data files under `analysis_data/raw` were overwritten. The Netflix, Happiness, and Fake Job source snapshots were checksum-checked locally and remain excluded from Git.

See `CHART_STYLE_GUIDE.md` for the shared palette, layout rules, and evidence boundaries. See `PORTFOLIO_REVIEW.md` for the case-study inventory and source limitations.
