---
title: "County Business Patterns: Choose Expansion Markets With Demand and Density in View"
date: 2026-08-30
categories: [business decision analytics]
tags: [market sizing, Census, location strategy, NAICS]
excerpt: "A market-screening framework using Census business counts, employment, and payroll to avoid choosing an expansion location from population or establishment count alone."
problem: "A commercial team needs to shortlist markets, but a large population does not guarantee a reachable customer base, competitive supply, or enough businesses in the target industry."
result: "The Census County Business Patterns program provides annual county × NAICS observations for establishments, employment, and payroll, with suppression markers that must remain visible in the market screen."
published: true
---

## Business question

Which counties deserve the next expansion investigation when the decision depends on market size, industry density, workforce depth, and competitive intensity?

## Why it matters

Expansion has fixed research and launch costs. A market can look attractive by population while having few target establishments, low employment density, or a competitive structure that makes entry uneconomic.

## Decision brief

- **Recommendation:** use County Business Patterns as a first-pass screen, not a standalone go/no-go model; shortlist markets that meet separate thresholds for target-industry establishments, employment, and recent stability.
- **Evidence:** [Census County Business Patterns](https://www.census.gov/programs-surveys/cbp.html) provides annual establishment, employment, and payroll measures by county and NAICS industry.
- **Evidence strength:** Moderate for market structure; low for customer demand, willingness to pay, or forecast revenue.
- **Main risk:** payroll and employment fields can be suppressed or grouped, and establishments are not customers.
- **Next test:** enrich the shortlist with ACS demographics, competitor research, travel time, and a localized demand test.

## Role

Role: Census API extraction, NAICS grain design, suppression handling, market-screen metric definition, and decision-threshold framing.

## Data used

The source is the U.S. Census Bureau’s [County Business Patterns program](https://www.census.gov/programs-surveys/cbp.html). Each observation is a county × industry × year record with business establishments, employment, and payroll measures. A market-screening view can aggregate to a county while retaining the industry hierarchy and suppression flags.

This is administrative business data, not a customer panel. It does not contain revenue, foot traffic, digital demand, market share, or the location quality of individual establishments.

## Approach

1. Pull a fixed release year and record the Census API query.
2. Keep NAICS codes at the level required for the decision; do not mix broad and narrow industries silently.
3. Separate observed zero, missing, and suppressed values.
4. Compare establishments per worker, target-industry employment, payroll intensity, and year-over-year stability.
5. Convert the screen into a research queue with explicit follow-up evidence.

## Key findings

### Establishment count and demand are different quantities

A county can have many target establishments because competition is dense, not because unmet demand is high.

**Meaning:** supply density is useful context and can be a competitive risk.

**Why it matters:** expansion scoring should not reward every large establishment count.

### Employment adds a scale check that establishments miss

Two counties with the same number of establishments can support very different numbers of jobs and operating scale.

**Meaning:** employment and payroll help distinguish small presence from meaningful industry depth.

**Why it matters:** the shortlist should retain separate scale and density measures instead of hiding them in one opaque score.

### Suppression is an uncertainty signal

Small-area business statistics may use range codes or suppression for confidentiality.

**Meaning:** an apparently precise ranking can be false precision.

**Why it matters:** markets with suppressed target values need primary research, not automatic exclusion or inclusion.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | Annual county × NAICS records provide establishments, employment, payroll, and suppression status | Screen market structure and industry depth |
| Inferred | A market with target-industry scale and stable supply deserves investigation | Allocate commercial research time |
| Not established | Establishments are customers, or a county screen predicts revenue | Enrich with demand and competitor evidence |

## Validation record

- **Grain:** county × NAICS × year.
- **Checks:** release year and NAICS level are explicit; suppressed/range values remain status fields.
- **Guardrail:** location quotient and composite screens are not presented as demand or profit estimates.

## Recommendation

**What:** build a two-stage expansion screen: objective Census thresholds first, commercial validation second.

**Where / who:** focus analyst time on counties with enough target-industry employment and stable recent observations, then investigate competition and reachable demand.

**Why:** the public data is strong for market structure and weak for revenue prediction.

**Risk:** a composite score can conceal trade-offs and create an appealing but untestable ranking.

**Next action:** field-test the top markets with a localized acquisition or partner pilot and compare incremental contribution.

## Evidence strength and limitations

The source is annual and county-level. It cannot prove market demand, customer willingness to pay, competitor quality, or a causal effect of expansion. Suppressed values, NAICS revisions, boundary changes, and time lags need to be documented for every release.

## Reproducibility

Source and program documentation: [Census County Business Patterns](https://www.census.gov/programs-surveys/cbp.html). The [expansion validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md) records grain and suppression treatment.

## Technical appendix

Use the Census API with an explicit `NAICS2017` query and release year. Preserve `D` and `S`-style suppression or range indicators as status fields; never coerce them to zero. Calculate location quotient only after selecting a consistent industry and comparison geography.
