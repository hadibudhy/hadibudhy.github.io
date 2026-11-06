# OTTO session recommendations

An offline baseline study for OTTO's public multi-objective recommender challenge. It compares action-specific item popularity with recent items from the visible session prefix, filled by action-specific popularity.

## Reproduce

The raw source archive is kept out of Git. Download it with the Kaggle CLI after accepting OTTO's dataset terms:

```powershell
kaggle datasets download -d otto/recsys-dataset -f otto-recsys-train.jsonl -p analysis_data/raw/otto
python projects/growth-analytics/04-otto-session-recommendations/src/analyze.py
```

The script reads the JSONL member directly from the compressed archive, checks its pinned SHA-256, and writes temporary validation data to the Git-ignored `analysis_data/processed/` directory. It then regenerates the three charts, metrics JSON, and evidence manifest. If the source content changes, the script stops until the data and findings have been reviewed.

The project uses Python, NumPy, and Matplotlib. `orjson` is optional and speeds up parsing; the standard JSON library is used when `orjson` is unavailable.

## Evaluation design

The validation split follows OTTO's published offline protocol: sessions starting in the final two days of the training file form the holdout. Sessions that begin before the cutoff are trimmed at the cutoff for training. The heldout sessions are filtered to items observed in the training period, and sessions with fewer than two remaining events are excluded. A seeded split (`42`) keeps a random visible prefix and labels only later events.

The next click is the click target. Cart and order targets are the distinct item IDs appearing later in the session. Recall@20 uses the competition's pooled denominators and weights: 0.10 for clicks, 0.30 for carts, and 0.60 for orders.

Popularity counts are computed from training-period events only. The second baseline places recent distinct items from the visible prefix first, then fills remaining slots with the corresponding action's training-period popularity list.

## Interpretation boundary

This is an offline benchmark on a historical, anonymized dataset. It does not contain recommendation impressions, randomized assignment, revenue, margin, or current OTTO production logs. Recall does not measure CTR, conversion lift, or business value.
