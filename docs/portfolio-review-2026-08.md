# Portfolio evidence review

Review date: 2026-08-30

This internal record uses pass/fail evidence requirements. It does not assign a numeric quality score, imply external endorsement, or treat proposed work as measured impact.

## Positioning

**Data Analyst**

Growth, product, marketplace, operations, analytics engineering, and applied AI appear as analytical capabilities within that single profile.

## Publication gate

| Requirement | Status | Evidence |
|---|---|---|
| Focused public library | Pass | Seven completed analyses or implemented artifacts are public |
| Project-specific evidence | Pass | Every public page contains computed results or validated system behavior |
| Reproducibility | Pass | Sources, denominators, validation logic, and limitations are stated |
| Visual evidence | Pass | Every public page declares at least three validated evidence visuals |
| Decision boundary | Pass | Observation, inference, causality, and proposed action are distinguished |
| Artifact status | Pass | Completed, proposed, rejected, prototype, and unmeasured states are explicit |
| Role consistency | Pass | Public positioning uses Data Analyst; specialties are capabilities, not competing identities |

## Strongest evidence

- **Campaign Incrementality:** randomized benchmark analysis, absolute lift, uncertainty, holdout logic, and an economic stop rule.
- **Online Shoppers Activation:** exact session denominators, duplicate sensitivity, leakage control, and a bounded experiment recommendation.
- **MTA Comparator Audit:** rejects a causal interpretation when the pre-policy comparison is unstable.
- **Online Retail Customer Growth:** transaction cleaning, customer concentration, and market-research prioritization without claiming expansion proof.
- **Marketplace Supply and Demand:** separates recorded trips from unmet demand and blocks a citywide incentive decision without request and availability data.
- **Restaurant Quality:** changes the unit of analysis from violation rows to inspections and treats borough results as unadjusted triage signals.
- **ComplaintFlow:** validates an auditable system prototype while separating software contract tests from real-world model performance.

## Evidence still required for stronger claims

- Implemented stakeholder decisions and post-launch measurement.
- Authentic, privacy-reviewed ComplaintFlow labels.
- Current unit economics for campaign, retention, and marketplace decisions.
- Adjusted Online Shoppers and Restaurant Quality comparisons where the source supports them.
- Current internal data for operational recommendations based on historical public datasets.

These gaps are disclosed rather than estimated or reconstructed. They do not block publication of the existing work, but they do block claims of measured commercial impact.

## Validation commands

```text
python scripts/verify_published_evidence.py
python -m pytest ai_engineering/complaintflow/tests -q
npm run lint
npm run build
```
