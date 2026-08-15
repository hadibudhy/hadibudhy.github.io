---
title: "Workforce Planning: Reading Openings, Hires, and Quits Together"
date: 2026-08-21
categories: [workforce analytics]
tags: [workforce planning, hiring, retention, BLS]
excerpt: "A workforce planning view that separates employer demand for workers from completed hiring and employee separations."
problem: "Hiring pressure is easy to misread when job openings, hires, and quits are shown separately or treated as the same signal."
result: "The BLS JOLTS API provides a consistent monthly view of openings, hires, quits, and separations, supporting workforce planning without pretending that aggregate data explains individual employee behavior."
featured: false
---

## Business context

Leaders need to know whether staffing pressure comes from growth, difficulty hiring, or employees leaving. The response is different in each case: recruiting capacity, workforce design, pay review, or retention work.

## Business question

What does the relationship between openings, hires, and quits suggest about workforce pressure, and what should management investigate next?

## Approach

I used the [BLS Job Openings and Labor Turnover Survey](https://www.bls.gov/jlt/) and its public API. I compared monthly openings, hires, quits, and total separations over time. The data is an aggregate labor-market indicator; it is not an employee-level explanation of turnover.

## Key findings

### Openings are demand, not completed hiring

An open role shows that an employer is seeking workers. A hire shows that a person joined during the period. Comparing the two helps distinguish persistent hiring pressure from a period when recruiting successfully converted demand into staffing.

### Quits and total separations answer different questions

Quits are employee-initiated separations, while total separations also include layoffs, discharges, and other exits. A rise in total separations should not automatically be described as voluntary turnover.

### Aggregate trends need company evidence

JOLTS can provide external context for a workforce plan, but it cannot identify which team, manager, pay band, or role is driving a company’s retention problem. Internal headcount, time-to-fill, tenure, and exit data are needed for action.

## Recommendations

1. Track openings, hires, quits, and total separations on one workforce scorecard.
2. Compare internal hiring and exit trends with the external labor-market context.
3. Investigate role, location, tenure, and manager patterns before launching broad retention programs.
4. Use time-to-fill and vacancy age to separate recruiting capacity issues from demand growth.

## Takeaway

Workforce decisions improve when leaders separate demand for workers from actual hiring and employee-initiated exits. JOLTS gives the context; internal people data must explain the local problem.

## Supporting detail

The BLS publishes JOLTS monthly indicators through a public API. The series are estimates and may be revised. They should support planning and benchmarking, not individual employment decisions.
