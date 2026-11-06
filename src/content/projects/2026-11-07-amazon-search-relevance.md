---
title: "Amazon Product Search: Can More Fields Improve Relevance Ranking?"
date: 2026-11-07
categories: [product analytics, search relevance]
tags: [Amazon, ESCI, product search, ranking, text matching]
excerpt: "A query-held-out reranking study tests whether product brand and color add value beyond title matching."
problem: "Amazon's public search benchmark asks how to rank a fixed list of candidate products so exact and useful matches appear before irrelevant results."
result: "On 8,956 held-out US queries, a train-tuned lexical score raised full nDCG from 0.7965 to 0.7982; the paired-query 95% interval for the gain is 0.0006 to 0.0030."
featured: false
published: true
kind: completed
artifactLabel: Product search relevance
caseId: amazon-search-relevance
primaryTrack: product-analytics
secondaryTracks: []
displayOrder: 96
evidenceManifest: /data/evidence/amazon-search-ranking.json
evidenceVisuals:
  - /images/amazon-esci-label-distribution.png
  - /images/amazon-search-ranking-ndcg.png
  - /images/amazon-search-top10-labels.png
header:
  teaser: /images/amazon-search-ranking-ndcg.png
---

## Project brief

- **Project:** Rerank Amazon's public candidate products for each shopping query.
- **Question:** Do brand, color, bullets, and descriptions improve on title-only lexical matching?
- **Built:** Two text-matching baselines, with field weights selected on train queries and scored on held-out queries.
- **Result:** Field-weighted full nDCG improved by 0.0017 (95% paired-query bootstrap interval: 0.0006–0.0030). nDCG@10 improved by 0.0038 (0.0024–0.0055). These are small offline ranking gains.

## Business question

Amazon released the Shopping Queries dataset to support research on matching shopping queries with useful product results. The labels distinguish an **Exact** match, a **Substitute**, a **Complement**, or an **Irrelevant** product. The benchmark asks systems to rank a fixed candidate list for each query; it does not ask us to retrieve products from Amazon's full catalog. [Amazon's dataset description](https://www.amazon.science/code-and-datasets/shopping-queries-dataset-a-large-scale-esci-benchmark-for-improving-product-search) frames ranking and substitute discovery as ways to improve product search.

The project asks whether product text fields beyond the title help reorder those candidates. It studies query-level ranking, not session recommendations or next-basket suggestions.

## Data and preparation

I used Task 1's reduced `small_version` and the **US** marketplace. The slice contains **601,354 query–product judgments** across **29,844 queries**: 20,888 training queries and 8,956 held-out test queries. Each query has a preselected list of judged candidate products. The examples and product metadata are from Amazon Science's 2022 release, which is licensed under [Apache-2.0](https://github.com/amazon-science/esci-data/blob/main/LICENSE).

The examples and product records are joined on both `product_locale` and `product_id`. All **482,105** candidate products had metadata rows. Several text fields were blank: descriptions were missing for **47.8%** of these products, colors for **32.2%**, bullet points for **13.2%**, and brands for **5.6%**.

## Method

The title-only baseline ranks candidates by IDF-weighted query-token coverage in the product title. The second score adds coverage in the product's bullet points, description, brand, and color.

To select field weights without looking at test labels, I split the provided training queries into **16,710 calibration queries** and **4,178 tuning queries** using seed 42. I estimated query-token IDF on the calibration subset, then selected a small field-weight grid on the tuning subset. The selected score used title weight **1.0**, brand **0.5**, color **0.5**, and zero weight for bullets and descriptions. Product ID breaks score ties in a stable order.

The official metric is query-macro nDCG using Amazon's published gains: Exact **1**, Complement **0.1**, Substitute **0.01**, and Irrelevant **0**. I also report nDCG@10 as a local top-ten view, not the official full-list metric.

## Findings

### The added fields make a small difference

On the held-out queries, title-only matching scored **0.7965 full nDCG** and **0.6670 nDCG@10**. The train-tuned field score reached **0.7982** and **0.6709**. A paired bootstrap over the 8,956 test queries put the full-nDCG change at **+0.0017** (95% interval **+0.0006 to +0.0030**) and the nDCG@10 change at **+0.0038** (**+0.0024 to +0.0055**).

The gains are consistent but modest. The selected weights retained the title signal, added small contributions from brand and color, and gave no weight to bullet or description text.

![Official full nDCG and local nDCG@10 for title-only and train-tuned field-weighted lexical ranking on the held-out US queries](/images/amazon-search-ranking-ndcg.png)

### Exact matches occupy about half of the top ten

In the title-only top tens, **48.7%** of ranked candidates were Exact and **13.7%** were Irrelevant. The field-weighted top tens were **49.0% Exact** and **13.8% Irrelevant**. The similar mix reinforces that adding metadata fields changed ranking quality only slightly.

![ESCI relevance labels among the top ten candidate products for each ranking baseline on test queries](/images/amazon-search-top10-labels.png)

### Train and test queries have similar label mixes

The Task 1 split includes Exact, Substitute, Complement, and Irrelevant judgments in both the training and test queries. Keeping these classes visible matters: a substitute can help a shopper, while an irrelevant result should fall below a useful result.

![Share of Exact, Substitute, Complement, and Irrelevant judgments in the US small-version train and test splits](/images/amazon-esci-label-distribution.png)

## Recommendation

Keep title matching as the main lexical signal, then test small brand and color boosts in a controlled search experiment. This benchmark supports a modest offline ranking gain; it cannot tell whether shoppers see the candidates or whether the rank change improves clicks, purchases, or sales.

## Limitations

This project reranks preselected candidate products. It does not test full-catalog retrieval. ESCI labels are human relevance judgments, not observed clicks or purchases. The dataset has no impression positions, randomized assignment, sales, or margin, and its queries are from a 2022 benchmark rather than current search traffic. Missing descriptions, bullets, colors, and brands also limit what text-based features can use.

## Technical notes

The analysis uses the provided query-disjoint split. Field weights are selected on train queries; test labels are used only for the final scores. The official Amazon scorer maps qrel grades E=4, C=3, S=2, I=1 to gains 1, 0.1, 0.01, and 0, respectively. nDCG@10 is an additional local metric. Source-file hashes, pair counts, evaluation results, and chart hashes are recorded in the [evidence manifest](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/public/data/evidence/amazon-search-ranking.json). Reproduction instructions are in the [project README](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/projects/growth-analytics/05-amazon-search-relevance/README.md).
