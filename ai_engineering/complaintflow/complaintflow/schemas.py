from dataclasses import dataclass, field
from typing import Literal

Queue = Literal["credit_reporting", "card_payments", "mortgages", "banking", "other"]


@dataclass(frozen=True)
class Complaint:
    complaint_id: str
    text: str
    product: str | None = None
    issue: str | None = None


@dataclass(frozen=True)
class Playbook:
    playbook_id: str
    title: str
    queue: Queue
    keywords: tuple[str, ...]
    steps: tuple[str, ...]
    source: str


@dataclass
class TriageDecision:
    complaint_id: str
    queue: Queue
    confidence: float
    summary: str
    playbook_id: str | None
    citations: list[str] = field(default_factory=list)
    escalated: bool = False
    escalation_reason: str | None = None
    provider: str = "local"
    latency_ms: float = 0.0

