"""Simple JSON file store for users and offline messages."""

from __future__ import annotations

import json
import os
from typing import Dict, List

from src.core.models import UserRecord, MessageEnvelope


class Store:
    """Persists users and queued envelopes to a JSON file."""

    def __init__(self, path: str = ".cipherchat/db.json") -> None:
        self.path = path
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        self._data: Dict[str, object] = {"users": {}, "queues": {}}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as fh:
                self._data = json.load(fh)

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self._data, fh, indent=2)

    # Users
    def add_user(self, rec: UserRecord) -> None:
        self._data["users"][rec.username] = rec.model_dump()
        self._save()

    def get_user(self, username: str) -> UserRecord | None:
        raw = self._data["users"].get(username)
        return UserRecord(**raw) if raw else None

    def list_users(self) -> List[UserRecord]:
        return [UserRecord(**v) for v in self._data["users"].values()]

    # Queues
    def enqueue(self, env: MessageEnvelope) -> None:
        q = self._data["queues"].setdefault(env.recipient, [])
        q.append(env.model_dump())
        self._save()

    def dequeue_all(self, username: str) -> List[MessageEnvelope]:
        raw = self._data["queues"].pop(username, [])
        self._save()
        return [MessageEnvelope(**r) for r in raw]
