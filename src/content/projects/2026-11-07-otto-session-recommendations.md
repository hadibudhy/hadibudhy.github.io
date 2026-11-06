---
title: "OTTO's 2022 Recommender Challenge: Clicks, Carts, and Orders"
date: 2026-11-07
categories: [product analytics, recommenders]
tags: [session-based recommendation, e-commerce, Recall@20, OTTO]
excerpt: "An offline session-recommendation study compares recent item context with action-specific popularity across clicks, carts, and orders."
problem: "OTTO's public challenge asked how to recommend products for a customer's next click, cart, or order instead of optimizing clicks alone."
result: "On 515,702 eligible known-item sessions, a recent-session baseline scored 0.473 OTTO-weighted Recall@20 on our local holdout versus 0.0057 for popularity alone."
featured: true
published: true
kind: flagship
artifactLabel: Applied data science
caseId: otto-session-recommendations
primaryTrack: product-analytics
secondaryTracks: []
displayOrder: 95
evidenceManifest: /data/evidence/otto-session-recommendations.json
evidenceVisuals:
  - /images/otto-session-event-mix.png
  - /images/otto-baseline-recall.png
  - /images/otto-prefix-context-recall.png
header:
  teaser: /images/otto-baseline-recall.png
---

## Project brief

- **Project:** Evaluate simple candidate-retrieval strategies for OTTO's multi-objective recommendation problem.
- **Question:** Does the visible session history improve Recall@20 over global item popularity for clicks, carts, and orders?
- **Built:** A time-based offline holdout, action-specific popularity baseline, and recent-session-items baseline.
- **Result:** The session-history baseline improved OTTO-weighted Recall@20 from 0.0057 to 0.4727 on our local holdout of 515,702 eligible known-item sessions. This is not a live impact estimate.

## Business question

OTTO's 2022 challenge asked recommenders to predict products a shopper would click, add to cart, or order. Optimizing for clicks alone can overlook downstream actions, while the company's public challenge weights orders more heavily than clicks. [OTTO described the challenge and its multi-objective goal](https://www.otto.de/jobs/en/blogs/techblog/otto-machine-learning-competition/).

The question here is narrower: **does the current session provide useful candidate items beyond items that are popular for each action?** The study compares two transparent baselines before attempting a more complex ranking model.

## Data and preparation

The [OTTO Recommender Systems Dataset](https://github.com/otto-de/recsys-dataset) contains anonymized webshop and app events. The released training file includes **12.9 million sessions** and **216.7 million events** across about **1.8 million item IDs**, from **31 July to 28 August 2022 UTC**. Events are clicks, cart additions, and orders. Item IDs have no product text, category, or price metadata. OTTO publishes the data under a [CC BY 4.0 license](https://github.com/otto-de/recsys-dataset#license).

The data is historical, and a session is not a unique person across visits. This project measures within-session candidate retrieval; it does not model customer-level purchase history.

## Validation design

The offline holdout follows OTTO's [published split and evaluation rules](https://github.com/otto-de/recsys-dataset/blob/main/KAGGLE.md). Of the **516,346** sessions starting in the final two days, **515,702** remained after filtering items not seen in training and sessions with fewer than two events. The remaining **644 sessions** are excluded from the score. Earlier sessions are truncated at the time boundary; **189,024** sessions with fewer than two pre-cutoff events are also dropped, leaving **12,194,409** training sessions.

For each heldout session, items not observed before the cutoff are filtered, sessions with fewer than two remaining events are dropped, and a seeded split (`42`) creates a visible prefix and future labels. Click labels use the next future click; cart and order labels use the distinct future item IDs for each action.

The official metric is **weighted Recall@20**: 0.10 for clicks, 0.30 for carts, and 0.60 for orders. Recall uses pooled hits and denominators across the validation sessions.

## Baselines

1. **Action-specific popularity:** rank items by their click, cart, or order event frequency in the training period.
2. **Recent session items plus popularity:** rank up to 20 distinct items from the visible session prefix by recency, then fill any remaining slots with the matching action's popularity list.

The second baseline is a candidate-retrieval rule. It uses no product metadata, model training, or validation suffix events.

## Findings

### The training file is dominated by clicks

The source contained **194.7 million click events**, **16.9 million cart events**, and **5.1 million order events**. Each action has a different base rate, so the study reports action-level recall and the challenge's weighted score separately.

![OTTO's 2022 training file contains 194.7 million clicks, 16.9 million cart events, and 5.1 million orders](/images/otto-session-event-mix.png)

### Recent session items beat global popularity on this holdout

The recent-session baseline reached **0.318 Recall@20 for next clicks**, **0.308 for cart items**, and **0.581 for ordered items**. The popularity baseline scored **0.008**, **0.005**, and **0.006**, respectively. Using OTTO's official weights, the local-holdout scores were **0.4727** and **0.0057**.

![Action-specific Recall@20 on 515,702 eligible sessions: recent session items plus popularity compared with popularity alone](/images/otto-baseline-recall.png)

This large gap shows that items already present in the visible session are strong candidates for its future actions in this offline split. It does not show that placing those items in a recommendation module causes more clicks or orders.

### Longer prefixes had higher weighted recall in this split

The recent-session baseline's weighted Recall@20 was **0.416** for prefixes of 1–3 events, **0.482** for 4–8 events, and **0.499** for 9 or more events. These groups are descriptive, not randomized; session length may reflect intent, product type, or other differences.

![Weighted Recall@20 by visible session-prefix length: short n=373,031, medium n=88,075, and long n=54,596](/images/otto-prefix-context-recall.png)

## Recommendation

Use recent, distinct session items as a simple retrieval baseline and fill remaining candidate slots with action-specific popularity. The offline result supports evaluating this strategy further before investing in a more complex ranker.

The next business test needs recommendation impressions, item positions, random assignment, product availability, and order value or margin. Measure clicks, carts, and orders separately, and assess whether the ranking changes downstream purchases rather than only offline recall.

## Limitations

This is a historical public benchmark from 2022, not a measurement of OTTO's current production recommender. Because unknown items are removed, the score is conditional on items already seen in training and does not measure cold-start performance. The release has anonymized item IDs and no recommendation impressions, assignments, prices, margin, or product metadata. Recall@20 measures whether heldout items appear in a candidate list; it does not measure exposure, conversion lift, revenue, or profit. OTTO notes in its [dataset documentation](https://github.com/otto-de/recsys-dataset) that recommendations generated about 20% of product-page views in the release, so many observed interactions came from other discovery paths.

## Technical notes

The analysis reads the official training JSONL from its Kaggle archive and pins the JSONL content hash in the [evidence manifest](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/public/data/evidence/otto-session-recommendations.json). It generates the holdout in a streaming pass, keeps raw and temporary validation data under ignored `analysis_data/`, and writes the charts and metrics through [the project script](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/projects/growth-analytics/04-otto-session-recommendations/src/analyze.py). Reproduction commands and split details are in the [project README](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/projects/growth-analytics/04-otto-session-recommendations/README.md).
