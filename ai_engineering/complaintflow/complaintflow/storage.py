import json
import sqlite3
from threading import Lock
from pathlib import Path

from .schemas import TriageDecision


class DecisionStore:
    def __init__(self, path: str | Path = ":memory:"):
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.lock = Lock()
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS triage_decisions (
                complaint_id TEXT PRIMARY KEY,
                queue TEXT NOT NULL,
                confidence REAL NOT NULL,
                summary TEXT NOT NULL,
                playbook_id TEXT,
                citations TEXT NOT NULL,
                escalated INTEGER NOT NULL,
                escalation_reason TEXT,
                provider TEXT NOT NULL,
                latency_ms REAL NOT NULL
            )"""
        )
        self.connection.commit()

    def save(self, decision: TriageDecision) -> None:
        with self.lock:
            self.connection.execute(
                """INSERT OR REPLACE INTO triage_decisions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (decision.complaint_id, decision.queue, decision.confidence, decision.summary,
                 decision.playbook_id, json.dumps(decision.citations), int(decision.escalated),
                 decision.escalation_reason, decision.provider, decision.latency_ms),
            )
            self.connection.commit()

    def get(self, complaint_id: str) -> TriageDecision | None:
        with self.lock:
            row = self.connection.execute(
                "SELECT complaint_id, queue, confidence, summary, playbook_id, citations, escalated, escalation_reason, provider, latency_ms FROM triage_decisions WHERE complaint_id = ?",
                (complaint_id,),
            ).fetchone()
        if row is None:
            return None
        return TriageDecision(
            complaint_id=row[0],
            queue=row[1],
            confidence=row[2],
            summary=row[3],
            playbook_id=row[4],
            citations=json.loads(row[5]),
            escalated=bool(row[6]),
            escalation_reason=row[7],
            provider=row[8],
            latency_ms=row[9],
        )
