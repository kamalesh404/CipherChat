"""Configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Config:
    host: str = "127.0.0.1"
    port: int = 8080
    db_path: str = ".cipherchat/db.json"

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            host=os.environ.get("CIPHERC_HOST", "127.0.0.1"),
            port=int(os.environ.get("CIPHERC_PORT", "8080")),
            db_path=os.environ.get("CIPHERC_DB", ".cipherchat/db.json"),
        )
