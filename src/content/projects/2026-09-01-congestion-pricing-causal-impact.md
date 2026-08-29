---
title: "Congestion Pricing: Building a Causal Marketplace Read"
date: 2026-09-01
categories: [growth analytics]
tags: [econometrics, causal inference, marketplace, experimentation]
excerpt: "A cautious econometric design for measuring how NYC congestion pricing may affect trips, fares, driver economics, and geographic substitution."
problem: "A policy change can coincide with seasonality, weather, provider mix, and rider substitution, so a simple before-and-after chart can give leadership the wrong answer."
result: "TLC added a CBD congestion-fee field from 2025 onward; the validated January 2025 yellow file contains 3,475,226 trips and 2,246,495 positive-fee rows, but this alone cannot identify a causal effect."
featured: false
---

## Executive Summary

- **Decision:** should pricing, incentives, or geographic strategy change?
- **Policy date:** 5 January 2025.
- **Validated evidence:** the January 2025 TLC yellow file has 3,475,226 trips and 2,246,495 positive CBD-fee rows.
- **Causal boundary:** no policy effect is claimed from one post-policy month.
- **Next step:** complete monthly HVFHV pre/post data and run a difference-in-differences event study.

## Business Problem

Congestion pricing may change trip volume, passenger fares, driver pay, duration, and where trips start. Leadership needs an estimate that separates the policy from normal winter patterns and market-wide shocks.

## Dataset

The source is the official [NYC TLC trip-record collection](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). TLC states that the `cbd_congestion_fee` field was added to Yellow, Green, and HVFHV data from 2025 onward. Each row is a submitted trip. The intended marketplace file is HVFHV; the validated January yellow file is used for current schema and fee-field checks while the larger HVFHV download is completed.

## Analysis Design

Use a difference-in-differences event study with pickup inside the congestion zone as treatment and matched outside zones as control. Include zone fixed effects, date or hour fixed effects, weekday and holiday controls, weather where available, provider mix, and route composition. Cluster standard errors by zone.

Before estimating an effect, check parallel trends and placebo dates. Measure trip volume, fare, driver pay, duration, airport flows, and border-zone substitution. A policy can reduce CBD trips while increasing nearby trips, so citywide totals and cross-zone flows are necessary guardrails.

## What the Current Evidence Supports

The January 2025 yellow file confirms **3,475,226 trips** and **2,246,495 positive CBD-fee rows**. These figures validate the field and show that fee exposure is observable in the post-policy source. They do **not** show that congestion pricing caused a change in demand or supply.

## Decision and Next Step

Do not change pricing or incentives from the current evidence. **P0:** complete 2024–2025 HVFHV monthly data and validate coverage. **P1:** run the event study and placebo tests. **P2:** evaluate pricing, incentive, airport, and border-zone actions only when estimates are stable and the substitution guardrail is understood.

## Risks and Limitations

The public records do not contain all requests, lost matches, driver online hours, or customer value. Policy exposure may spill into neighboring zones. Reporting completeness, provider mix, weather, holidays, and anticipation can invalidate a naive comparison.

## Interview explanation

**30-second explanation:** “I treated congestion pricing as a causal inference problem, not a before-and-after chart. TLC added the CBD fee field in 2025, but one post-policy month cannot identify the effect. I would compare treated and matched control zones in an event study, check pre-trends and placebo dates, cluster by zone, and measure substitution at the border before recommending pricing or incentives.”

**2-minute explanation:** I would discuss treatment definition, parallel trends, fixed effects, clustered uncertainty, spillovers, seasonal controls, and the business decision rule.

## Supporting detail

The reproducible design and source notes live under `projects/growth-analytics/03-congestion-pricing-causal-impact`. Raw TLC files remain local and are not published.
