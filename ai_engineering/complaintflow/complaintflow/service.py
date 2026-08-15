import time
from pathlib import Path

from .baseline import classify
from .provider import LocalProvider, ProviderError, RetryingProvider, TriageProvider
from .redact import redact
from .retrieval import PlaybookStore
from .schemas import Complaint, TriageDecision
from .storage import DecisionStore


class TriageService:
    def __init__(self, playbooks: PlaybookStore, store: DecisionStore, provider: TriageProvider, min_confidence: float = 0.62):
        self.playbooks = playbooks
        self.store = store
        self.provider = provider
        self.min_confidence = min_confidence

    def triage(self, complaint: Complaint) -> TriageDecision:
        started = time.perf_counter()
        text = redact(complaint.text).strip()
        if not text:
            decision = TriageDecision(complaint.complaint_id, "other", 0.0, "No narrative supplied.", None,
                                      escalated=True, escalation_reason="missing_narrative")
            self.store.save(decision)
            return decision
        safe_complaint = Complaint(complaint.complaint_id, text, complaint.product, complaint.issue)
        baseline = classify(safe_complaint)
        books = self.playbooks.retrieve(baseline.queue, text)
        try:
            queue, summary, confidence = self.provider.triage(safe_complaint, books)
            if queue not in {"credit_reporting", "card_payments", "mortgages", "banking", "other"}:
                raise ProviderError("provider returned an unsupported queue")
            confidence = max(0.0, min(1.0, float(confidence)))
            summary = str(summary).strip() or "No supported summary returned."
        except (ProviderError, TimeoutError):
            queue, confidence = baseline.queue, baseline.confidence
            summary = "Provider unavailable; returned transparent baseline routing."
        escalated = confidence < self.min_confidence or queue == "other"
        reason = "low_confidence_or_unknown_queue" if escalated else None
        decision = TriageDecision(
            complaint.complaint_id, queue, confidence, summary,
            books[0].playbook_id if books else None,
            [book.source for book in books], escalated, reason, self.provider.name,
            (time.perf_counter() - started) * 1000,
        )
        self.store.save(decision)
        return decision


def default_service(db_path: str = ":memory:") -> TriageService:
    root = Path(__file__).resolve().parents[1]
    return TriageService(PlaybookStore(root / "data" / "playbooks.json"), DecisionStore(db_path), RetryingProvider(LocalProvider()))
