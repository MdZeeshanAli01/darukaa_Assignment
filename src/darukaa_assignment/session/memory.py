from __future__ import annotations

from collections import defaultdict


class SessionMemory:
    def __init__(self) -> None:
        self.store: dict[str, dict[str, object]] = defaultdict(dict)

    def get_session(self, session_id: str) -> dict[str, object]:
        return self.store.setdefault(session_id, {})

    def update_metrics(self, session_id: str, **metrics: object) -> None:
        session = self.get_session(session_id)
        session.update(metrics)

    def get_last_messages(self, session_id: str, limit: int = 5) -> list[str]:
        session = self.get_session(session_id)
        history = session.get("history", [])
        if not isinstance(history, list):
            return []
        return history[-limit:]

    def add_message(self, session_id: str, message: str) -> None:
        session = self.get_session(session_id)
        history = session.setdefault("history", [])
        if not isinstance(history, list):
            history = []
        history.append(message)
        session["history"] = history
