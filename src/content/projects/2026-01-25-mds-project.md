---
title: "Making Customer Value Metrics Easier to Trust"
date: 2026-01-25
categories: [data engineering]
tags: [data engineering, sql, dbt, databricks]
excerpt: "Turning a manual customer value calculation into a repeatable, tested data process."
problem: "A manual customer value calculation was difficult to review, test, and reuse."
result: "Built a repeatable data process with automated checks using dbt and Databricks."
featured: true
header:
  teaser: "/images/mds-project.png"
---

## Business context

Customer Lifetime Value (CLV) helps a business understand how much value each customer creates over time. It can guide marketing, service, and growth decisions. However, a useful metric is difficult to trust when its calculation lives in a long SQL query on one person's computer.

I built this project to replace that fragile process with a repeatable data pipeline. The goal was not to add more tools. It was to make the calculation easier to review, test, update, and use again.

## Business question

How can a team calculate customer value in a way that remains consistent as the data and business logic change?

## How I approached it

I separated the work into three simple stages:

- **Raw data:** Keep customer and order records as they arrive.
- **Clean data:** Standardize names and data types so the records are easier to use.
- **Business metrics:** Join the clean records and calculate customer-level value.

The process uses Databricks for computing the data, dbt for managing the transformations and tests, and GitHub for tracking changes. These tools are supporting detail; the main improvement is the structure around the metric.

## What changed

The new process replaces a manual query with a versioned, automated pipeline. A change to the calculation can now be reviewed before it is used. Basic checks also catch missing or duplicated customer IDs before they reach the final metric.

That matters because a wrong CLV number can lead to poor decisions about customer segments, marketing spend, or service priorities. The pipeline does not make the business decision itself, but it makes the number behind that decision more dependable.

## Recommendation

For recurring business metrics, keep the calculation in a shared, tested process instead of a personal SQL file. Start with a small number of useful checks, such as unique customer IDs and required fields, then add more checks as the metric becomes more important.

## Takeaway

The value of this project is not only the CLV calculation. It is the move from a one-off answer to a process that a team can trust, review, and improve.

## Supporting technical detail

The final model uses clean customer and order records, then groups order value by customer:

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
```

The pipeline follows a simple raw, cleaned, and business-ready structure. Tests check that customer IDs are present and unique. If a test fails, the build stops instead of allowing a questionable metric to move downstream.

**Code and setup:** [View the project repository](https://github.com/hadibudhy/projects/tree/main/data_engineering/mds-project)
