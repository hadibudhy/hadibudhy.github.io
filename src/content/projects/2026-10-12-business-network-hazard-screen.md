---
title: "Multi-Site Operations: Prioritize Continuity Planning by Hazard and Footprint"
date: 2026-10-12
categories: [business decision analytics, operations]
tags: [business continuity, FEMA, Census, location risk, resilience]
excerpt: "A county-level FEMA and Census screen finds where large retail, food-service, and manufacturing footprints overlap with higher relative hazard risk."
problem: "Operations leaders need a repeatable way to identify business-dense counties for continuity review without mistaking community hazard scores for site-level loss forecasts."
result: "FEMA High or Very High counties contained 46.2% to 52.4% of tracked sector establishments; hazard-specific shares differed sharply, led by inland flooding."
featured: false
published: true
kind: completed
primaryTrack: product-analytics
displayOrder: 130
caseId: business-network-hazard-screen
evidenceManifest: /data/evidence/business-network-hazard-screen.json
evidenceVisuals:
  - /images/business-risk-rating-establishment-share.png
  - /images/business-risk-hazard-exposure.png
  - /images/business-risk-priority-counties.png
header:
  teaser: /images/business-risk-rating-establishment-share.png
---

## Business question

Which U.S. counties should multi-site operators investigate first when a large local business footprint overlaps with higher natural-hazard risk?

## Why it matters

A continuity team may need to choose where to test alternate suppliers, backup power, staffing, and recovery plans. County-level evidence can narrow the review list, but it cannot identify the exposure of an individual facility.

## Decision brief

- **Recommendation:** use FEMA county ratings to create a continuity review queue, then geocode actual sites and evaluate hazard-specific exposure before changing investments or operating plans.
- **Evidence:** 179 high or very-high composite-risk counties contained 48.4% of the tracked retail establishments, 52.4% of accommodation and food-service establishments, and 46.2% of manufacturing establishments.
- **Evidence strength:** Moderate for identifying counties where business activity and FEMA's relative community risk ratings overlap; low for estimating company losses or disruption duration.
- **Main risk:** County Business Patterns counts industry establishments, not a named chain's locations. FEMA's county score is a relative community measure, not a site-level risk estimate.
- **Next test:** join exact facility coordinates to hazard layers, insurance terms, supplier links, and business-continuity dependencies.

## Data used

The Census Bureau's [2023 County Business Patterns](https://www.census.gov/data/datasets/2023/econ/cbp/2023-cbp.html) provides establishment counts by county and industry. I grouped retail trade from NAICS 44 and 45, accommodation and food services from NAICS 72, and manufacturing from NAICS 31, 32, and 33.

I joined these counts to FEMA's [National Risk Index county layer](https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/National_Risk_Index_Counties/FeatureServer/0), version 1.20, released in December 2025. FEMA provides composite ratings and hazard-specific ratings, including hurricanes, inland flooding, and wildfire. The two sources describe different periods: 2023 business counts and 2025 risk data.

## Analysis

### Composite high-risk counties contain a large share of establishments

FEMA's High and Very High composite risk classes covered 179 counties with matching business counts. These counties held **504,642 of 1,043,104 retail establishments (48.4%)**, **410,822 of 784,735 accommodation and food-service establishments (52.4%)**, and **131,363 of 284,156 manufacturing establishments (46.2%)**.

The overlap is substantial, but it is not a risk rate per business. Large counties tend to contain more establishments and more exposed assets. A high county score and a large business footprint therefore flag review priority, not the loss expected at each establishment.

![Share of retail, accommodation and food-service, and manufacturing establishments by FEMA composite risk rating](/images/business-risk-rating-establishment-share.png)

### Hazard-specific screens produce different priorities

Among establishments in counties with an applicable FEMA hazard rating, the share in high or very-high inland-flood counties was **53.1% for retail**, **57.4% for accommodation and food services**, and **51.8% for manufacturing**. The corresponding hurricane shares were **27.1%**, **27.3%**, and **20.7%**. Wildfire shares ranged from **12.6% to 14.5%**.

Hurricane ratings covered 73.3% to 77.1% of sector establishments. Inland-flood and wildfire ratings covered more than 99.9%. I excluded unrated and not-applicable counties from each hazard denominator. These comparisons show why one composite score should not replace hazard-specific review.

![Share of establishments in high or very-high counties by FEMA composite, hurricane, inland flood, and wildfire ratings](/images/business-risk-hazard-exposure.png)

### County priorities depend on both operating footprint and risk class

Los Angeles County had 28,998 retail establishments, 25,110 accommodation and food-service establishments, and 10,122 manufacturing establishments. It also had the maximum FEMA composite risk score of 100. Other large county-sector footprints in high or very-high counties included Harris County, Texas; Cook County, Illinois; and Maricopa County, Arizona.

These places are candidates for detailed continuity reviews, not automatic relocation decisions. A national ranking can obscure facility-level variation within each county.

![Largest retail, accommodation and food-service, and manufacturing footprints in counties with high or very-high FEMA composite risk](/images/business-risk-priority-counties.png)

## Result - use the screen to queue facility reviews

The evidence supports prioritizing county-level continuity reviews, with inland flooding first in this broad sector screen. The result does not estimate a particular operator's expected loss, insurance premium, downtime, or mitigation return.

For a real network, the decision should use exact facility locations and operating dependencies. Review sites against hazard-specific maps, supplier concentration, transport access, backup capacity, and recovery plans. Test scenarios before reallocating sites or capital.

## Technical notes

I aggregated non-overlapping Census industry group codes to county totals. I removed records with an unknown county FIPS code, then validated a one-to-one county join against the FEMA layer. The analysis reports both FEMA's High or Very High categories and a sensitivity screen using the upper quartile of the composite score within each sector's matched counties. The latter contains 75.8% to 82.1% of sector establishments, showing that a planning queue changes with the selected cutoff.

Hazard-specific establishment shares use counties with applicable ratings as denominators. The source labels No Rating, Not Applicable, and Insufficient Data separately. I do not treat those categories as low hazard.

The FEMA [National Risk Index technical documentation](https://www.fema.gov/sites/default/files/documents/fema_national-risk-index_technical-documentation.pdf) describes the county risk methodology. The local source snapshots, hashes, validation checks, and regeneration command are recorded in the [evidence manifest](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/public/data/evidence/business-network-hazard-screen.json). The manifest identifies the public source version used.
