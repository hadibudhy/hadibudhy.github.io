---
title: "Sales Churn Predictor"
date: 2026-02-10
categories: [machine learning]
tags: [python, scikit-learn, aws, xgboost]
excerpt: "Predicting customer churn to proactively save MRR."
problem: "High customer churn was reducing MRR with no early warning system."
result: "Reduced churn by 15% via a predictive XGBoost model."
header:
  teaser: "/images/sales-churn.png"
mathjax: "true"
---

## Executive Summary

Brief explanation of the business problem. High customer churn was eating into the Monthly Recurring Revenue (MRR), and the retention team had no way of knowing which accounts were at risk until they submitted a cancellation request.

## Impact & Metrics

- Reduced customer churn by 15% within the first quarter of deployment.
- Saved an estimated $500k in lost revenue annually.
- Model achieved 92% ROC-AUC on the holdout test set.

## Technical Approach

We formulated this as a binary classification problem to predict the likelihood of an account churning within the next 30 days.

### Data Engineering
We combined product usage telemetry, billing history, and support ticket metadata from our Snowflake data warehouse.

### Modeling
We trained an XGBoost model, handling class imbalance with SMOTE and optimizing hyperparameters via Bayesian Optimization. Feature importance analysis revealed that a sudden drop in core feature usage was the strongest predictor.

### Deployment
The model was deployed as a SageMaker endpoint, with daily batch inferences written back to Salesforce to alert account managers.
