"""Pydantic models for API and storage."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-z0-9_]+$")
    public_key: str  # hex of 32-byte X25519 pub


class RegisterResponse(BaseModel):
    username: str
    public_key: str


class UserRecord(BaseModel):
    username: str
    public_key: str  # hex


class HandshakeRequest(BaseModel):
    sender: str
    recipient: str
    ephemeral_pub: str  # hex


class MessageEnvelope(BaseModel):
    sender: str
    recipient: str
    nonce_ct: str  # hex of nonce+ciphertext
    msg_no: int


class WSMessage(BaseModel):
    type: Literal["handshake", "message", "error", "ack"]
    payload: dict
