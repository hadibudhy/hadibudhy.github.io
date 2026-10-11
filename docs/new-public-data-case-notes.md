# New public-data case studies

The energy and College Scorecard articles use official public data. Raw snapshots are stored locally under `analysis_data/raw/`, which Git ignores. Run the generator from the repository root to download a missing source snapshot, verify its SHA-256, and rebuild all six charts and evidence manifests:

```powershell
python scripts/generate_commercial_energy_and_college_outcomes.py
```

Set `EIA_API_KEY` to an EIA key if the public `DEMO_KEY` limit is reached. The generator pages through the EIA response and saves one normalized snapshot. It downloads the College Scorecard field-of-study ZIP from the official public download host when the file is missing.

| Case | Official source | Local snapshot | SHA-256 |
|---|---|---|---|
| Commercial electricity costs | [EIA Form EIA-861M](https://www.eia.gov/electricity/data/eia861m/index.php) | `eia_commercial_electricity_2019_2025_full.json` | `a4214c6405861c1fee3f7eaa074c14354374a8d64ce4e5a415c52a59f4c356f0` |
| College program outcome coverage | [College Scorecard data](https://collegescorecard.ed.gov/data/) | `Most-Recent-Cohorts-Field-of-Study_06102026.zip` | `9c4339d65f0699a60d6078fe54fc3bf03fded30a65079222d9221952b8578165` |

## EIA snapshot

The EIA request selects monthly sales, revenue, customer counts, and price for the commercial sector from January 2019 through December 2025. It returned 5,208 records across 84 months. The data contains 51 state and District of Columbia series, the U.S. aggregate, and regional aggregates. The state analysis uses only the 51 state and District of Columbia codes. The national annual average retail price is recomputed as 100 times annual revenue divided by annual sales; all prices are nominal. EIA says utility revenue can include energy, demand, delivery, tax, and other charges, while its average retail price is not an individual utility tariff. See [EIA's average price definition](https://www.eia.gov/tools/faqs/faq.php?id=507&t=5) and [rate and tariff data boundary](https://www.eia.gov/tools/faqs/faq.php?id=20&t=6).

The EIA source is mutable. If the service replaces historical values, the script reports a hash mismatch and stops. Recheck the figures and update the snapshot hash only after reviewing the changed source.

## College Scorecard snapshot

The June 10, 2026 ZIP contains 227,980 program rows. Outcome rows are deduplicated using OPEID6, CIP field, and credential because Scorecard reports those values at the institution-system level and repeats them across branch campuses. The script verifies that repeated branch rows agree on the earnings and debt values before counting one program record.

The reported earnings share uses numeric `EARN_MDN_4YR` values. Privacy-suppressed and unavailable cells remain non-reportable. The published analysis does not impute these values or rank institutions by the subset that is visible.
