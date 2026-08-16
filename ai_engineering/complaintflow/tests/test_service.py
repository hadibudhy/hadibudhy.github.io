from pathlib import Path

from complaintflow.baseline import classify
from complaintflow.schemas import Complaint
from complaintflow.service import TriageService
from complaintflow.provider import LocalProvider, ProviderError, RetryingProvider
from complaintflow.retrieval import PlaybookStore
from complaintflow.storage import DecisionStore


ROOT = Path(__file__).parents[1]


def make_service() -> TriageService:
    return TriageService(PlaybookStore(ROOT / "data" / "playbooks.json"), DecisionStore(), LocalProvider())


def test_routes_and_cites_approved_playbook():
    result = make_service().triage(Complaint("1", "I do not recognize this credit card charge."))
    assert result.queue == "card_payments"
    assert result.playbook_id == "card-unauthorized-charge"
    assert result.citations == ["internal://playbooks/card-unauthorized-charge"]
    assert not result.escalated


def test_missing_narrative_escalates_without_model_call():
    result = make_service().triage(Complaint("2", ""))
    assert result.escalated
    assert result.escalation_reason == "missing_narrative"
    assert result.queue == "other"


def test_redacts_phone_before_summary():
    result = make_service().triage(Complaint("3", "Call 555-010-2020 about my credit report."))
    assert "555-010-2020" not in result.summary
    assert "REDACTED" in result.summary


def test_unknown_issue_is_escalated():
    result = make_service().triage(Complaint("4", "Something unusual happened and I need help."))
    assert result.queue == "other"
    assert result.escalated


def test_baseline_is_deterministic():
    complaint = Complaint("5", "My bank checking account transfer is missing.")
    assert classify(complaint) == classify(complaint)


def test_provider_retries_transient_failure():
    class Flaky:
        name = "flaky"
        calls = 0

        def triage(self, complaint, playbooks):
            self.calls += 1
            if self.calls == 1:
                raise TimeoutError("temporary")
            return "banking", "retried", 0.8

    provider = Flaky()
    result = RetryingProvider(provider, attempts=2).triage(Complaint("6", "bank account"), [])
    assert result[0] == "banking"
    assert provider.calls == 2


def test_invalid_provider_queue_uses_transparent_baseline():
    class InvalidProvider:
        name = "invalid"

        def triage(self, complaint, playbooks):
            return "unsupported_queue", "unsafe answer", 0.99

    service = TriageService(PlaybookStore(ROOT / "data" / "playbooks.json"), DecisionStore(), InvalidProvider())
    result = service.triage(Complaint("7", "My checking account transfer is missing."))
    assert result.queue == "banking"
    assert result.summary == "Provider unavailable; returned transparent baseline routing."


def test_provider_failure_uses_baseline_without_losing_audit_record():
    class BrokenProvider:
        name = "broken"

        def triage(self, complaint, playbooks):
            raise ProviderError("gateway unavailable")

    store = DecisionStore()
    service = TriageService(PlaybookStore(ROOT / "data" / "playbooks.json"), store, BrokenProvider())
    result = service.triage(Complaint("8", "The bank froze my checking account."))
    assert result.queue == "banking"
    assert result.summary == "Provider unavailable; returned transparent baseline routing."
    assert store.get("8") == result
