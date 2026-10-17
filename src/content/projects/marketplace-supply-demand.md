---
title: "Ride-Hail Data Audit: Trips Alone Cannot Diagnose a Shortage"
date: 2026-08-29
categories: [growth analytics]
tags: [marketplace, supply and demand, experimentation, SQL]
excerpt: "A retrospective audit of NYC trip and driver summaries that shows why recorded activity cannot locate a current supply shortage."
problem: "Leaders had trip counts from one historical week and annual driver summaries, but neither source shows current requests, waits, or zone-time supply."
result: "The official records describe past completed-trip activity and separate monthly driver proxies; they are not sufficient to target current incentives or identify unserved demand."
featured: true
kind: flagship
published: true
caseId: marketplace-experience
primaryTrack: product-analytics
secondaryTracks: [analytics-engineering]
displayOrder: 40
evidenceManifest: /data/evidence/marketplace-experience.json
evidenceVisuals:
  - /images/growth-hvf-hourly.png
  - /images/growth-hvf-weekday.png
  - /images/growth-hvf-monthly-supply.png
  - /images/growth-hvf-monthly-matched.png
  - /images/portfolio-marketplace-measurement.svg
---
## Project brief

- **Project:** Audit the time and grain mismatch in public NYC ride-hail measures.
- **Question:** Can these public summaries identify a current supply shortage or support an incentive change?
- **Built:** Hourly and weekday views of one 2019 trip week, a separate 2024–25 driver-proxy comparison, and a measurement-boundary map.
- **Result:** No. The sources describe different periods and omit current requests, waits, and zone-time supply, so they cannot target a current intervention.

## Business question

Leadership hears that riders wait longer and rides are lost in some areas, and wants to know whether driver incentives should increase. Recorded trips alone cannot tell whether a quiet period had low demand or weak supply, or whether a busy period still left riders unserved.

The decision is whether these public sources can justify a current city or zone-level incentive change. This analysis is a data-sufficiency audit, not a current shortage map.

## Data and preparation

The analysis combines two different official sources: a one-week trip table for **1–7 February 2019** and monthly High Volume FHV reports for **2024 and 2025**. They are separate descriptive views, not one continuous time series. The trip table records submitted dispatched trips; it does not show every request, rejected match, cancellation, wait, or online driver-hour.

The hourly aggregation checks all 24 hour buckets and the total of 4,965,012 trip rows. A separate query groups the same seven days by weekday and reconciles to the same total. The monthly reports are summarized by year. I do not join these periods as one continuous trend.

## Stakeholder questions

- **When did recorded trips peak in the sample week?** At 18:00, with 334,713 records.
- **Which day had the most trips in the sample week?** Saturday, with 866,393 records. This is a seven-day descriptive slice.
- **What did annual averages hide?** Trips per day averaged 2.0% higher in 2025, while driver totals averaged 0.1% lower. Matched-month driver counts averaged 4.2% lower in January–June, then 4.0% higher in July–December.
- **Do these records prove that riders were underserved?** No. Requests, lost matches, cancellations, and true wait are missing.

## Findings

### Recorded trips peaked at 18:00 in the observed week

The bounded week contains **4,965,012 recorded trip rows**. Counts ranged from **59,285 at 04:00** to **334,713 at 18:00**.

![Official NYC TLC HVFHV data, 1–7 February 2019: recorded trips peaked at 334,713 at 18:00; trip records do not show unserved requests](/images/growth-hvf-hourly.png)

This makes early evening a reasonable time to inspect with internal request and wait data. It is not evidence that 18:00 had unmet demand.

### Saturday and Friday had the most recorded trips

Saturday had **866,393** records and Friday had **860,161** in the seven-day slice. Tuesday had the fewest, with **576,476**. The weekday pattern identifies when to inspect internal request and online-supply data. It does not show shortage or lost demand.

![NYC TLC HVFHV trip records by weekday, 1–7 February 2019: Saturday and Friday had the most records, while Tuesday had the fewest](/images/growth-hvf-weekday.png)

### Annual averages hide opposite first- and second-half driver patterns

In the monthly reports, average trips per day rose from **654,410 in 2024** to **667,537 in 2025** (**+2.0%**). Average unique drivers changed from **83,399** to **83,299** (**−0.1%**), while reported average hours per driver changed from **6.35** to **6.38** per day.

![TLC monthly High Volume FHV reports: average trips per day rose 2.0%, while unique-driver counts were nearly flat; reported driver hours rose 0.4%](/images/growth-hvf-monthly-supply.png)

The annual average hides a seasonal pattern. Compared with the same month in 2024, unique driver counts averaged **4.2% lower in January–June 2025**, then **4.0% higher in July–December**. Trips per day averaged **0.7% higher** in the first half and **3.3% higher** in the second half. These are 12 matched monthly pairs, not an inferential test or hourly supply measure.

![NYC TLC monthly reports: compared with the same 2024 month, 2025 driver counts were lower through June and higher from July; trips per day rose modestly in both halves](/images/growth-hvf-monthly-matched.png)

The month-matched comparison sharpens the retrospective picture but still cannot locate an hourly or zone-level shortage. The 2019 trip slice and 2024–2025 monthly reports describe different periods and must not be combined as one continuous trend.

### The public sources leave key parts of the funnel unknown

![NYC TLC marketplace evidence boundary: recorded trips and monthly driver proxies are observed; requests, lost matches, cancellations, true wait, and incentive return are not](/images/portfolio-marketplace-measurement.svg)

Without these missing measures, the data cannot distinguish low demand, low availability, and poor matching.

## Built

The project uses official TLC trip and monthly report data, SQL and Python analysis files, and five visuals. They separate observed historical patterns from missing marketplace measures.

## Result

The public data supports a time-of-day activity pattern and separate monthly supply proxies. It does not confirm a shortage or estimate incentive ROI.

**Recommendation:** do not raise incentives or choose target zones from these public counts. Instrument requests, matches, cancellations, wait, driver-online hours, incentives, and contribution at the same zone-time grain. If those contemporaneous measures show a repeated local shortage, run a powered zone-time or switchback test. Measure request fulfillment as the customer outcome, trips per online driver-hour as a supply diagnostic, and incremental fulfilled trips per incentive dollar as the economic measure. Monitor wait, cancellations, driver earnings, and neighboring-zone displacement.

For the next decision review, request a 28-day zone-by-15-minute baseline with request ID, request time, match result, pickup wait, driver online minutes, completed trip, and incentive cost. This gives the team a comparable current baseline; the historic public snapshots cannot substitute for it.

**Limitations:** the trip slice is from 2019 while the monthly comparison covers 2024–2025. Neither public source shows every request, lost match, or zone-hour online driver. No incentive pilot or marketplace outcome is measured here.

## Technical appendix

The hourly and weekday aggregations each reconcile to 4,965,012 rows for 1–7 February 2019. The 2024–2025 monthly report is summarized separately. The source queries and chart generation notes are in the [marketplace analysis files](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/projects/growth-analytics/02-marketplace-supply-demand).
