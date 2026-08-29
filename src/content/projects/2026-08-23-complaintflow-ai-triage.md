---
title: "ComplaintFlow: A Reliable AI Triage Service for Consumer Support"
date: 2026-08-23
categories: [AI engineering]
tags:
  - production AI
  - evaluation
  - retrieval
  - reliability
  - FastAPI
excerpt: "A production-oriented AI service that routes financial complaints, retrieves approved support playbooks, escalates uncertainty, and records enough evidence to evaluate every decision."
problem: "Support teams need to route complaints quickly, but an unreliable AI response can send a customer to the wrong queue or invent guidance."
result: "Portfolio reference implementation: ComplaintFlow combines a transparent baseline, approved-playbook retrieval, provider retries, PII redaction, schema checks, human escalation, and an auditable SQLite decision log."
featured: true
header:
  teaser: /images/complaintflow-architecture.svg
---

## Executive summary

**Business problem:** support operations spends time reading and routing complaints, while incorrect or unsupported AI guidance creates customer, compliance, and trust risk.

**AI solution:** ComplaintFlow is a portfolio reference implementation, not a production deployment. It recommends a support queue and retrieves an approved playbook. It does not make refunds, credit, legal, or regulatory decisions.

**Engineering result:** the system has a FastAPI endpoint, input validation, PII redaction, a transparent baseline, retrieval, retries, fallback routing, SQLite persistence, and automated tests.

**Business value:** the first measurable outcome is faster, more consistent triage. The system is designed so production value can be measured without hiding uncertainty behind a confident answer.

## Business question

The decision owner is a support operations manager. The decision is:

1. Which queue should receive the complaint?
2. Is there an approved playbook that matches the issue?
3. Is confidence high enough to assist, or should a person review it first?

The north-star metric is **correct queue routing**. Supporting metrics are time saved per case, citation coverage, provider latency, and fallback rate. Guardrails are escalation recall, unsupported-answer rate, PII exposure, customer complaints, and cost per case.

## Why it matters

The [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) publishes complaint records and some consumer narratives after privacy review. The Bureau says the data is freely available and generally updated daily, but it is not a representative sample of all consumer experiences.

That limitation shapes the system. ComplaintFlow helps with routing and evidence retrieval; it does not estimate total consumer harm or decide whether a company response is correct.

## Data used

The public complaint data is an example source for the workflow, not a representative measure of all consumer support demand. The service's checked-in evaluation fixture is synthetic and small; production quality requires privacy-reviewed, labeled cases.

## Approach

![ComplaintFlow reference architecture: A bounded AI workflow validates input, redacts PII, retrieves approved guidance, escalates uncertainty, and records each decision.](/images/complaintflow-architecture.svg)

1. **Validate:** reject missing IDs and overlong text.
2. **Protect:** redact obvious email, phone, and account-like values before provider use.
3. **Baseline:** classify with transparent keywords so there is always a simple fallback.
4. **Retrieve:** select only approved playbooks for the predicted queue.
5. **Assist:** call a provider through an interface that can support a local model or approved LLM gateway.
6. **Validate:** reject unsupported queues, invalid confidence, or empty summaries.
7. **Escalate:** route low-confidence, unknown, or missing-narrative cases to a human.
8. **Persist:** record the decision, confidence, citations, provider, latency, and escalation reason.

## Key findings

The bounded workflow validates inputs, protects personal data, retrieves approved guidance, makes uncertainty visible, and records enough evidence for review. The local reference fixture achieved perfect routing and citation coverage, but that result is a contract test, not a production accuracy claim.

## Recommendation

Start in shadow mode. Roll out only if a privacy-reviewed holdout shows equal or better routing accuracy and escalation recall than the baseline, with acceptable latency, cost, and unsafe-output rates.

## What internal data would improve the decision

Real reviewer labels, queue outcomes, resolution time, customer satisfaction, language, attachments, privacy incidents, and provider cost would show whether the workflow improves support operations safely.

## Technical design

### Why a hybrid system?

A pure LLM answer is difficult to audit and can invent policy. A keyword-only system is transparent but weak on language variation. The hybrid design keeps the baseline and approved retrieval visible while allowing a stronger provider to improve language understanding.

### Why retrieval instead of free-form advice?

The service retrieves a small, approved playbook and returns its source identifier. This narrows the answer space and gives reviewers something concrete to inspect. Retrieval is not proof that a playbook applies; confidence and human review remain part of the contract.

### Why SQLite for the reference implementation?

SQLite is enough to demonstrate persistence and audit fields without adding an operational database dependency. A production deployment would move this table to a managed database with encryption, access control, retention, and backup policies.

### Evaluation

The repository includes a labeled fixture and an evaluation script that compares the transparent keyword baseline with the service. It measures macro-F1, recall by queue, escalation recall for unknown cases, citation coverage, latency, fallback behavior, and performance on standard, paraphrase, short, unknown, and PII slices.

On the expanded **20-case reference fixture**, the local service achieved **1.00 macro-F1**, **1.00 recall for each supported queue**, **1.00 escalation recall for unknown cases**, and **100% citation coverage for routed cases**. It also reports slice-level accuracy and escalation count so a perfect aggregate score cannot hide a failure on short or redacted inputs. These results show that the checked-in contract works; they are not production performance claims because the fixture is small, synthetic, and built from hand-written examples.

### Reliability and failure handling

- Provider failures retry twice with backoff.
- If retries fail, the service returns transparent baseline routing instead of an invented answer.
- Unsupported provider queues are rejected and use the same transparent fallback.
- Empty narratives escalate without a model call.
- Unknown queues and low confidence escalate.
- The test suite covers correct routing, missing text, PII redaction, unknown issues, deterministic baseline behavior, retry handling, invalid provider output, fallback routing, and audit persistence.

### Cost and latency

The local reference provider has no API cost and measured sub-millisecond fixture latency. A hosted model would add token cost and network latency. Before rollout, the team should measure p50/p95 latency, input/output tokens, cost per case, retry rate, and the percentage of cases that can safely use the cheaper baseline.

### Security and responsible AI

Complaint narratives may contain personal information. Redaction is applied before provider use, but it is not a complete privacy guarantee. Production controls must include encryption, least-privilege access, retention limits, provider data-use review, audit monitoring, and a process for correcting or deleting records.

The system must not make lending, refund, legal, or regulatory decisions. It assists a human support workflow and makes uncertainty visible.

The privacy evidence is also deliberately limited. The tests prove that common email, phone, and account-like patterns are redacted before the local summary is created. They do not prove that every identifier, free-text indirect identifier, attachment, log, provider, or database backup is safe. That requires a privacy review, representative red-team examples, retention checks, and provider contract review.

### Rollout and measurement plan

Start in shadow mode: generate recommendations without changing routing. Measure reviewer agreement, queue accuracy, escalation recall, latency, cost, and unsafe-output rate. Move to a small assisted cohort only if the system matches or beats the baseline on a time-based, privacy-reviewed holdout. Keep a control group and monitor product, state, company, language, and narrative-length slices.

## Key takeaway

The public complaint database is not representative of all consumers, and the checked-in fixture is intentionally small. The next engineering step is a privacy-reviewed sample of real narratives with reviewer labels, followed by a stronger model comparison, calibration, drift monitoring, and managed persistence.

## Technical appendix

Code: [ComplaintFlow reference implementation](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/ai_engineering/complaintflow)

Research and design: [AI Engineer project research](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/ai-engineer-project-research-2026-08.md) and [ComplaintFlow design](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/ai-engineer-complaintflow-design-2026-08.md).
