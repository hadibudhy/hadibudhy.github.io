from dataclasses import dataclass
import time
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from typing import Protocol

from .baseline import classify
from .redact import redact
from .schemas import Complaint, Playbook, Queue


class ProviderError(RuntimeError):
    pass


class TriageProvider(Protocol):
    name: str

    def triage(self, complaint: Complaint, playbooks: list[Playbook]) -> tuple[Queue, str, float]: ...


@dataclass
class LocalProvider:
    """Deterministic local provider used in tests and as a safe offline fallback."""

    name: str = "local"

    def triage(self, complaint: Complaint, playbooks: list[Playbook]) -> tuple[Queue, str, float]:
        result = classify(complaint)
        safe_text = redact(complaint.text).strip()
        summary = safe_text[:180] + ("…" if len(safe_text) > 180 else "")
        return result.queue, summary, result.confidence


@dataclass
class RetryingProvider:
    """Retry transient provider failures, then let the service use its baseline fallback."""

    inner: TriageProvider
    attempts: int = 2
    backoff_seconds: float = 0.01

    @property
    def name(self) -> str:
        return self.inner.name

    def triage(self, complaint: Complaint, playbooks: list[Playbook]) -> tuple[Queue, str, float]:
        last_error: Exception | None = None
        for attempt in range(self.attempts):
            try:
                return self.inner.triage(complaint, playbooks)
            except (ProviderError, TimeoutError) as error:
                last_error = error
                if attempt + 1 < self.attempts:
                    time.sleep(self.backoff_seconds * (attempt + 1))
        raise ProviderError("provider failed after retries") from last_error


@dataclass
class JsonGatewayProvider:
    """Small provider adapter for an approved internal JSON/LLM gateway.

    The gateway must return: {"queue": str, "summary": str, "confidence": number}.
    The adapter keeps provider-specific transport outside the business service.
    """

    endpoint: str
    api_key: str
    model: str = "approved-triage-model"
    timeout_seconds: float = 8.0
    name: str = "json-gateway"

    def triage(self, complaint: Complaint, playbooks: list[Playbook]) -> tuple[Queue, str, float]:
        payload = {
            "model": self.model,
            "task": "route_complaint_with_grounded_summary",
            "complaint": {"id": complaint.complaint_id, "text": redact(complaint.text)},
            "playbooks": [{"id": book.playbook_id, "title": book.title, "steps": book.steps} for book in playbooks],
            "output_schema": {"queue": "string", "summary": "string", "confidence": "number"},
        }
        request = Request(self.endpoint, data=json.dumps(payload).encode(), method="POST", headers={
            "content-type": "application/json", "authorization": f"Bearer {self.api_key}",
        })
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                result = json.loads(response.read().decode())
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            raise ProviderError("gateway request failed") from error
        try:
            return result["queue"], result["summary"], float(result["confidence"])
        except (KeyError, TypeError, ValueError) as error:
            raise ProviderError("gateway returned an invalid response") from error
