# ComplaintFlow design

## Decision

Support operations needs a first-pass queue recommendation and a safe, sourced playbook suggestion. A human remains responsible for the final customer response and any regulated action.

## Architecture

The service is a small FastAPI application with six explicit stages: input validation, PII redaction, transparent baseline routing, approved-playbook retrieval, provider response validation with retries, and SQLite persistence. The provider is an interface so an approved LLM gateway can be substituted without changing the business policy or evaluation harness.

## Reliability contract

- Empty narratives are escalated immediately.
- Inputs have length limits.
- Obvious email, phone, and account-like values are redacted before provider use.
- Provider failures retry twice with backoff, then fall back to the baseline classifier.
- Unsupported queues, invalid confidence values, or empty summaries are rejected.
- Every decision records confidence, provider, latency, citations, and escalation reason.

## Evaluation contract

The baseline is keyword routing. The service is evaluated on a labeled fixture for macro-F1, high-risk escalation recall, citation coverage, latency, and fallback behavior. A production rollout would require a time-based holdout of real, privacy-reviewed complaints, reviewer agreement, calibration, slice metrics, and drift monitoring.

## Security and responsible AI

The system does not request secrets, makes no eligibility decision, and never treats a retrieved playbook as authority beyond its approved scope. PII redaction is defense-in-depth rather than a guarantee. Access control, encryption, retention, audit review, and provider data-use terms are deployment requirements.
