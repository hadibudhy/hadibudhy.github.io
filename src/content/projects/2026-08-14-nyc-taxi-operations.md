---
title: "NYC Taxi Operations: Matching Capacity to the Right Trips"
date: 2026-08-14
categories: [operations]
tags:
  - operations
  - unit economics
  - geospatial analysis
  - python
excerpt: "A large-scale trip analysis showing when demand peaks and why airport-linked trips need a different operating plan."
problem: "Taxi demand was not evenly distributed across time or location, making a single operating plan inefficient."
result: "After filtering 3.48 million raw records, the analysis showed that evening demand peaked in Manhattan while airport-linked areas produced longer, higher-value trips."
featured: true
header:
  teaser: /images/taxi-demand-by-hour.png
---

## Business context

Taxi operators have to make decisions about where to position vehicles, when to add capacity, and which trips deserve a different service plan. A monthly trip file can answer those questions if the analysis separates demand volume from trip economics.

## Business question

When and where should a taxi operator focus capacity, and which trip types should be managed as a separate operating lane?

## How I approached it

I used the January 2025 yellow taxi trip file and joined pickup location IDs to the TLC taxi-zone lookup. I removed records with non-positive distance or fare and excluded trips shorter than one minute or longer than two hours. I then compared trip volume, duration, and average fare by pickup hour and borough.

## Finding 1: The busiest demand window was the early evening

Valid trips peaked at **241,585 pickups at 18:00**, with demand also high at 17:00 and 19:00. Manhattan accounted for **2.96 million of 3.31 million valid trips**, or about **89%** of the cleaned sample.

![Taxi demand peaked between 17:00 and 19:00](/images/taxi-demand-by-hour.png)

**Business meaning:** A broad, all-day capacity plan would miss the most important window. Vehicle availability and dispatch coverage should be strongest before and during the evening peak.

## Finding 2: Airport-linked areas had a different trip profile

Queens pickups averaged **32.0 minutes** and **$72.12 per trip**, compared with **12.8 minutes** and **$22.34** in Manhattan. The JFK Airport pickup zone alone recorded **133,337 valid trips**, with an average duration of **38.4 minutes** and an average fare of **$81.11**.

![Airport-linked areas had longer, higher-value trips while Manhattan carried most of the volume](/images/taxi-zone-economics.png)

These trips are not directly comparable with short Manhattan trips. They use vehicles for longer periods, involve different pickup patterns, and create different revenue per trip. Treating every zone as the same operating problem would hide that difference.

## Finding 3: Data quality could change the operating picture

The raw file contains **3,475,226 rows**, but **90,893** have non-positive trip distance and **145,516** have non-positive fare amounts. Optional fields such as passenger count and rate code are also missing in more than 540,000 rows.

**Business meaning:** The demand pattern is useful for planning, but any dispatch or revenue scorecard should publish its cleaning rules. Otherwise, invalid records can distort zone comparisons.

## Recommendations

1. **Protect 17:00-19:00 capacity in Manhattan.** Use the evening peak as the first staffing and vehicle-positioning test.
2. **Manage airport-linked service separately.** Track JFK and other airport zones with their own targets for trip duration, revenue per trip, and vehicle utilization.
3. **Review zone performance with both volume and value.** High demand does not automatically mean the best economics; compare trips, time occupied, and fare together.
4. **Make data-quality rules part of the operating report.** Keep invalid-distance and invalid-fare counts visible so decisions are based on a known denominator.

## Takeaway

The biggest operational opportunity is not simply adding more taxis. It is matching capacity and service rules to two different patterns: high-volume evening demand in Manhattan and longer, higher-value airport-linked trips.

## Supporting technical detail

The source is the [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). The case uses the January 2025 yellow taxi Parquet file and the official [taxi-zone lookup](https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv). The TLC notes that records come from technology-provider submissions and may not be fully accurate or complete. This analysis describes observed trip patterns; it does not measure wait time, driver supply, traffic speed, or profit.

**Data dictionary:** [Read the TLC trip record documentation](https://www.nyc.gov/assets/tlc/downloads/pdf/trip_record_user_guide.pdf)
