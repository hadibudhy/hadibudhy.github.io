# Dataset research for the next portfolio projects

Research date: 2026-08-15

## Candidate scorecard

Scores are from 1 to 10. The total is a guide, not the only selection rule. The final set was chosen for coverage across customer growth, operations, and commercial quality.

| Candidate | Business relevance | Story potential | Data richness | Analysis depth | Recommendation potential | Portfolio uniqueness | Recruiter readability | Data quality challenge | Visualization potential | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| NYC TLC Yellow Taxi Trip Records | 9 | 9 | 10 | 8 | 9 | 8 | 8 | 8 | 10 | 79 |
| UCI Online Retail | 9 | 9 | 9 | 8 | 9 | 7 | 9 | 9 | 9 | 78 |
| NYC Restaurant Inspection Results | 8 | 8 | 9 | 8 | 8 | 8 | 8 | 10 | 8 | 75 |
| CFPB Consumer Complaint Database | 10 | 9 | 10 | 8 | 9 | 8 | 9 | 8 | 9 | 80 |
| U.S. Airline On-Time Performance | 9 | 8 | 9 | 8 | 8 | 7 | 8 | 7 | 9 | 73 |
| NYC 311 Service Requests | 9 | 8 | 9 | 8 | 8 | 7 | 9 | 8 | 9 | 75 |
| Census County Business Patterns | 8 | 7 | 9 | 8 | 8 | 8 | 8 | 7 | 8 | 71 |
| UCI Online Retail II | 9 | 8 | 10 | 9 | 9 | 5 | 8 | 8 | 9 | 75 |
| UCI Clickstream Data for Online Shopping | 8 | 7 | 7 | 6 | 7 | 7 | 8 | 7 | 8 | 65 |
| NYC Motor Vehicle Collisions | 8 | 8 | 8 | 8 | 8 | 7 | 8 | 9 | 9 | 73 |

## Selected set

The final three are deliberately complementary:

1. **UCI Online Retail** demonstrates customer value, repeat purchasing, market concentration, and data cleaning.
2. **NYC TLC Yellow Taxi Trip Records** demonstrates large-scale operational analysis, time patterns, geography, and unit economics.
3. **NYC Restaurant Inspection Results** demonstrates messy administrative data, inspection-level rollups, risk prioritization, and careful interpretation of incomplete outcomes.

The CFPB complaint database scored highly, but it was not selected because its customer-experience story overlaps with the retail project and the full download is very large. It remains a strong future project.

## Sources and usage notes

- [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online%2Bretail) is a UK online retail transaction dataset with 541,909 records and a CC BY 4.0 license.
- [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) is published monthly in Parquet format. The TLC warns that records come from vendor submissions and may contain accuracy or completeness issues.
- [NYC Restaurant Inspection Results](https://data.cityofnewyork.us/d/43nn-pn8j) is public NYC Open Data. The catalog says no explicit license information is provided and warns that the administrative source can contain illogical values from data-entry or transfer errors.
- [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) is freely available for analysis, but the CFPB warns that complaints are not a representative sample of all consumer experiences.
- [NYC 311 Service Requests](https://catalog.data.gov/dataset/311-service-requests-from-2010-to-present), [U.S. Airline On-Time Performance](https://catalog.data.gov/dataset/u-s-marketing-air-carriers-on-time-performance), [Census County Business Patterns](https://catalog.data.gov/dataset/economic-surveys-business-patterns-county-business-patterns-95872), [UCI Online Retail II](https://archive-beta.ics.uci.edu/dataset/502/online%2Bretail%2Bii), [UCI Clickstream Data for Online Shopping](https://archive.ics.uci.edu/dataset/553/clickstream%2Bdata%2Bfor%2Bonline%2Bshopping), and [NYC Motor Vehicle Collisions](https://data.cityofnewyork.us/) were also reviewed as alternatives.

## Validation notes

### UCI Online Retail

- 541,909 raw rows and 8 columns.
- Coverage: 2010-12-01 08:26 through 2011-12-09 12:50.
- 135,080 missing `CustomerID` values and 1,454 missing descriptions.
- 10,677 duplicate transaction keys using invoice, stock code, customer, and timestamp.
- 9,288 cancellation rows, 10,624 negative-quantity rows, and 2 negative-price rows.
- Clean analysis kept positive-quantity, positive-price, non-cancelled rows with a customer ID.

### NYC TLC Yellow Taxi, January 2025

- 3,475,226 raw rows and 20 columns.
- Pickup timestamps span 2024-12-31 20:47:55 through 2025-02-01 00:00:44; analysis restricted pickups to January 2025.
- 540,149 rows have missing values in several optional fields such as passenger count, rate code, and surcharge fields.
- 90,893 rows have non-positive trip distance and 145,516 have non-positive fare amounts.
- Clean analysis kept January pickups with positive distance and total amount and a duration between 1 and 120 minutes, leaving 3,312,701 trips.

### NYC Restaurant Inspection Results

- 295,256 raw violation records and 27 columns in the current public extract.
- Dates include placeholder values such as 1900-01-01 and current records through 2026-08-12.
- 160,467 grade dates, 150,141 grades, and 17,159 scores are missing.
- The dataset repeats restaurant and inspection details when one inspection has multiple violations.
- The case study restricts the analysis to 2022-2025 and rolls violation rows up to restaurant, inspection date, and inspection type, producing 73,478 inspection records.
