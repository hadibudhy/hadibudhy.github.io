---
title: "Company Performance: Reading Growth and Profit Together"
date: 2026-08-19
categories: [financial performance]
tags: [financial analysis, revenue, profitability, SEC]
excerpt: "A public-filing analysis that keeps revenue growth, profit, and reporting context together so business performance is not reduced to one headline number."
problem: "Management and investors can see revenue growth while missing changes in profitability, reporting periods, or the quality of the comparison."
result: "SEC Company Facts provides structured reported measures by company, period, and filing, creating a repeatable base for comparing revenue and net income without predicting stock prices."
featured: false
---

## Business context

Business performance is not one number. Revenue growth can be attractive while profit falls, or profit can improve while the business is shrinking. A useful review needs both the result and the context around how it was reported.

## Business question

Is the company growing in a way that also improves reported profitability, and what should management investigate next?

## Approach

I used the [SEC Company Facts API](https://www.sec.gov/data-research/sec-api-documentation), which publishes structured facts from company filings. I compared reported revenue and net income by fiscal period, checked filing dates, and kept fiscal-year definitions visible. This is a reporting analysis, not a stock-price forecast.

## Key findings

### Revenue and profit must be read as a pair

The core view compares revenue, net income, and net margin. Revenue answers how much business was recorded; net income shows what remained after reported expenses. A strong recommendation requires the direction of both measures, not revenue growth alone.

### Filing periods are a data-quality issue

Companies use different fiscal year ends, and SEC facts may contain amended filings or multiple facts for similar tags. The comparison therefore keeps fiscal period, filing date, form, and accounting tag in the working table.

### Reported performance is a starting point for questions

The data can identify a change in growth or margin, but it cannot by itself explain whether the driver was price, volume, cost, acquisition, or accounting classification. Those drivers require management commentary and the underlying statements.

## Recommendations

1. Use revenue and net margin together in quarterly performance reviews.
2. Flag periods where revenue direction and profit direction diverge.
3. Validate unusual changes against the filing, notes, and management discussion.
4. Keep restatements and fiscal-year differences visible before comparing companies.

## Takeaway

Financial analysis is most useful when it turns a headline change into a management question. SEC data makes that comparison repeatable, but the filing context is essential before acting on it.

## Supporting detail

SEC Company Facts is built from public XBRL filing data. Values can differ across companies because of fiscal calendars, tags, restatements, and reporting choices. The case study does not claim causation or investment performance.
