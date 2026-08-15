from dataclasses import dataclass

from .redact import redact
from .schemas import Complaint, Queue


KEYWORDS: dict[Queue, tuple[str, ...]] = {
    "credit_reporting": ("credit report", "credit bureau", "equifax", "transunion", "experian"),
    "card_payments": ("credit card", "debit card", "charge", "transaction", "payment"),
    "mortgages": ("mortgage", "foreclosure", "home loan", "escrow"),
    "banking": ("bank account", "checking", "savings", "deposit", "wire transfer"),
}


@dataclass(frozen=True)
class BaselineResult:
    queue: Queue
    confidence: float


def classify(complaint: Complaint) -> BaselineResult:
    text = redact(complaint.text).lower()
    scores = {queue: sum(term in text for term in terms) for queue, terms in KEYWORDS.items()}
    queue, score = max(scores.items(), key=lambda pair: pair[1])
    if score == 0:
        return BaselineResult("other", 0.2)
    total = sum(scores.values()) or 1
    return BaselineResult(queue, min(0.95, 0.45 + score / total * 0.5))

