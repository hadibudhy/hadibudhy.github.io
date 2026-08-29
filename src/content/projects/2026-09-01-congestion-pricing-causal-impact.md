---
title: "Congestion Pricing: Building a Causal Marketplace Read"
date: 2026-09-01
categories: [growth analytics]
tags: [econometrics, causal inference, marketplace, experimentation]
excerpt: "A cautious econometric design for measuring how NYC congestion pricing may affect trips, fares, driver economics, and geographic substitution."
problem: "A policy change can coincide with seasonality, weather, provider mix, and rider substitution, so a simple before-and-after chart can give leadership the wrong answer."
result: "TLC added a CBD congestion-fee field from 2025 onward; the validated January 2025 yellow file contains 3,475,226 trips and 2,246,495 positive-fee rows, but this alone cannot identify a causal effect."
featured: false
published: false
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

Use a difference-in-differences event study with policy exposure defined from origin, destination, and documented charge rules. A pickup-only flag is too narrow because the charge can apply to trips to, from, within, or through the zone. Matched controls must be plausibly untreated, and ambiguous through-trips and border spillovers must be handled explicitly. Include zone and time fixed effects; treat provider mix and route composition as diagnostics unless they are pre-treatment covariates. Use a pre-specified dependence strategy for standard errors.

Before estimating an effect, check parallel trends and placebo dates. Measure trip volume, fare, driver pay, duration, airport flows, and border-zone substitution. A policy can reduce CBD trips while increasing nearby trips, so citywide totals and cross-zone flows are necessary guardrails.

## What the Current Evidence Supports

The January 2025 yellow file confirms **3,475,226 trips** and **2,246,495 positive CBD-fee rows**. These figures validate the field and show that fee exposure is observable in the post-policy source. They do **not** show that congestion pricing caused a change in demand or supply.

The complete TLC monthly High Volume FHV subset adds **137 observations from January 2015 through May 2026**, including reported trips per day, unique drivers, unique vehicles, and average hours. An aggregate interrupted-series check estimates a post-policy level change of **-0.257 log points** (HAC p = **0.034**) but no statistically clear post-policy trend change (p = **0.110**). It is a broad-market diagnostic, not a causal policy estimate, because it has no untreated market or route-level exposure.

![TLC monthly High Volume FHV activity, January 2015–May 2026: the post-policy series shows a level shift, but this aggregate view cannot establish causality](/images/growth-hvf-monthly-its.png)

## Decision and Next Step

Do not change pricing or incentives from the current evidence. **P0:** complete 2024–2025 HVFHV monthly data and validate coverage. **P1:** run the event study and placebo tests. **P2:** evaluate pricing, incentive, airport, and border-zone actions only when estimates are stable and the substitution guardrail is understood.

## Risks and Limitations

The public records do not contain all requests, lost matches, driver online hours, or customer value. Policy exposure may spill into neighboring zones. Reporting completeness, provider mix, weather, holidays, and anticipation can invalidate a naive comparison.

## Supporting detail

The reproducible design and source notes live under `projects/growth-analytics/03-congestion-pricing-causal-impact`. Raw TLC files remain local and are not published.
