---
title: "Bank Marketing: Targeting Response Without Confusing It With Profit"
date: 2026-08-17
categories: [marketing performance]
tags: [campaigns, customer segments, response rate, experimentation]
excerpt: "A campaign decision study that identifies the strongest response signals, quantifies the addressable audience, and defines the missing economics needed for budget allocation."
problem: "The bank made 45,211 contacts, but broad response rates hid the difference between audience quality, channel coverage, and prior campaign history."
result: "The overall positive-response rate is 11.7%; cellular contacts respond at 14.9%, unknown contact types at 4.1%, and previously successful contacts at 64.7%."
featured: false
header:
  teaser: /images/bank-channel-response.png
---

## Executive summary

**Business problem:** reduce low-value outreach while protecting response.

**Evidence strength:** Medium for historical response segmentation; low for channel causality and profit because cost and deposit value are missing.

**Key findings:** 5,289 of 45,211 contacts were positive; the unknown-contact group contains 13,020 contacts and trails cellular response; prior success is the strongest observed signal; and the dataset lacks contact cost and deposit value.

**Decision implication:** improving data coverage could address a large contact pool, but response uplift is not yet a profit case.

**Recommended action:** run a controlled targeting test and add cost/value fields before reallocating budget.

## Business question

**Decision owner:** Head of Marketing. **Decision:** which audiences and channels should receive incremental campaign capacity? **North-star KPI:** incremental contribution per contact. **Drivers:** response rate, contact cost, deposit value, and repeat response. **Guardrails:** complaint rate, contact frequency, and customer fatigue.

## My role

I owned the response segmentation, data-quality review, scenario calculation, and controlled-targeting recommendation for this independent portfolio case. I did not run the bank campaign or observe incremental contribution.

## Why it matters

More outreach is not automatically better. A high response rate can still destroy value if the contact is expensive or the product contribution is low.

## Data used

The validated archive has **45,211 rows, 17 fields, no missing values, and no duplicates**. Positive outcomes are 11.7% overall. Cellular response is 14.9%, telephone 13.4%, and unknown contact type 4.1%. Previous successful outcomes respond at 64.7%, while unknown previous outcomes respond at 9.2%.

The channel pattern is associated evidence, not causality. Channel may proxy for data quality or customer selection. The dataset also lacks profit, so optimizing response alone could increase cost without improving value.

![Bank Marketing campaign archive, 45,211 contacts: Positive response was 14.9% for cellular, 13.4% for telephone, and 4.1% for unknown contact type](/images/bank-channel-response.png)

![Bank Marketing campaign archive, 45,211 contacts: Previous campaign success had a 64.7% positive response versus 9.2% for unknown prior outcomes](/images/bank-prior-outcome-response.png)

## Approach

If the **13,020 unknown-contact records** reached the observed cellular rate, the arithmetic upside would be about **1,410 additional positive outcomes**. This is a scenario, not a forecast: it assumes the group is reachable and comparable. The trade-off is that more contact may increase complaints or cost.

## Key findings

- Positive response is **11.7% overall**, **14.9% for cellular**, and **4.1% for unknown contact type**.
- Previous campaign success is a strong observed signal: **64.7%** positive response versus **9.2%** for unknown prior outcomes.
- These are associations in a historical archive; they do not establish channel lift or profit.

## Recommendation

- **P0 — Act now:** repair contact-type completeness and add contact cost, deposit value, and complaint fields.
- **P1 — Test:** randomize a targeted follow-up among customers with prior success; compare incremental contribution, not raw response.
- **P2 — Investigate:** test whether the channel gap remains after controlling for customer history and month.

Treatment is a targeted offer; control is the current campaign; primary metric is contribution per contacted customer; guardrails are complaints, opt-outs, and contact frequency. Repeat using alternative definitions of “prior success” and exclude months with unusual campaign mix.

## Key takeaway

The bank has a clear targeting signal, but senior budget judgment requires economics. Response rate should open the investigation; incremental contribution should close it.

## What internal data would improve the decision

Contact cost, deposit value, margin, complaints, opt-outs, customer history, and campaign assignment would show whether the observed response differences create profitable incremental value.

## Technical appendix

Source: [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank%5C%5C%2Bmarketing), CC BY 4.0. The data covers a Portuguese bank’s direct-marketing campaign from 2008–2010 and does not prove causal channel lift or profitability.
