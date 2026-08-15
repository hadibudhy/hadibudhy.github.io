---
title: "New York Short-Term Rentals: Where Marketplace Supply Is Concentrated"
date: 2026-08-20
categories: [marketplace analysis]
tags: [marketplace, supply and demand, pricing, segmentation]
excerpt: "A listing-level marketplace review showing how room type, location, price, availability, and host concentration shape the supply side of New York’s rental market."
problem: "A marketplace can look large while supply is concentrated among a small group of hosts or unavailable at the times guests need it."
result: "The June 2026 snapshot contains 30,555 listings; after restricting price to $20–$1,000, 21,138 listings remained for a more credible price comparison, with a median listed price of $171."
featured: false
---

## Business context

Two-sided marketplaces must balance the needs of buyers and suppliers. Guests need choice, clear prices, and availability. Hosts need demand and a workable return. Platform teams should understand where supply is concentrated before treating listing growth as marketplace health.

## Business question

Where does New York marketplace supply sit, and which segments deserve closer attention from a platform team?

## Approach

I used the [Inside Airbnb New York City snapshot](https://insideairbnb.com/get-the-data/) dated 14 June 2026. I reviewed 30,555 listings by room type, borough, listed price, availability, reviews, and host listing count. Prices outside $20–$1,000 were excluded from the comparison; this is a quality filter, not a claim that those listings are impossible.

## Key findings

### Entire homes and private rooms dominate supply

The snapshot contains **16,808 entire-home listings** and **13,009 private-room listings**. Hotel and shared-room supply is much smaller. That mix matters because these segments serve different guest needs and may respond differently to fees, rules, and demand changes.

### Listed prices are incomplete, not observed booking prices

Among the filtered listings, the median listed price was **$171**. Price is missing for 8,758 rows, and the file does not record booking revenue. The number is therefore a supply-side price reference, not an average paid by guests.

### Host concentration can affect marketplace resilience

The largest observed hosts listed hundreds of properties, including one with 292 listings. A platform should monitor whether a small group controls a large share of supply, because policy or availability changes affecting those hosts could have an outsized marketplace effect.

## Recommendations

1. Report supply by room type, borough, price band, and availability together.
2. Track host concentration as a marketplace-health measure.
3. Add booking, occupancy, cancellation, and guest-quality data before claiming demand or revenue effects.
4. Design host policies separately for professional multi-listing hosts and smaller hosts.

## Takeaway

New York supply is large but not uniform. Marketplace decisions should protect choice across room types and locations while monitoring concentration and the difference between listed supply and actual bookings.

## Supporting detail

Inside Airbnb states that its data is collected from public Airbnb information and that accuracy is not guaranteed. The snapshot has 19 columns, no duplicate rows, 8,758 missing prices, and 25,269 missing license values. It is licensed CC BY 4.0; the analysis does not infer illegal or compliant status from missing license fields.
