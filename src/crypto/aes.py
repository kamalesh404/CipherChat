"""AES-GCM symmetric encryption with HKDF-derived keys."""

from __future__ import annotations

import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def derive_key(shared_secret: bytes, info: bytes = b"cipherchat-aes") -> bytes:
    """HKDF-SHA256 derive 32-byte AES key from ECDH secret."""
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=info)
    return hkdf.derive(shared_secret)


def encrypt(key: bytes, plaintext: bytes, associated: bytes | None = None) -> bytes:
    """Encrypt with AES-GCM. Returns nonce(12) + ciphertext + tag."""
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, plaintext, associated)
    return nonce + ct


def decrypt(key: bytes, data: bytes, associated: bytes | None = None) -> bytes:
    """Decrypt nonce+ciphertext. Raises if tag invalid."""
    nonce, ct = data[:12], data[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, associated)
