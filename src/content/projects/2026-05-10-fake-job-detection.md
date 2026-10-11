---
title: "Detecting Fake Job Posts Before They Reach Job Seekers"
date: 2026-05-10
categories: machine learning
tags:
  - nlp
  - classification
  - lightgbm
  - imbalanced-data
excerpt: "A fraud-screening study that compares text and profile signals and makes the detection versus review trade-off explicit."
problem: "Fake job posts were rare, so a system could appear accurate while missing every scam."
result: "On a stratified holdout, the tuned combined model reached 75% recall and 98% precision at a 0.10 threshold; the text-only model reached 91.3% recall."
featured: true
published: true
caseId: fake-job-detection
kind: completed
primaryTrack: product-analytics
displayOrder: 90
evidenceManifest: /data/evidence/fake-job-detection.json
evidenceVisuals:
  - /images/fake-job-all-models.png
  - /images/fake-job-threshold-cv.png
  - /images/fake-job-keywords.png
  - /images/fake-job-shap.png
header:
  teaser: /images/fake-job-all-models.png
---

## Executive summary

**Decision:** how should a hiring platform balance scam detection against human review capacity? **Finding:** text signals caught more fake posts than profile-only signals, and a 0.10 threshold raised the combined model's recall to 75% while keeping precision at 98% on the holdout. **Recommendation:** use text-first screening in shadow mode, keep a human review step, and monitor missed scams and false alerts.

## Problem - high accuracy can still miss nearly every scam

The Employment Scam Aegean Dataset contains **17,880** postings, of which **866** are fraudulent. A classifier that always predicts “legitimate” would be about 95% accurate while catching no scams.

The business question is: **can a platform identify suspicious posts early enough to protect job seekers without sending too many legitimate employers to review?**

## Hypotheses - what could improve screening?

- **The wording may carry more signal than profile fields.** Compare a text-only model with profile-only and combined models.
- **A 0.50 cutoff may be too conservative for a rare positive class.** Test lower cutoffs and compare recall, precision, and F1.
- **A strong holdout result may vary across splits.** Repeat evaluation with stratified folds before recommending an operating threshold.

## Analysis - what did the model comparisons show?

The source is the public [Employment Scam Aegean Dataset (EMSCAD)](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction). The analysis uses a fixed 17,880-row source snapshot, then creates a stratified 80/20 split with **3,576** held-out posts, including **173** fake posts. I compared TF-IDF logistic regression, profile-feature LightGBM, and a sentence-embedding plus LightGBM model. These results describe this historical dataset, not a current platform.

### Text signals caught the most scams

The text-only logistic regression model had **91.3% recall** and **0.927 PR-AUC**. The tuned combined model had the highest F1 at **0.850**, while the profile-only model had weaker recall. This supports including posting text in a review process; it does not prove that these features will generalize to new scam patterns.

![Held-out EMSCAD results: the text model caught more scams, while the tuned combined model had the highest F1](/images/fake-job-all-models.png)

### Lowering the threshold increased the share of scams caught

At the default 0.50 threshold, the combined model reached **0.831 F1** and **71.1% recall**. At **0.10**, it reached **0.850 F1**, **75.1% recall**, and **98% precision**. In this test, it caught about 130 of 173 fake posts and missed about 43. These counts are approximate because the published rates are rounded.

![Threshold and five-fold validation: a 0.10 cutoff balances scam capture with review volume](/images/fake-job-threshold-cv.png)

The cutoff is an operating decision. Higher recall can protect more job seekers but may increase the review queue. The platform must decide how it values missed scams, review time, and employer friction.

### Posting language differed between the two classes

Terms such as “work from home,” “data entry,” and “tax free” were more common in fake posts in this dataset. Terms associated with specific organizations, qualifications, or roles appeared more often in legitimate posts. These are associations, not proof that a phrase identifies a scam in another period.

![EMSCAD keyword comparison: terms associated with fake and legitimate postings differ in the labeled dataset](/images/fake-job-keywords.png)

### Profile and text features both influenced the combined model

For a LightGBM model using profile and engineered text features, the largest mean absolute SHAP values were for industry, company-profile availability, required education, word count, and text length. SHAP describes model behavior; it does not show that changing a feature would change whether a job is fraudulent.

![SHAP summary for the tabular LightGBM model: profile and text-derived features both influenced predictions](/images/fake-job-shap.png)

### Cross-validation showed variation across folds

Across five stratified folds, mean F1 was **0.8251** with a standard deviation of **0.0208**; mean ROC-AUC was **0.9859** with a standard deviation of **0.0030**. F1 varies more because each test fold contains relatively few fraudulent posts.

## Result - use the model as a review aid, not an automatic decision

The text-signal hypothesis was supported in this dataset. Lowering the combined model's threshold improved recall while precision stayed high on the holdout. Cross-validation showed some variation, and no live platform outcome was measured.

- Start with shadow scoring and human review, not automatic rejection.
- Choose the cutoff using review capacity and the cost of missed scams.
- Monitor recall, false alerts, review time, appeals, and performance by industry and language.
- Recheck the model on a time-based sample because scam language and prevalence can change.

As a sensitivity scenario, if **100,000 future posts** had the dataset's 4.8% fraud rate, the tuned model's recall would identify roughly **3,600** fraudulent posts; the text model's recall would identify roughly **4,400**. This is not a forecast. Scam prevalence can change, and a production system needs a time-based test.

## Technical notes

The model compares TF-IDF logistic regression, profile-feature LightGBM, and a sentence-embedding plus LightGBM model using `all-MiniLM-L6-v2`. The train/test split is random and stratified, not chronological. The dataset covers 2012 to 2014, so the reported metrics do not establish current fraud detection, fairness across groups, or production performance.

The source file is available from [Kaggle](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction). A checksum, download path, dependencies, and run command are in [`legacy_jekyll/scripts/fake-job-detection/README.md`](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/legacy_jekyll/scripts/fake-job-detection/README.md).
