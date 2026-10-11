# Chart style guide

This guide covers charts and evidence diagrams in the seven case studies currently published by the site. The common style sets the visual identity; each chart keeps the form that best answers its question.

## Editorial principles

- Lead with the finding when the evidence supports a clear finding. Use a descriptive title for exploratory or inconclusive results.
- Put the measure, population, period, and unit in the subtitle or axis labels.
- Place a short annotation beside the data it explains. Keep exact values available on the chart.
- Use one chart for one question. Separate measures with different units or denominators.
- Keep uncertainty, missing data, and proxy measures visible. Do not imply causation when the design is descriptive.
- Choose the chart type for the question: lines for time, bars for comparisons, points for effects and intervals, and tables for exact summaries.

These principles are informed by Chartosaur's [takeaway-title analysis](https://www.chartosaur.com/blog/washington-post-music-nostalgia-chart), [Likert chart critique](https://www.chartosaur.com/blog/likert-scale-responses), and [marginal-plot example](https://www.chartosaur.com/blog/heatmap-marginal-plots). Instagram was unavailable during this review, so no claim is made about its examples.

## Tokens

| Token | Value | Use |
|---|---|---|
| Canvas | `#FAFAF8` | Chart background, matched to the site |
| Paper | `#FFFFFF` | High-contrast table or annotation surface |
| Ink | `#202B30` | Titles, values, and primary labels |
| Muted | `#52636B` | Axis labels, subtitles, and source notes |
| Border | `#C9D3D8` | Axis rules and table separators |
| Grid | `#E3E9EC` | Sparse reference lines |
| Accent | `#225B73` | Primary series or estimate |
| Secondary | `#64867E` | A second meaningful series or group |
| Highlight | `#B45435` | A specific event, threshold, or key point |
| Warning | `#94632C` | Evidence limits or unavailable measures |

Color never carries meaning alone. Labels, position, markers, or line style provide a second cue.

## Typography and layout

- Use Arial with a sans-serif fallback across SVG and PNG charts.
- Use sentence case, with one takeaway title, one concise context line, and compact source notes.
- Use consistent title, subtitle, data-label, and source-note weights and sizes from `scripts/chart_theme.py`.
- Use a 16:9 canvas for raster charts and a 1200 by 680 viewBox for SVGs.
- Keep chart margins consistent. Remove top and right borders; use only the gridlines needed to read values.
- Prefer direct labels. Keep a legend only when direct labeling would make the chart harder to read.

## Data and accessibility rules

- Start comparison bars at zero unless a clearly marked alternative is required by the question.
- Show denominators and units. Separate measures with different units rather than sharing a scale.
- Label estimates and confidence intervals directly. State when intervals or causal estimates are unavailable.
- Label partial periods, proxies, and descriptive comparisons at the point of use.
- Use meaningful alternative text, a takeaway caption, and keyboard-focusable horizontal scrolling on narrow screens.
- Preserve the source records and metric calculations. Regenerate chart assets from their source scripts and verify the manifest hashes.

## Reusable implementation

`scripts/chart_theme.py` owns the shared Matplotlib tokens and axis helpers. `scripts/generate_portfolio_visuals.py` uses the same tokens for SVG evidence graphics. Article-specific generators set data, chart form, labels, and annotations without changing the shared palette.
