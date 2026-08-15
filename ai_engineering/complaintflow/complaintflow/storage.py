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
