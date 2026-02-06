---
title: "Moving Beyond Manual Queries"
date: 2026-01-25
categories: [data engineering]
tags: [data engineering, sql, dbt, databricks]
excerpt: "From ad-hoc SQL to a versioned, tested Modern Data Stack pipeline"
header:
  teaser: "/images/waterfront.jpg"
mathjax: "true"
---

Like many analysts, I started by running SQL queries manually and saving them on my desktop. That approach works for ad-hoc analysis, but it quickly breaks down when queries grow larger, logic becomes shared, or results need to be trusted over time.

To move beyond this, I built a small project to learn the Modern Data Stack (MDS). The goal was simple: create an automated pipeline to calculate Customer Lifetime Value (CLV) while treating data logic like software—versioned, tested, and modular.

This post walks through how I set it up using only free tools.

---

## The Motivation

Relying on manual SQL scripts exposed a few clear limitations:

- **Version Control**  
  Changes are hard to track when files live locally and get overwritten.

- **Testing**  
  Data quality issues like null or duplicated IDs often surface too late.

- **Complexity**  
  Long, monolithic queries are difficult to debug, review, or explain.

I wanted a setup that encouraged better engineering habits by default.

---

## My Approach

I focused on tools that clearly separate storage, compute, and transformation.

- **Databricks Serverless (Free Edition)**  
  Used for compute.

- **dbt Core**  
  Used to manage transformations, dependencies, and tests.

- **GitHub**  
  Used for version control and change tracking.

---

## Structuring the Data

I followed the Medallion Architecture to keep the pipeline easy to reason about.

### 1. Bronze Layer (Raw)

This is the landing zone. Data is stored exactly as it arrives from the source, preserving the original record.

- `raw_customers`
- `raw_orders`

### 2. Silver Layer (Staging)

This layer handles basic cleanup and standardization. Column names are normalized (e.g., `id` → `customer_id`) and data types are fixed. Each model maps 1-to-1 with its source table.

### 3. Gold Layer (Marts)

This is where business logic lives. Clean Silver models are joined and aggregated to produce final metrics.

---

## The Logic

Instead of querying raw tables directly, the final model references upstream dbt models. dbt handles dependency resolution and execution order.

```sql
WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
)

SELECT
    customers.customer_id,
    customers.customer_name,
    SUM(orders.order_amount) AS lifetime_value
FROM customers
LEFT JOIN orders
    ON customers.customer_id = orders.customer_id
GROUP BY 1, 2
````

---

## Adding Safety Nets

To catch data issues early, I added basic tests in a `schema.yml` file. These tests run automatically every time the pipeline builds:

* **Uniqueness**
  Ensures `customer_id` is not duplicated.

* **Not Null**
  Ensures the primary key is always present.

If a test fails, the build stops. This prevents bad data from silently propagating downstream.

---

## What I Learned

This project helped me understand the difference between writing queries and building data systems. Even a small pipeline benefits from version control, testing, and clear structure.

Most importantly, it showed that you don’t need an enterprise budget to practice solid data engineering fundamentals.

---

## Code

Full code and setup instructions are available here:
[https://github.com/hadibudhy/projects/tree/main/data_engineering/mds-project](https://github.com/hadibudhy/projects/tree/main/data_engineering/mds-project)
