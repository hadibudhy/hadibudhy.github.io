---
title: "NYC 311: Finding Queue Pressure Without Mislabeling Resolution"
date: 2026-09-06
categories: [analytics engineering]
tags: [data reliability, service operations, metric definitions, public data]
excerpt: "A mature-cohort analysis of 348,180 real service requests that separates arrivals, administrative closure tails, open cases, and resolution evidence."
problem: "An operations lead needs to decide which workflows need investigation, but request volume alone hides long-lived cases and administrative closure does not prove that the issue was resolved."
result: "Following January 2025 requests through a September 2026 snapshot found long administrative closure times in a small set of queues, including a 155-day P90 among valid closed Taxi complaints."
featured: true
kind: flagship
published: true
caseId: service-metric-reliability
primaryTrack: analytics-engineering
secondaryTracks: [product-analytics]
displayOrder: 25
evidenceManifest: /data/evidence/service-metric-reliability.json
evidenceVisuals:
  - /images/senior-311-pressure.png
  - /images/senior-311-volume-time.png
  - /images/portfolio-nyc311-boundary.svg
header:
  teaser: /images/senior-311-pressure.png
---

## The decision

An operations director needs to choose which service queue should receive a routing or capacity pilot. The decision must consider incoming work, open backlog, and long close times together. It must also avoid presenting administrative closure as proof of resident satisfaction.

## Data and cutoff

I downloaded **348,180 NYC 311 requests** created during January 2025 from the [official Open Data API](https://data.cityofnewyork.us/resource/erm2-nwe9) and used the recorded snapshot available on 5 September 2026. This creates a mature intake cohort: each January request has at least 19 months of follow-up.

The request identifier is unique in the snapshot. Creation time is complete. **2,609 requests** have no closure time and **97 records** have a closure before creation; those invalid durations remain counted in quality reporting and stay out of close-time statistics.

## Metric contract

| Metric | Definition | Boundary |
|---|---|---|
| Arrivals | Requests created during January | Reported demand, not total service need |
| Open backlog | No valid closure by the September 2026 snapshot | Administrative open state |
| Median close time | Median hours for valid closures by the snapshot | Typical completed lifecycle |
| P90 close time | 90th percentile hours among valid closed requests by the snapshot | Long-tail administrative delay, not eventual resolution time |
| Closure coverage | Valid closures / non-invalid requests | Whether the queue has enough mature outcomes for timing analysis |

![NYC 311 records contain lifecycle fields but not first response, staff effort, reopen history, or verified resolution](/images/portfolio-nyc311-boundary.svg)

## Analytics architecture

`API snapshot → request-grain staging → cutoff-safe queue mart → pressure comparison → capacity pilot`

The dbt mart never uses a closure after the recorded snapshot. It excludes negative durations from timing and open-backlog metrics, reports them as quality issues, requires at least 80% closure coverage for P90 comparison, and groups at agency × complaint type. P90 is explicitly a closed-request measure; open requests are right-censored and shown separately. Source and result hashes make the published snapshot reproducible.

## What I investigated

I tested whether the largest queues also had the longest mature administrative closure tail. The comparison includes agency–complaint groups with at least 500 arrivals and at least 80% valid closure coverage. It ranks by observed P90 closure time, then uses open cases as a separate monitoring signal.

## Volume and pressure point to different decisions

High request volume does not always mean a long closure tail. The comparison shows that some smaller queues have a much longer mature tail, while some larger queues close most recorded work sooner.

![NYC 311 requests created in January 2025: high arrival volume and closed-request closure time identify different workflow investigations](/images/senior-311-volume-time.png)

This matters because a volume-only staffing rule can send resources to the wrong queue.

## Long administrative closure tails are concentrated

Among mature queues with at least 500 arrivals and 80% closure coverage:

- **Building/Use:** 1,460 arrivals; 100% valid closure coverage; P90 administrative closure **330.6 days**.
- **Elevator:** 1,605 arrivals; 100% coverage; P90 **189.0 days**.
- **Taxi Complaint:** 584 arrivals; **96.6%** coverage; P90 **155.2 days**.
- **For Hire Vehicle Complaint:** 1,425 arrivals; **96.6%** coverage; P90 **139.6 days**.

![NYC 311 January 2025 intake cohort: selected queues have the longest closed-request administrative closure times](/images/senior-311-pressure.png)

These figures show lifecycle timing, not failure by an agency. Complaint type, legal workflow, severity, reporting channel, and closure rules are plausible explanations that need operational review.

## Recommendation

**P0: review workflow definitions before moving staff.** Confirm what “open” and “closed” mean for Building/Use, Elevator, Taxi Complaint, and For Hire Vehicle Complaint. Add first-response, transfer, reopen, effort, and resident-outcome events.

**P1: test capacity only after workflow review.** Select one queue where the bottleneck is operationally controllable. Randomize routing or staffing by eligible queue-time blocks. Use age-adjusted backlog clearance and time to first response as primary metrics.

**Guardrails:** reopen or repeat-contact rate, transfer rate, issue-resolution confirmation, cost per completed request, and backlog displacement into neighbouring queues.

**P2: investigate access bias.** Compare request rates with population and service-inspection data before using geography to allocate service value.

## Success rule

The pilot succeeds only if it reduces age-adjusted backlog and first-response time without increasing reopen, transfer, repeat-contact, or cost beyond agreed limits. A faster closure timestamp alone is not success.

## Limitations

- The source captures reported requests, not all resident need.
- Administrative closure does not establish resolution.
- The intake month is fixed, but closure workflows may still vary by season and policy.
- Closed-request P90 does not estimate eventual full-cohort resolution time because open cases are right-censored.
- Long administrative closure time does not identify the bottleneck or staff performance.

## Key takeaway

The senior decision is to follow a mature intake cohort, find long administrative closure tails with adequate coverage, verify the workflow, then test capacity only where the bottleneck is controllable.

## Technical appendix

The repository includes the fixed-cutoff loader, staging model, queue mart, negative-duration test, CI fixture, evidence builder, and aggregate result at `/data/senior/service-queues.json`.
