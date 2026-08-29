---
title: "New York Short-Term Rentals: Finding Marketplace Concentration"
date: 2026-08-20
categories: [marketplace analysis]
tags: [marketplace, supply and demand, pricing, concentration]
excerpt: "A supply-side marketplace analysis that separates listing growth from marketplace health and identifies where concentration creates risk."
problem: "A large listing count does not prove healthy demand, fair choice, or resilient supply."
result: "The June 2026 snapshot has 30,555 listings; 24.7% of listings belong to the top 1% of observed hosts, and the filtered median listed price is $171."
featured: false
header:
  teaser: /images/airbnb-room-supply.png
---

## Executive summary

**Business problem:** protect marketplace choice and resilience while balancing hosts and guests.

**Evidence strength:** Medium for visible supply and concentration in one snapshot; low for bookings, occupancy, revenue, and customer outcomes.

**Key findings:** supply is dominated by entire homes and private rooms; 24.7% of listings are controlled by the top 1% of observed hosts; 8,758 listings have missing prices; and listings are not bookings.

**Decision implication:** platform policy can have an outsized effect if professional hosts control a large share of visible supply, but demand and revenue cannot be inferred from listings alone.

**Recommended action:** monitor concentration and availability, then add booking data before changing marketplace investment.

## Business question

**Decision owner:** Marketplace GM. **Decision:** where should the platform invest in supply, trust, or demand? **North-star KPI:** successful booked nights with acceptable guest experience. **Drivers:** active supply, availability, price, demand, host quality, and location. **Guardrails:** cancellations, complaints, regulatory risk, and host concentration.

## My role

I owned the snapshot validation, supply segmentation, host-concentration analysis, chart, and measurement-first marketplace recommendation for this independent portfolio case. I did not observe bookings, host interventions, or guest outcomes.

## Why it matters

A large visible supply base can still produce poor choice if listings are unavailable, unaffordable, or controlled by a small group. Growth decisions need demand and booking evidence, not only listings.

## Data used

The validated snapshot contains **30,555 listings, 19 columns, and no duplicate rows**. It includes **16,808 entire-home** and **13,009 private-room** listings. After restricting price to $20–$1,000, 21,138 listings remained and the median listed price was **$171**.

The top 1% of observed hosts account for **24.7% of listings**. This is a concentration risk, not proof that these hosts create most bookings. Missing price and license values also require separate treatment; missing license is not evidence of non-compliance.

![Inside Airbnb New York snapshot, June 14 2026: Entire homes and private rooms made up almost all of 30,555 visible listings](/images/airbnb-room-supply.png)

![Inside Airbnb New York snapshot, June 14 2026: The top 1% of observed hosts controlled 24.7% of visible listings](/images/airbnb-host-concentration.png)

## Approach

The conservative opportunity is to reduce supply concentration risk without removing productive hosts: improve onboarding and visibility for smaller hosts. The expected case adds booking and occupancy data by neighbourhood and room type. The ambitious case tests targeted supply incentives. The trade-off is that incentives can add supply but reduce platform contribution or increase regulatory exposure.

## Key findings

- The June 2026 snapshot contains **30,555 visible listings**, mostly entire homes and private rooms.
- The top 1% of observed hosts account for **24.7% of listings**, a concentration signal rather than a booking share.
- Listings are not bookings; occupancy, revenue, demand, and customer choice remain unmeasured.

## Recommendation

- **P0 — Act now:** add host concentration, active availability, price coverage, and cancellation to the marketplace scorecard.
- **P1 — Test:** run a smaller-host activation experiment in a high-demand, low-choice segment.
- **P2 — Investigate:** join bookings, reviews, response time, and regulatory status before claiming customer or revenue impact.

Primary metric is booked nights per active listing; guardrails are cancellation, complaints, guest rating, host retention, and contribution. Repeat concentration using top 0.5%, 1%, and 5% definitions.

## Key takeaway

Marketplace health is not listing count. It is reliable choice, demand conversion, and resilient supply. The current data identifies concentration clearly and shows exactly which missing measures must be added before making a commercial decision.

## What internal data would improve the decision

Bookings, occupied nights, availability, search demand, conversion, host response, cancellations, reviews, contribution, and regulatory status would reveal whether concentration harms customer choice or service quality.

## Technical appendix

Source: [Inside Airbnb](https://insideairbnb.com/get-the-data/), New York snapshot dated 14 June 2026, CC BY 4.0. The source describes public listing data and warns that accuracy is not guaranteed. No bookings, occupancy, revenue, or causal policy effect is available.
