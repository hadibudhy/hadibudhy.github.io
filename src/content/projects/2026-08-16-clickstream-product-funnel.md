---
title: "Online Shopping Clickstream: Finding the Pages Where Intent Weakens"
date: 2026-08-16
categories: [product analytics]
tags: [funnel analysis, user behavior, conversion, python]
excerpt: "A session-level review of online shopping behavior showing how much browsing happens after the first page and where a product team should focus journey improvements."
problem: "The store could see page activity, but it was not clear how far shoppers moved through the journey or where attention weakened."
result: "The file contains 24,026 sessions and 165,474 events; 79.0% of sessions visited more than one page, giving the product team a clear base for funnel testing."
featured: false
---

## Business context

An online store can receive a lot of traffic without creating a strong shopping experience. Page visits show interest, but they do not explain whether visitors can move from browsing to a useful product view and then toward a purchase decision.

## Business question

Where does the shopping journey lose momentum, and which parts of the experience deserve the first product tests?

## Approach

I used the [UCI Clickstream Data for Online Shopping](https://archive.ics.uci.edu/dataset/553/clickstream%2Bdata%2Bfor%2Bonline%2Bshopping). I grouped 165,474 events into 24,026 sessions and compared session depth, page stages, countries, and product-page activity. The source records browsing events and product prices, but it does not provide a confirmed order or revenue field.

## Key findings

### Most sessions moved beyond the first page

The median session contained four events, and **79.0% of sessions had more than one event**. This means the main opportunity is not only attracting visitors. It is helping active visitors continue with less friction.

### Interest narrowed as shoppers moved deeper

There were **93,452 first-stage page events**, followed by **41,037**, **19,301**, **8,861**, and **2,823** events across the later stages. The volume falls at each stage, so the next step should be to compare the content and navigation around each transition rather than treat every page view as equal.

### The data supports a journey test, not a revenue claim

The dataset contains 195 order identifiers, but the file description does not establish that the identifier is a completed purchase measure. I therefore use it to understand browsing behavior, not to claim a conversion rate or revenue lift.

## Recommendations

1. Measure the share of sessions reaching each page stage and product model, with a clear definition of “completed purchase.”
2. Test simpler navigation and stronger next-step prompts after the first product interaction.
3. Compare the journey by country and category before changing the whole site.
4. Add reliable checkout and revenue events to future tracking so product changes can be tied to business results.

## Takeaway

The store already had meaningful multi-page engagement. The next product decision should focus on helping those interested visitors move through the journey, while improving event tracking so future tests can measure commercial impact.

## Supporting detail

The archive contains five months of 2008 clickstream data, 14 fields, and no missing values in the downloaded CSV. Prices describe product-page observations; they are not proof of sales. The source is licensed CC BY 4.0.
