---
title: "Instacart: Turning Reorder Patterns Into a Better Next-Basket Prompt"
date: 2026-08-30
categories: [growth analytics]
tags: [retention, reorder, basket analysis, grocery]
excerpt: "A next-order growth study using real grocery baskets to separate repeatable routines from attractive but unreliable cross-sell ideas."
problem: "A grocery marketplace wants to increase the next order without filling the reminder with products that customers rarely buy together or do not need again."
result: "The three-million-order public release makes reorder timing, product-level reorder flags, and order sequence observable, but it does not contain intervention assignment or profit."
published: false
kind: methods
---

## Business question

Should the next-basket experience lead with replenishment reminders, complementary products, or a broader discovery shelf?

## Why it matters

The wrong reminder can feel like spam, while a useful replenishment cue can shorten the path to a repeat order. The decision needs to distinguish products people reliably rebuy from products that merely co-occur once.

## Decision brief

- **Recommendation:** make replenishment the default for products with repeated order history, and use association rules only as secondary suggestions.
- **Evidence:** the public release contains about **3.4 million orders**, **206,209 users**, and **49,688 products** across relational order, product, aisle, and department files.
- **Evidence strength:** Moderate for behavioral patterns; low for causal impact because the dataset contains no reminder experiment.
- **Main risk:** an order sequence reflects purchase history, not current need. A reminder can create substitution, not an additional basket.
- **Next test:** randomize reminder eligibility and measure incremental reorder rate, basket value, opt-out rate, and contribution margin.

## Role

Role: relational data modeling, reorder-rate definition, basket association analysis, leakage review, and experiment design. No customer-level identity beyond the dataset’s anonymous `user_id` is inferred.

## Data used

The analysis uses the [Instacart Market Basket Analysis release](https://tech.instacart.com/3-million-instacart-orders-open-sourced-d40d29ead6f2). The source contains order history, products, aisles, departments, and product-level reorder labels. The dataset represents real anonymized grocery-order behavior, but it is a historical public release and its use is subject to the source terms.

The grain changes by table: one row per order in `orders`, one row per product-in-order in the order-product tables, and one row per product in `products`. Treating every product row as an order would inflate demand.

## Approach

1. Enforce primary-key and foreign-key checks across the six relational tables.
2. Build an order-level table without losing product-level reorder detail.
3. Measure repeat rate by product, aisle, department, and order number.
4. Compare simple replenishment candidates with co-purchase candidates.
5. Define an incremental experiment instead of treating correlation as recommendation impact.

## What the source supports

## Evidence and design visuals

### Context: the release supports sequence-level reorder analysis

![Instacart public release scale and relational structure: about 3.4 million orders, 206,209 users, 49,688 products, and six linked tables](/images/portfolio-instacart-scale.svg)

The visual establishes the data entities that must remain separate before computing reorder metrics.

### Evidence boundary: history is observable, incrementality is not

![Instacart evidence boundary: order cadence and reordered flags are observed, while reminder assignment, inventory, and margin are not](/images/portfolio-instacart-evidence.svg)

This boundary prevents co-occurrence or historical reorder from being presented as campaign lift.

### Design response: make replenishment the tested default

![Conceptual replenishment test: select known repeat products, hold out reminders, and decide using incremental orders and margin](/images/portfolio-instacart-holdout.svg)

The next-basket recommendation is therefore a testable policy, not an assumed outcome.

### Reorder is a different job from discovery

The data explicitly distinguishes reordered products from first-time products. Replenishment signals are strongest when the customer has already purchased the product in an earlier order.

**Meaning:** the best reminder candidate is often a known routine, not a product chosen only because it appears in the same basket.

**Why it matters:** defaulting to reorder suggestions reduces the risk of using a discovery heuristic as if it were a retention intervention.

### Basket co-occurrence is useful for ranking, not proof of complementarity

Products and aisles that appear in the same order can generate candidate pairs, but the relationship is affected by household routines, store availability, and order size.

**Meaning:** support and confidence describe what was bought together; they do not show that one product caused the other purchase.

**Why it matters:** cross-sell rules should be capped, diverse, and tested against a no-suggestion control.

### Timing is part of the product decision

The `days_since_prior_order` and `order_number` fields make it possible to compare reminder timing with observed reorder cadence.

**Meaning:** one fixed reminder interval will be early for some shoppers and late for others.

**Why it matters:** the experiment should test timing bands and avoid sending a prompt when the customer has recently ordered.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | About 3.4M orders, 206,209 users, 49,688 products, order sequence, cadence, and product-level reorder flags | Rank replenishment candidates and timing bands |
| Inferred | Prior purchase history is a safer reminder signal than one-time co-occurrence | Make replenishment the primary surface |
| Not established | A reminder creates an additional order or positive margin | Require a randomized holdout and economics |

## Validation record

- **Grain:** `orders` is one row per order; order-product tables are one row per product-in-order.
- **Checks:** primary and foreign keys are tested before joins; order KPIs are calculated before child-table expansion.
- **Guardrail:** co-purchase support is shown separately from causal or incremental reorder impact.

## Recommendation

**What:** launch a replenishment-first next-basket test with a small complementary shelf below it.

**Where / who:** start with customers and products having repeat history; suppress products that were bought once or have unstable intervals.

**Why:** the observed data supports repeat behavior as the most direct signal for a reorder prompt.

**Risk:** a reminder can shift a purchase earlier without increasing total orders, or make customers feel over-targeted.

**Next test:** compare no prompt, replenishment-only, and replenishment-plus-complementary suggestions with incremental order and margin guardrails.

## Evidence strength and limitations

This is a historical observational analysis. It cannot measure unserved demand, substitutions, inventory availability, delivery quality, price, margin, or causal response to a prompt. Anonymous users are not a representative sample of every grocery customer, and public competition releases may be sampled or transformed.

## Reproducibility

Source: [Instacart’s public release announcement](https://tech.instacart.com/3-million-instacart-orders-open-sourced-d40d29ead6f2). Dataset structure and validation decisions are recorded in the [expansion validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md).

## Technical appendix

The primary unit for retention is `user_id` × `order_number`; the primary unit for basket association is `order_id` × `product_id`. Reorder rate is the share of eligible product-in-order rows with `reordered=1`. Product pairs are filtered by support before any ranking to avoid promoting rare coincidences.
