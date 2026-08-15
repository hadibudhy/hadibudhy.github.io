import json
from pathlib import Path

from .schemas import Playbook, Queue


class PlaybookStore:
    def __init__(self, path: str | Path):
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        self.playbooks = [Playbook(**item) for item in payload]

    def retrieve(self, queue: Queue, text: str, limit: int = 2) -> list[Playbook]:
        words = set(text.lower().split())
        candidates = [book for book in self.playbooks if book.queue == queue]
        ranked = sorted(candidates, key=lambda book: sum(term in words for term in book.keywords), reverse=True)
        return ranked[:limit]

