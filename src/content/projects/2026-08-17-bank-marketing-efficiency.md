---
title: "Bank Marketing: Which Contacts Deserve More Attention?"
date: 2026-08-17
categories: [marketing performance]
tags: [campaigns, customer segments, response rate, python]
excerpt: "A campaign review that compares contact channels, prior outcomes, and customer groups to support better targeting decisions."
problem: "The bank made many campaign contacts, but response varied sharply by channel, timing, and customer history."
result: "Among 45,211 contacts, 5,289 resulted in a positive outcome; cellular contacts responded at 14.9% versus 4.1% for records with an unknown contact type."
featured: false
---

## Business context

Marketing teams need to balance reach with customer attention and campaign cost. A high response rate can be useful, but only if the channel and audience can be reached efficiently and the offer remains commercially valuable.

## Business question

Which audiences and contact methods should the bank prioritize for future term-deposit campaigns?

## Approach

I validated the [UCI Bank Marketing dataset](https://archive.ics.uci.edu/dataset/222/bank%5C%5C%2Bmarketing), then compared campaign outcomes by contact type, month, job group, and previous campaign result. I used response rate as the main measure because the file does not include campaign cost, deposit value, or customer lifetime value.

## Key findings

### The campaign produced a minority response

There were **5,289 positive outcomes out of 45,211 contacts**, or **11.7%**. Most contacts did not convert, so broad outreach should be treated as a starting point for better targeting rather than a finished growth strategy.

### Contact channel was strongly associated with response

The response rate was **14.9% for cellular contacts**, **13.4% for telephone contacts**, and **4.1% where contact type was unknown**. The pattern supports improving contact data and testing channel mix. It does not prove that channel alone caused the difference.

### Previous success was the clearest audience signal

Customers whose previous campaign outcome was recorded as successful responded at **64.7%**, compared with **9.2%** for customers with an unknown previous outcome. This is a strong reason to treat campaign history as a priority signal, while avoiding repeated contact that may create fatigue.

## Recommendations

1. Prioritize customers with a documented positive prior outcome for a controlled follow-up test.
2. Improve contact-type completeness before comparing channel performance at scale.
3. Use response rate together with contact cost, deposit value, and complaints before reallocating budget.
4. Set a contact-frequency rule so high-propensity customers are not over-contacted.

## Takeaway

The bank’s strongest targeting signal was prior campaign success, supported by a clear difference between known and unknown contact channels. Better targeting and measurement can reduce low-value outreach without assuming every positive response is equally profitable.

## Supporting detail

The archive contains 45,211 rows and 17 fields with no missing or duplicate rows in the validated `bank-full.csv`. The data covers a Portuguese bank’s direct-marketing campaign from 2008–2010 and is licensed CC BY 4.0. It does not prove profitability or causal lift.
