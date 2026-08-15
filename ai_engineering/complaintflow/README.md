# ComplaintFlow

ComplaintFlow is a production-oriented reference service for routing financial consumer complaints to the right support queue and retrieving an approved response playbook.

It is deliberately bounded. It does not decide refunds, credit, legal outcomes, regulatory violations, or customer eligibility. Low-confidence or sensitive cases are escalated to a human.

## Run locally

```bash
python -m venv .venv
\.venv\Scripts\activate
pip install fastapi uvicorn pytest
uvicorn complaintflow.api:app --reload
```

The API writes an audit database to `complaintflow.db` by default. Set `COMPLAINTFLOW_DB_PATH` to use a managed or mounted SQLite path in deployment. Then send a request:

```bash
curl -X POST http://127.0.0.1:8000/triage \
  -H "content-type: application/json" \
  -d '{"complaint_id":"demo-1","text":"I do not recognize this credit card charge and need help disputing it."}'
```

## Design

1. Normalize and redact obvious email, phone, and account-like values.
2. Run a transparent keyword baseline.
3. Run the structured triage policy and retrieve only approved playbooks.
4. Validate the response schema, retry transient provider failures, and fall back to the baseline.
5. Persist the request, decision, confidence, citations, and escalation reason in SQLite.

The provider interface can be connected to an approved LLM gateway later. The default local provider is deterministic, so tests and evaluation do not depend on network access or a paid API.

## Evaluation

```bash
python -m evaluation.evaluate
pytest -q
```

The evaluation compares the keyword baseline with the structured service on a labeled fixture. Metrics include macro-F1, escalation recall, citation coverage, latency, and fallback behavior. The fixture is intentionally small and synthetic; it demonstrates the evaluation contract, not production performance.
