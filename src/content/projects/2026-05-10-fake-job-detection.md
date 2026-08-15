---
title: "Detecting Fake Job Posts Before They Reach Job Seekers"
date: 2026-05-10
categories: machine learning
tags:
  - nlp
  - classification
  - lightgbm
  - sentence-transformers
  - imbalanced-data
excerpt: "A fraud-detection study showing why the language in a job post is more useful than surface-level profile details."
problem: "Fake job posts were rare, so a system could appear accurate while missing every scam."
result: "The best balance caught 75% of fake posts and was correct 98% of the time when it raised an alert."
featured: true
header:
  teaser: /images/fake-job-all-models.png
---

## Business context

Fake job posts can harm both job seekers and employment platforms. Scammers may use attractive job titles to collect personal information, request fees, or impersonate real companies.

This project uses 17,880 job postings from the Employment Scam Aegean Dataset. Only 866 posts were fraudulent, so fake posts made up about 1 in 20 records.

## Business question

Can a platform identify suspicious job posts early enough to protect users, while avoiding too many false alarms for legitimate employers?

## How I approached it

I compared three ways to identify fraud:

1. Read the words and phrases in the posting.
2. Use profile details such as industry, education, or whether the company had a logo.
3. Combine the posting's meaning with those profile details.

The goal was to compare the signals, not to choose a complex model for its own sake.

## Why accuracy was not enough

There were about 19.6 real job posts for every fake post. A system that marked every post as real would be about 95% accurate while missing every scam.

For this problem, two questions matter more:

- **Recall:** How many of the fake posts did the system catch?
- **Precision:** When the system flagged a post, how often was it actually fake?

The F1 score combines those two measures. It helps show whether the system catches enough fraud without creating too many unnecessary reviews.

## Finding 1: The words in the post mattered most

The model that used profile details without reading the post had the weakest overall F1 score. Adding the text improved performance significantly.

![Text-based signals outperformed profile details when identifying fake job posts](/images/fake-job-all-models.png)

Scammers can easily add a logo, choose a credible industry, or select “full-time” as the employment type. Their wording is harder to disguise. Phrases such as “earn money from home,” “no experience needed,” and “tax free income” appeared more often in fake posts.

**Business meaning:** Content review should be part of a fraud-screening process. Surface-level profile checks alone can create a false sense of security.

## Finding 2: The decision threshold needed to be lower

The model normally labels a post as fake when its score is above 0.50. That setting was too cautious for a problem where fake posts were rare.

Testing different thresholds showed that 0.10 gave the best balance for the sentence-based model:

- F1 increased from 0.831 to **0.850**.
- Recall increased from 71% to **75%**.
- Precision stayed high at **98%**.

In plain terms, the tuned system caught about 75 of every 100 fake posts. When it flagged a post, it was correct about 98 times out of 100 in this test.

![The best balance between catching fraud and avoiding false alarms appeared at a 0.10 threshold](/images/fake-job-threshold-cv.png)

The right threshold is a product decision. A platform that wants to catch more scams may accept more human reviews. A platform that wants fewer reviews may choose a stricter threshold and miss more cases.

## Finding 3: Fake posts used recognizable language

Fake posts often used emotional or aspirational phrases such as “work from home,” “earn,” “tax free,” “typing,” and “data entry.” Some groups appeared to imitate energy companies or promise international opportunities.

Real posts were more specific about location, qualifications, and job structure. This difference gives reviewers and future models useful signals to investigate.

![The language patterns that appeared more often in fake and real job posts](/images/fake-job-keywords.png)

## Finding 4: Profile details still added useful context

Feature contribution analysis showed that industry, the presence of a company profile, required education, text length, capitalization, and exclamation marks all influenced the prediction.

Having a company logo was not the strongest signal. It ranked 11th, which supports the earlier finding: a logo alone is not a reliable sign that a posting is legitimate.

![The profile and writing features that influenced fraud predictions](/images/fake-job-shap.png)

## How stable were the results?

I tested the tuned model across five different data splits. The average F1 score was **0.825 +/- 0.021**, and the average ROC-AUC was **0.986 +/- 0.003**. The results were consistent enough to support the main findings, although the F1 score varied more because each test split contained only about 173 fake posts.

| Model | F1 | Recall | PR-AUC |
|-------|----|--------|--------|
| Logistic regression using text | 0.819 | **0.913** | **0.927** |
| LightGBM using profile details | 0.828 | 0.723 | 0.915 |
| Sentence model + LightGBM, default threshold | 0.831 | 0.711 | 0.901 |
| **Sentence model + LightGBM, tuned threshold** | **0.850** | 0.751 | 0.901 |

The simple text model caught the most fake posts, with 91.3% recall. The tuned combined model had the highest F1 score and very high precision. The best choice depends on whether the platform values maximum fraud detection or fewer false alarms.

## Recommendation

Use text as the first line of screening, combine it with profile details, and set the threshold according to the cost of missed scams and manual reviews. Any production system should also keep human review in the loop and monitor how performance changes as scam language evolves.

## Takeaway

The strongest fraud signal was not whether a company had a logo. It was the language and structure of the job post. A practical screening system should read the content, tune its decision threshold, and make the trade-off between protection and review effort explicit.

## Supporting technical detail

The study compared logistic regression using TF-IDF word and phrase counts, LightGBM using 19 profile features, and a sentence-embedding model combined with LightGBM. The embedding model represented the meaning of each post in 384 dimensions. Feature contribution values were calculated on a 200-sample stratified test subset.

**Dataset:** 17,880 job postings, including 866 fraudulent records. The train/test split was 80/20 and stratified by the target label.

**Code and data:** [View the analysis scripts](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/legacy_jekyll/scripts/fake-job-detection)
