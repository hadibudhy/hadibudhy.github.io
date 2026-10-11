# Visual QA

## Published pages

The seven published case studies were opened from the local static export at desktop (1440px) and mobile (375px) widths. The 14 full-page screenshots are in `visual-tests/actual/`.

| Published route | Desktop | Mobile | Charts |
|---|---|---|---:|
| `/projects/2026-09-05-product-event-foundation` | Pass | Pass | 3 |
| `/projects/2026-09-05-financial-metrics` | Pass | Pass | 3 |
| `/projects/2026-09-05-service-metric-reliability` | Pass | Pass | 3 |
| `/projects/2026-08-15-online-retail-customer-growth` | Pass | Pass | 3 |
| `/projects/marketplace-supply-demand` | Pass | Pass | 3 |
| `/projects/campaign-incrementality` | Pass | Pass | 3 |
| `/projects/mta-congestion-pricing-causal-audit` | Pass | Pass | 3 |

All renders returned HTTP 200. Each page loaded its three chart images with non-empty alt text. No page-level horizontal overflow was detected. At mobile width, charts remain reachable in focusable horizontal scroll regions with an accessible scroll hint.

## Repository-wide chart inventory

The repository has 35 current Next.js project articles and four legacy Jekyll posts. Across all 39 content files, there are 91 unique referenced image assets; the legacy posts add no new assets. Every referenced asset was visually reviewed in the chart atlas screenshots under `visual-tests/actual/`.

- 84 visuals were regenerated from available source files or restyled from existing analysis outputs. Data assertions cover available source files.
- `/images/portfolio-nyc311-metrics.svg` was reviewed and retained because its light palette and observed, derived, and unavailable metric groups already fit the shared system.
- Six draft charts remain in their previous visual form because the source data or saved model artifacts are not present in this repository: `fake-job-keywords.png`, `fake-job-shap.png`, `fake-job-threshold-cv.png`, `netflix-beat01.png`, `netflix-beat03.png`, and `netflix-beat05.png`. The Netflix analysis README confirms its raw catalog file is not included. These assets were reviewed but not redrawn, so their original values were not altered.

Airfare, Airbnb host concentration, happiness, clickstream, bank response, credit default, taxi, restaurant, JOLTS, REES46, and the generated evidence diagrams were regenerated from available source files or official reported values. Chart source checks include the original input hashes and assertions for key reported figures. The Airbnb and taxi article values were corrected to match their source calculations.

## Validation

- `python scripts/verify_published_evidence.py`: 7 published projects verified.
- `npm run lint`: passed.
- `npm run build`: passed.
- Python generator syntax check: passed.
- No raw source data files were modified.

See `CHART_STYLE_GUIDE.md` for the shared palette, layout rules, and evidence boundaries.
