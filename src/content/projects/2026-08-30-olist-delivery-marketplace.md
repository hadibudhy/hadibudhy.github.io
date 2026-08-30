---
title: "Olist: Find the Delivery Failures That Put Marketplace Trust at Risk"
date: 2026-08-30
categories: [marketplace operations]
tags: [marketplace, delivery, sellers, customer experience]
excerpt: "A Brazilian e-commerce operations study that joins orders, sellers, products, payments, freight, and reviews to separate late delivery from product or seller-quality problems."
problem: "A marketplace wants to improve customer trust, but a low review score can come from late delivery, product mismatch, payment friction, or seller behavior."
result: "The public Olist release links about 100,000 orders across customers, sellers, products, payments, freight, delivery dates, and reviews; it supports root-cause decomposition without exposing private customer identity."
published: true
---

## Business question

Should the marketplace invest first in seller coaching, carrier performance, product-page quality, or promise-date accuracy?

## Why it matters

Delivery issues are visible to customers but operationally ambiguous. Treating every low review as a seller problem can punish good sellers for carrier delays; treating every delay as a carrier problem can miss poor listing or fulfillment behavior.

## Decision brief

- **Recommendation:** make on-time delivery and review outcomes a joint diagnostic, with seller coaching targeted only after carrier and product controls are checked.
- **Evidence:** the [Olist Brazilian e-commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) contains roughly 100,000 orders and multiple relational tables for orders, customers, sellers, products, payments, freight, and reviews.
- **Evidence strength:** Moderate for historical operational associations; low for causal intervention impact.
- **Main risk:** the release is historical, the customer IDs are anonymized, and the data does not include carrier identity, contacts, or marketplace-wide unserved demand.
- **Next test:** randomize seller coaching or promise-message changes within eligible lanes and measure on-time delivery, review score, cancellation, and contribution.

## Role

Role: relational joins, delivery-promise calculation, seller and product rollups, outcome decomposition, and operational test design.

## Data used

The analysis uses the [Olist public dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), originally published for educational analysis. The grain differs by table: one row per order, item, payment, review, seller, customer, or product. Order timing fields support comparison of purchase, estimated delivery, actual delivery, and review outcomes.

The release measures recorded marketplace transactions. It does not measure browsing, rejected orders, customer support contacts, carrier scans, or profit at the order level.

## Approach

1. Declare the order as the primary business entity and validate one-to-many joins.
2. Deduplicate only at the table grain; never drop legitimate multi-item orders.
3. Derive delivery lateness from actual versus estimated delivery timestamps.
4. Compare review outcomes by lateness, seller, product category, geography, and freight context.
5. Use a holdout for any seller or promise intervention.

## Key findings

## Visual evidence

### Context: the order is the business entity across multiple child tables

![Olist public release scope: about 100,000 orders from 2016–2018 connect delivery dates, sellers, freight, products, payments, and reviews](/images/portfolio-olist-scale.svg)

The data model explains why order-level KPIs must be calculated before one-to-many joins.

### Main finding: promise and review do not reveal root cause by themselves

![Olist evidence boundary: delivery dates and reviews are observed, while carrier events, unplaced demand, and contribution margin are not](/images/portfolio-olist-boundary.svg)

This keeps a low review score from becoming an unsupported seller penalty.

### Decision: route the operational cause before coaching

![Conceptual Olist delivery-quality pilot: diagnose the promise gap, route to seller, carrier, or product, then compare coaching with control](/images/portfolio-olist-pilot.svg)

The visual turns the diagnostic into a bounded marketplace intervention.

### A review is an outcome, not a root cause

The joined model makes it possible to compare review scores with delivery timing and order context.

**Meaning:** a low score can be associated with several operational pathways.

**Why it matters:** route the issue to the team that can change it rather than sending every complaint to sellers.

### Promise accuracy is a separate metric from delivery speed

An order can arrive quickly but late against its promise, or arrive slowly while still meeting the promise.

**Meaning:** customers experience the promise gap, not only elapsed days.

**Why it matters:** operations should monitor on-time rate and delivery duration separately.

### Joins can create false order volume

Orders have multiple items, payments, and review or installment records.

**Meaning:** summing after a many-to-many join can inflate revenue, order count, and seller exposure.

**Why it matters:** a trusted marketplace dashboard needs one row per order for order KPIs and child-level tables for diagnostics.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | About 100,000 orders connect purchase, promise, delivery, seller, freight, and review fields | Decompose delivery-quality pathways |
| Inferred | Promise lateness may be a more actionable service signal than review score alone | Route work to seller, carrier, or product teams |
| Not established | Lateness caused a review score, or an intervention will improve contribution | Test coaching and promise changes |

## Validation record

- **Grain:** one order with item, payment, and review child rows.
- **Checks:** order-level KPIs are calculated before child joins; missing delivery timestamps stay missing.
- **Guardrail:** actual versus estimated delivery is reported separately from elapsed delivery duration.

## Recommendation

**What:** create a delivery-quality queue that combines promise lateness, review outcome, freight burden, and seller history.

**Where / who:** begin with lanes and sellers where lateness is repeated and the cause is observable.

**Why:** the public data supports operational triage but not a universal seller penalty.

**Risk:** intervention can shift volume away from small sellers or reward better reporting rather than better service.

**Next test:** compare targeted coaching, promise-date improvement, and no intervention with seller retention and customer-experience guardrails.

## Evidence strength and limitations

This is an observational historical release. It cannot establish that lateness caused a review score, identify current carrier performance, estimate profit, or measure orders that were never placed. Seller and customer identifiers are dataset keys, not real-world identities.

## Reproducibility

Source: [Olist Brazilian e-commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Join, grain, and limitation checks are recorded in the [portfolio expansion validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md).

## Technical appendix

Calculate order-level metrics before joining item, payment, or review children. Delivery lateness is `delivered_customer_date - estimated_delivery_date`; missing timestamps remain missing and are reported as data-quality cases rather than imputed as on-time.
