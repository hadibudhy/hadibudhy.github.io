---
title: "Commercial Electricity: Where Should a Multi-Site Business Review Cost Risk?"
date: 2026-10-12
categories: [business analytics, operations]
tags: [energy, cost-analysis, electricity, EIA]
excerpt: "A state-level price review finds where commercial electricity costs rose fastest, while setting clear limits on what public averages can say about a company's bills."
problem: "A national energy budget can hide state-level price differences, leaving multi-site operators unsure where a closer cost review may matter most."
result: "EIA's nominal U.S. commercial price rose 25.6% from 2019 to 2025, with wide variation across states. The public averages do not estimate a company's bill or the savings from an efficiency project."
featured: false
published: true
caseId: commercial-electricity-costs
kind: completed
primaryTrack: product-analytics
displayOrder: 100
evidenceManifest: /data/evidence/commercial-electricity-costs.json
evidenceVisuals:
  - /images/commercial-electricity-price-trend.png
  - /images/commercial-electricity-state-priorities.png
  - /images/commercial-electricity-top-state-rates.png
header:
  teaser: /images/commercial-electricity-price-trend.png
---

## Project brief

- **Project:** Screen commercial electricity price levels and changes across states.
- **Question:** Where should a multi-site business review energy cost exposure first?
- **Built:** A sales-weighted EIA price series and state comparison from 2019 to 2025.
- **Result:** The U.S. average rose 25.6% in nominal terms. State prices and changes varied. Public averages do not estimate company bills or savings.

## Business question

A finance team may set one electricity cost assumption for every location. That can miss markets where prices are already high or where the published average has risen quickly. The business question is: **which locations should a multi-site operator review first, and what can public data support before a site-level audit?**

The analysis is a market screen. It does not estimate a particular company's energy bill, operating margin, or savings opportunity.

## Data and preparation

The source is the U.S. Energy Information Administration's monthly Form EIA-861M electricity sales and revenue data. The checked snapshot covers January 2019 through December 2025. Each row is a state, month, and sector. I kept the commercial sector, analyzed the 50 states and District of Columbia separately, and used the EIA U.S. aggregate for the national trend. Regional aggregates were excluded from the state comparisons. EIA makes state-level adjustments for non-sampled entities; the monthly figures cover bundled service.

For each year, I calculated the sales-weighted price as 100 times total commercial revenue divided by total commercial sales. The published units convert to cents per kilowatt-hour. Prices are nominal and are not adjusted for general inflation.

## Stakeholder questions

- **How did the U.S. commercial average change?** It rose from 10.68 cents per kilowatt-hour in 2019 to 13.41 cents in 2025.
- **Which states had both high prices and fast growth?** The state chart marks states above the 75th percentile on both measures.
- **Can a state average estimate one company's bill?** No. Site tariffs, load, contracts, and demand charges are missing.

## Findings

### The national commercial average price rose, but it is not a company bill

The U.S. aggregate increased by 25.6% between 2019 and 2025. The average retail price dipped slightly in 2020, then rose each year from 2021 through 2025.

![U.S. commercial electricity price rose from 10.68 cents per kilowatt-hour in 2019 to 13.41 cents in 2025](/images/commercial-electricity-price-trend.png)

This supports updating the national planning baseline. It does not show how a specific business's bill changed because the EIA value is an average across commercial customers and utility arrangements.

### Price levels and growth differ across states

Hawaii had the highest 2025 state average at **36.4 cents per kilowatt-hour**, followed by California at **26.4 cents**. Across states, the median nominal price increase was **21.7%**. The District of Columbia, Maine, and California had increases of **66.5%**, **63.4%**, and **58.1%**, respectively. The chart highlights markets above the 75th percentile on both price and growth; dashed lines show state medians.

![State comparison of 2025 commercial electricity price and nominal price growth from 2019 to 2025, with states in the top quartile for both measures highlighted](/images/commercial-electricity-state-priorities.png)

This comparison helps identify markets for a closer review. It does not show that an operator in a highlighted state can negotiate a lower price or save a particular amount.

### The highest-price markets do not share one cost pattern

Hawaii and California led the 2025 state averages, but their changes since 2019 were different. The comparison keeps the earlier level visible so a team does not confuse a high current price with the fastest increase.

![Ten highest state and District of Columbia commercial electricity prices in 2025, compared with their 2019 prices](/images/commercial-electricity-top-state-rates.png)

The distinction matters for planning: a high level may call for a tariff and load review, while a fast increase may call for a budget and contract review. Neither signal replaces actual bills.

## Built

The analysis calculates annual sales-weighted prices and compares 51 state and District of Columbia series. It excludes regional and national rows from state comparisons and retains the nominal-price boundary.

## Result

The evidence supports the first two hypotheses: the national commercial average retail price rose, and both 2025 price levels and 2019 to 2025 changes vary by state. The third hypothesis is not supported. A state average is not detailed enough to choose a procurement or efficiency investment.

- Start a bill and tariff review in sites with high prices, steep increases, or both.
- Compare each location's time-of-use rate, demand charges, contract terms, load profile, and operating schedule.
- Evaluate efficiency work using site-specific baseline consumption and costs, adjusted for weather, occupancy, and production.
- Track realized cost per kilowatt-hour and peak demand after a pilot. The EIA analysis does not measure savings.

## Technical notes

The analysis uses 5,208 monthly EIA records, including state, District of Columbia, U.S. aggregate, and regional rows. The state comparison contains 51 complete series with 84 months each. Annual weighted prices use EIA revenue and sales totals; the analysis does not use a simple average of monthly prices. Data, source hashes, and the regeneration command are documented in [`docs/new-public-data-case-notes.md`](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/new-public-data-case-notes.md).

The source is [EIA Form EIA-861M](https://www.eia.gov/electricity/data/eia861m/index.php). EIA derives its average retail price from utility revenue and sales. Utility revenue can include energy, demand, delivery, tax, and other charges, but the average is not a utility tariff and does not separate those components for a specific site. EIA does not publish utility tariffs or itemized demand charges. See [EIA's price definition](https://www.eia.gov/tools/faqs/faq.php?id=507&t=5) and [rate and tariff data boundary](https://www.eia.gov/tools/faqs/faq.php?id=20&t=6). The analysis does not establish the effect of any policy or energy-efficiency change.
