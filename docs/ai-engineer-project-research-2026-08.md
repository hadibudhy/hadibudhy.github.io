# AI Engineer project research

Research date: 2026-08-15

The selection criteria were business value, AI engineering depth, evaluation potential, uniqueness, data access, and recruiter readability.

| Candidate | Business problem | AI solution | Engineering depth | Evaluation potential | Business value | Uniqueness | Main risk | Score |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | ---: |
| CFPB consumer complaint triage | Route financial complaints to the right product/issue queue and suggest a safe next step | Hybrid text classifier, retrieval over approved playbooks, confidence-based escalation | 10 | 10 | 10 | 8 | Narratives are incomplete and not representative of all consumers | 48/50 |
| FAA Service Difficulty Report assistant | Help maintenance teams find similar aircraft defects and required follow-up | Metadata filtering plus grounded retrieval over defect reports | 9 | 9 | 10 | 9 | Safety domain requires strict human approval and source traceability | 46/50 |
| FCC consumer complaint routing | Prioritize unwanted-call/message complaints and identify recurring patterns | Text classification, entity extraction, and retrieval over response guidance | 8 | 9 | 9 | 8 | Informal complaints are not a complete view of harm | 43/50 |
| Open Contracting bid review assistant | Help procurement teams compare tenders, risks, and missing information | Document extraction, retrieval, rule checks, and structured summaries | 10 | 8 | 9 | 9 | Public contract documents vary widely by country and format | 45/50 |
| Public GitHub/Jira issue triage | Reduce engineering support backlog by routing and summarizing tickets | Classification, duplicate detection, retrieval over runbooks, and human review | 9 | 9 | 8 | 7 | Public issues may not reflect private enterprise workflows | 42/50 |

## Selected project

**ComplaintFlow: a reliable complaint-triage and response-assistance service for financial support teams.**

The CFPB publishes complaint records and, where consumers opt in and privacy review is complete, narrative descriptions. The Bureau says the data is freely available, generally updates daily, and is not a representative sample of all consumer experiences. Those constraints make it a strong engineering case: the system must be useful while clearly separating routing assistance from a verified customer outcome.

## Decision and system boundary

The decision owner is a support operations manager. The decision is which queue should receive a complaint, whether the system has enough evidence to suggest a playbook, and when a human must review it. The system never makes a credit, legal, refund, or regulatory decision.

The primary business measures are correct queue routing and time saved per case. Guardrails are unsupported-answer rate, sensitive-data exposure, escalation recall, latency, and cost per complaint.

## Planned evaluation

The first baseline is a TF-IDF plus logistic-regression classifier. The production path adds a retrieval layer and a provider adapter with structured output validation. Evaluation will compare baseline and AI-assisted routing on a held-out, time-aware split, report macro-F1 and high-risk recall, test retrieval precision, measure abstention, and include adversarial cases such as empty narratives, prompt injection, and unsupported product claims.

## Sources

- [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
- [CFPB API field reference](https://cfpb.github.io/api/ccdb/fields.html)
- [FAA Service Difficulty Reports](https://www.faa.gov/av-info/download_SDR)
- [FCC Consumer Complaints Data](https://opendata.fcc.gov/Consumer/CGB-Consumer-Complaints-Data/3xyp-aqkj)
- [Open Contracting Data Registry](https://data.open-contracting.org/)
- [GitHub issue-report research dataset](https://arxiv.org/abs/2303.09236)
