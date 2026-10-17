---
title: "Screening Historical Job Posts for Fraud Signals"
date: 2026-05-10
categories: machine learning
tags:
  - nlp
  - classification
  - lightgbm
  - imbalanced-data
excerpt: "A fraud-screening study that compares text and profile signals and makes the detection versus review trade-off explicit."
problem: "Fake job posts were rare, so a system could appear accurate while missing every scam."
result: "On an untouched stratified test set, the combined TF-IDF/SVD and profile LightGBM model reached 72.8% recall and 96.9% precision at a 0.30 threshold selected on validation data."
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
  - /images/fake-job-feature-importance.png
header:
  teaser: /images/fake-job-all-models.png
---

## Project brief

- **Project:** Compare fake-job screening models on the Employment Scam Aegean Dataset.
- **Question:** How should a platform balance scam detection with manual-review capacity?
- **Built:** A text-only model, a combined model, separate training, validation, and test sets, and a validation-selected threshold.
- **Result:** At a 0.30 threshold selected on validation data, the combined model flagged 130 of 3,576 test posts (3.6%); 126 were labeled fake and 4 legitimate. It missed 47 of 173 fake posts. This historical result does not establish current performance.

## Business question

The Employment Scam Aegean Dataset contains **17,880** postings, of which **866** are fraudulent. A classifier that always predicts “legitimate” would be about 95% accurate while catching no scams.

The business question is: **can a platform identify suspicious posts early enough to protect job seekers without sending too many legitimate employers to review?**

## Data and preparation

The source is the public [Employment Scam Aegean Dataset (EMSCAD)](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction). It has 17,880 posts and 866 fake labels. I use a stratified 60/20/20 split: 10,728 training posts, 3,576 validation posts, and 3,576 test posts. The validation and test sets each contain 173 fake posts. The dataset covers 2012 to 2014.

## Stakeholder questions

- **Which model caught the most fake posts on test data?** The text-only logistic regression reached 87.9% recall.
- **What happened at the selected threshold?** A 0.30 threshold selected on validation data gave the combined model 72.8% recall and 96.9% precision on test data.
- **What review volume did that create?** 130 of 3,576 test posts (3.6%) were flagged; 4 of those were labeled legitimate.
- **How many fake posts did the combined model catch?** It caught 126 of 173 fake posts and missed 47. It falsely flagged 4 legitimate posts.

## Findings

### Text signals caught the most scams

The text-only logistic regression had **87.9% recall** and **0.906 PR-AUC** on the untouched test set. The combined model reached **0.832 F1** at the validation-selected threshold. It reached **0.815 F1** at the default 0.50 threshold. These results compare fixed candidates on historical data. They do not show how the models will perform on future scam patterns.

![Untouched EMSCAD test results: text-only recall was 87.9%, while the combined model reached 0.832 F1 at its validation-selected threshold](/images/fake-job-all-models.png)

### Lowering the threshold increased the share of scams caught

F1 was highest at **0.30** on the separate validation set. At this threshold, the combined model reached **0.832 F1**, **72.8% recall**, and **96.9% precision** on the untouched test set. It caught **126 of 173** fake posts, missed **47**, and falsely flagged **4** legitimate posts. At the default **0.50** threshold, test recall was **69.9%**.

![Validation data selected a 0.30 threshold. On the untouched test set, the combined model caught 126 of 173 fake posts and falsely flagged 4 legitimate posts](/images/fake-job-threshold-cv.png)

The cutoff is an operating decision. At this threshold, a reviewer would inspect about 36 posts per 1,000 in this test sample; about 35 were labeled fake, while 13 fake posts per 1,000 were missed. The platform must decide how it values missed scams, review time, and employer friction. These ratios are historical test results, not a production forecast.

### Posting language differed in development data

Terms such as “work from home,” “data entry,” and “tax free” were more common in fake posts in the development sample. Terms associated with specific organizations, qualifications, or roles appeared more often in legitimate posts. These are associations, not proof that a phrase identifies a scam in another period.

![Development-sample EMSCAD keyword comparison: terms associated with fake and legitimate postings differ](/images/fake-job-keywords.png)

### Text and profile fields shaped the tabular model

For the profile-feature LightGBM, split counts were highest for capitalization ratio, text length, industry, and word count. Split counts show how the model used fields. They do not show that changing a field would change whether a post is fraudulent.

![Training-sample LightGBM split counts ranked capitalization ratio, text length, industry, and word count highest](/images/fake-job-feature-importance.png)

### The random split does not measure future scam drift

The validation and test sets are random samples from the same 2012–2014 source period. They do not test performance on later scam patterns or changes in fraud prevalence.

## Built

The analysis compares TF-IDF logistic regression with combined TF-IDF/SVD and profile-feature LightGBM. It selects the combined-model threshold on validation data. It calculates keyword frequencies on development data and split-count importance on training data.

## Result

The text-only model had the highest test recall at 87.9%. The combined model at its validation-selected threshold flagged 3.6% of test posts, with 96.9% precision and 72.8% recall. The validation-selected threshold exposes a measurable review-versus-miss trade-off, but no live platform outcome was measured.

- Start with shadow scoring and human review, not automatic rejection.
- Choose the cutoff using review capacity and the cost of missed scams. Select it on validation data, not test labels.
- Monitor recall, false alerts, review time, appeals, and performance by industry and language.
- Recheck the model on a time-based sample because scam language and prevalence can change.

As a scale illustration, if **100,000 posts** had the dataset's 4.8% fraud rate, the combined model's test recall would identify about **3,500** fake posts. The text model's test recall would identify about **4,200**. This is not a forecast. Scam prevalence can change, so a production system needs a time-based test.

## Technical notes

The split is stratified and random. It assigns 60% of posts to training, 20% to threshold selection, and 20% to the final test. The dataset covers 2012 to 2014. It does not establish current fraud detection, fairness across groups, or production performance.

The source file is available from [Kaggle](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction). A checksum, download path, dependencies, and run command are in [`legacy_jekyll/scripts/fake-job-detection/README.md`](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/legacy_jekyll/scripts/fake-job-detection/README.md).
