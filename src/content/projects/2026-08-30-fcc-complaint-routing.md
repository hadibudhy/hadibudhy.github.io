---
title: "FCC Complaints: Use AI to Organize Consumer Issues Without Treating Allegations as Verified Facts"
date: 2026-08-30
categories: [applied AI]
tags: [NLP, complaint routing, classification, governance]
excerpt: "An AI-assisted complaint-routing study that combines transparent taxonomy, confidence thresholds, and human review for public telecom complaints."
problem: "A consumer-support organization receives complaints spanning billing, service quality, equipment, and privacy, but manual routing is slow and the complaint text is not independently verified."
result: "The FCC publishes individual informal consumer complaints beginning in October 2014; the dataset supports taxonomy and routing analysis while the agency warns that allegations are selected by consumers and not verified by the FCC."
published: true
---

## Business question

Which complaint categories can be routed automatically for faster handling, and which require human review because the text is ambiguous, sensitive, or high-risk?

## Why it matters

Routing errors delay resolution and can send a consumer’s sensitive issue to the wrong team. Treating an allegation as established fact can also create unfair provider or product conclusions.

## Decision brief

- **Recommendation:** use a transparent multi-label taxonomy and confidence-based routing; keep sensitive, novel, and low-confidence cases human-reviewed.
- **Evidence:** the [FCC Consumer Complaints dataset](https://catalog.data.gov/dataset/cgb-consumer-complaints-data) contains individual informal complaints filed with the Consumer Help Center beginning October 31, 2014.
- **Evidence strength:** Moderate for workflow and taxonomy discovery; low for prevalence or provider-quality claims because consumers select what to report and the FCC does not verify allegations.
- **Main risk:** class imbalance, changing issue names, PII in narratives, and feedback loops from past routing decisions.
- **Next test:** evaluate on a time-based reviewer-labeled sample and measure class recall, escalation, time-to-queue, and correction rate.

## Role

Role: text-field review, taxonomy design, privacy boundary, baseline classification, evaluation slice design, and responsible AI rollout planning.

## Data used

The source is the [FCC CGB Consumer Complaints Data](https://catalog.data.gov/dataset/cgb-consumer-complaints-data). It includes complaint records and issue-related fields; the catalog states that the data represents information selected by the consumer and that the FCC does not verify the facts alleged.

The project treats the data as routing evidence. It does not treat a complaint as proof that a provider caused a problem or that all customers experienced it.

## Approach

1. Remove or mask direct identifiers and restrict narrative access by role.
2. Freeze a taxonomy version and map source issue values to stable queue labels.
3. Establish a transparent keyword/linear baseline before using embeddings or an LLM.
4. Evaluate on a chronological, reviewer-labeled sample with rare and sensitive slices.
5. Escalate uncertain, novel, or high-impact cases and log the evidence used for routing.

## Key findings

## Visual evidence

### Context: FCC complaints are individual informal reports

![FCC complaint source scope: complaints from October 31, 2014 onward, one complaint grain, issue fields, and an unverified-allegation boundary](/images/portfolio-fcc-complaint-scope.svg)

The source is useful for queue design, not a denominator of provider experience.

### Main finding: routing evidence and prevalence evidence are different

![FCC evidence boundary: issue and provider context are observed, while representative prevalence, verified fault, and resolution quality are not](/images/portfolio-fcc-boundary.svg)

This is why the project avoids provider rankings.

### Decision: confidence-based routing keeps a human path

![Conceptual FCC complaint workflow: redact complaint text, suggest a cited queue, and escalate low-confidence or sensitive cases](/images/portfolio-fcc-routing.svg)

The visual makes escalation a product outcome, not a model failure.

### Complaint volume is not provider failure rate

The dataset records people who chose to file an informal complaint.

**Meaning:** a high count can reflect exposure, reporting propensity, or a temporary campaign, not only poor service.

**Why it matters:** use the data to prioritize service review, not publish unadjusted provider rankings.

### Taxonomy drift is an operational risk

Issue labels and product language can change over time.

**Meaning:** a model trained on old labels can route new complaints incorrectly even if its historical score was strong.

**Why it matters:** monitor unknown-label and correction rates and version the taxonomy.

### Escalation is part of the product, not a model failure

Some cases are too ambiguous or sensitive to automate safely.

**Meaning:** the right system maximizes useful routing while preserving a human path.

**Why it matters:** report automated coverage and human-review quality together.

## Evidence register

| Layer | Evidence | Decision use |
|---|---|---|
| Observed | FCC records contain selected informal complaints and issue/provider fields; the FCC does not verify allegations | Build and monitor a routing taxonomy |
| Inferred | Confidence-based routing with escalation can improve queue handling | Start in shadow mode with human review |
| Not established | Complaint counts are provider failure rates, or automated routing resolves the issue | Avoid public rankings and measure corrections |

## Validation record

- **Grain:** one informal complaint; narrative and structured fields remain linked.
- **Checks:** direct identifiers/PII, source-label drift, time split, rare categories, reviewer labels, and correction outcomes are reviewed.
- **Guardrail:** low-confidence, sensitive, and novel cases always have a human path.

## Recommendation

**What:** launch a shadow-mode router that suggests a queue and cites the source fields used.

**Where / who:** start with high-volume, low-sensitivity categories; exclude PII-heavy and novel cases until privacy and reviewer policy are approved.

**Why:** a transparent baseline creates a measurable workflow improvement without making unsupported factual claims.

**Risk:** feedback loops can reinforce the first routing decision and hide emerging categories.

**Next test:** compare assisted and manual routing with time-to-queue, correction, escalation, and complaint-resolution guardrails.

## Evidence strength and limitations

This is a workflow and taxonomy study, not a provider-performance analysis. Public complaints are not a representative sample, facts are not verified, and narratives may contain personal information. Production quality requires reviewer labels, access controls, drift monitoring, and a retention policy.

## Reproducibility

Source and field metadata: [FCC CGB Consumer Complaints Data](https://catalog.data.gov/dataset/cgb-consumer-complaints-data). The [portfolio expansion validation record](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/portfolio-expansion-2026-08.md) records the source boundary and evaluation contract.

## Technical appendix

The baseline should report macro recall, per-queue recall, escalation rate, correction rate, and calibration. A model must not be trained on post-routing labels without a time split, and every generated explanation must be traceable to the original complaint fields.
