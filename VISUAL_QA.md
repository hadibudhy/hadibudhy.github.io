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

The repository has 35 current Next.js project articles and four legacy Jekyll posts. Across all 39 content files there are 92 unique image references, including one decorative MDS teaser. The public image directory contains 109 image files total; the remaining 17 are unreferenced legacy or support assets. All 109 were visually reviewed in the atlas screenshots under `visual-tests/actual/`.

- 87 chart and diagram assets were regenerated from available source files or restyled from existing analysis outputs. Data assertions cover available source files.
- Eleven unreferenced chart or diagram assets were also restyled or refreshed to keep the public image directory coherent.
- `/images/portfolio-nyc311-metrics.svg` was reviewed and retained because its light palette and observed, derived, and unavailable metric groups already fit the shared system. The legacy MDS teaser was retained as a decorative illustration, not a data chart.
- The Fake Job overview was restyled from the stored metric values, but the model was not rerun. Five supporting charts remain in their previous visual form because the exact source model outputs are not present in this repository: `fake-job-keywords.png`, `fake-job-shap.png`, `fake-job-threshold-cv.png`, `fake-job-model-comparison.png`, and `fake-job-confusion-matrices.png`. The first three are referenced by a draft article. All five were reviewed but not redrawn, so their original values were not altered. Four other unreferenced images are portraits, a waterfront photo, or a formula illustration.

Airfare, Airbnb host concentration, happiness, clickstream, bank response, credit default, taxi, restaurant, JOLTS, Netflix, REES46, and the generated evidence diagrams were regenerated from available source files or official reported values. Chart source checks include the original input hashes and assertions for key reported figures. The Airbnb, happiness, taxi, Netflix, and airfare article values were corrected to match their source calculations.

## Validation

- `python scripts/verify_published_evidence.py`: 7 published projects verified.
- `npm run lint`: passed.
- `npm run build`: passed.
- Python generator syntax check: passed.
- No original source data files were overwritten. A local Netflix snapshot was added for regeneration and hash-checked; raw data remains excluded from Git.

See `CHART_STYLE_GUIDE.md` for the shared palette, layout rules, and evidence boundaries.
