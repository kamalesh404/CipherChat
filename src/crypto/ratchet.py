"""Simple Double Ratchet for forward secrecy."""

from __future__ import annotations

import hashlib
import hmac
import os


def _hkdf_rk(rk: bytes, dh_out: bytes) -> tuple[bytes, bytes]:
    """Ratchet root key with DH output -> (new_rk, chain_key)."""
    okm = hmac.new(rk, dh_out, hashlib.sha256).digest()
    # okm is 32 bytes; derive chain key from it
    ck = hmac.new(okm, b"chain", hashlib.sha256).digest()
    return okm, ck


def _kdf_ck(ck: bytes) -> tuple[bytes, bytes]:
    """Chain key -> (next_ck, message_key)."""
    mk = hmac.new(ck, b"\x01", hashlib.sha256).digest()
    next_ck = hmac.new(ck, b"\x02", hashlib.sha256).digest()
    return next_ck, mk


class Ratchet:
    """Minimal symmetric ratchet with DH rotation support."""

    def __init__(self, root_key: bytes, chain_key: bytes | None = None) -> None:
        self.rk = root_key
        self.ck = chain_key or hmac.new(root_key, b"init-chain", hashlib.sha256).digest()
        self.msg_no = 0

    def next_message_key(self) -> bytes:
        """Advance chain and return message key."""
        self.ck, mk = _kdf_ck(self.ck)
        self.msg_no += 1
        return mk

    def dh_ratchet(self, dh_out: bytes) -> None:
        """Rotate root and chain keys with new DH output."""
        self.rk, self.ck = _hkdf_rk(self.rk, dh_out)
        self.msg_no = 0
