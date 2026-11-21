# College Scorecard case reproduction

This page documents the source snapshot and checks for the published College Scorecard case. Raw input is stored locally under the Git-ignored `analysis_data/raw/` directory.

Run the College-only path from the repository root:

```powershell
python scripts/generate_commercial_energy_and_college_outcomes.py --case college
```

The script downloads the public source ZIP when it is missing, verifies its SHA-256, and rebuilds the three charts and evidence manifest. It stops if the source hash differs from the pinned snapshot.

| Official source | Local snapshot | SHA-256 |
|---|---|---|
| [College Scorecard field-of-study data](https://collegescorecard.ed.gov/data/) | `Most-Recent-Cohorts-Field-of-Study_06102026.zip` | `9c4339d65f0699a60d6078fe54fc3bf03fded30a65079222d9221952b8578165` |

The June 10, 2026 ZIP contains 227,980 program rows. Outcome records are deduplicated at OPEID6, four-digit CIP field, and credential level because institution-system outcomes repeat across branch campuses. The script checks that repeated branch rows agree on earnings and debt before retaining one record.

The published earnings coverage uses numeric `EARN_MDN_4YR` values. Privacy-suppressed and unavailable cells remain non-reportable. The analysis does not impute missing values or rank institutions by the subset that is visible. The manifest records the source hash, row counts, validation checks, chart paths, and chart hashes.
