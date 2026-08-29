---
title: "Workforce Planning: Separating Hiring Pressure From Turnover"
date: 2026-08-21
categories: [workforce analytics]
tags: [workforce planning, hiring, retention, BLS]
excerpt: "A workforce decision framework that distinguishes open roles, completed hiring, voluntary quits, and total separations."
problem: "Leaders can misread staffing pressure when openings, hires, and exits are treated as one workforce signal."
result: "In the BLS December 2025 aggregate series, openings were 6.55 million, hires were 3.3%, quits were 2.0%, and total separations were 5.203 million."
featured: false
header:
  teaser: /images/jolts-december-signals.png
---

## Executive summary

**Business problem:** determine whether workforce pressure comes from growth, hiring friction, or employees leaving.

**Key findings:** open roles are demand rather than completed hiring; quits are different from total separations; and the December 2025 U.S. aggregate shows 6.55m openings alongside 5.203m total separations.

**Decision implication:** the same headline “staffing problem” can require recruiting, retention, workforce-design, or cost action.

**Recommended action:** use JOLTS as external context and connect it to internal vacancy age, time-to-fill, tenure, and exit data.

## Business question

**Decision owner:** Chief People Officer. **Decision:** where should workforce investment go first? **North-star KPI:** critical-role coverage. **Drivers:** openings, hires, time-to-fill, quits, separations, tenure, and productivity. **Guardrails:** labor cost, overtime, quality, burnout, and regretted attrition.

## Why it matters

Hiring pressure and turnover require different actions. Hiring more people will not solve a retention problem, and retention programs will not fill roles that are hard to recruit.

## Data used

The BLS API returned December 2025 values of **6.55m openings**, **3.3% hires**, **2.0% quits**, and **5.203m total separations**. Openings measure employer demand; hires measure people starting; quits measure employee-initiated exits; total separations include other exit types.

The data cannot identify a company, team, manager, or role causing turnover. It is also an aggregate estimate that can be revised. Any internal diagnosis must preserve that distinction.

![U.S. BLS JOLTS, December 2025: Openings are a point-in-time stock, separations are a monthly flow, and hires and quits are rates](/images/jolts-december-signals.png)

## Approach

The conservative scenario is to improve vacancy visibility and recruiting throughput in critical roles. The expected scenario combines that with targeted retention work where internal quits exceed the external benchmark. The ambitious scenario redesigns roles or staffing models. Faster hiring can improve coverage but increase cost or reduce selection quality; retention programs can add cost without reducing regretted exits.

## Key findings

- December 2025 openings were **6.55 million**; this is a point-in-time stock, not completed hiring.
- Hires (**3.3%**) and quits (**2.0%**) are rates, while total separations were **5.203 million** in the month.
- The aggregate series provides labor-market context, not a diagnosis of a company, team, or role.

## Recommendation

- **P0 — Act now:** build one scorecard for openings, hires, time-to-fill, quits, and regretted exits.
- **P1 — Test:** pilot a retention or recruiting intervention in one role family with a comparable control group.
- **P2 — Investigate:** join internal HR data to pay, tenure, manager, location, and workload measures.

Primary metric is critical-role coverage; guardrails are quality, overtime, labor cost, employee experience, and regretted attrition. Repeat with revised BLS data and alternative time windows.

## Key takeaway

JOLTS does not explain a company’s people problem. It improves the decision by separating labor-market context from internal root causes, so management can act on the drivers it can control.

## What internal data would improve the decision

Role, location, vacancy age, applicant flow, time-to-fill, pay, tenure, manager, workload, overtime, performance, and regretted-exit data would identify the teams that need recruiting, retention, or redesign.

## Technical appendix

Source: [BLS JOLTS](https://www.bls.gov/jlt/). The series is an aggregate U.S. labor-market indicator and should not be used for individual employment decisions.
