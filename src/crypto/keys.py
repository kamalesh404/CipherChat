"""X25519 key generation and ECDH."""

from __future__ import annotations

import os

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives import serialization


def generate_keypair() -> tuple[bytes, bytes]:
    """Generate X25519 private and public key bytes."""
    private = X25519PrivateKey.generate()
    priv_bytes = private.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_bytes = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return priv_bytes, pub_bytes


def ecdh(priv_bytes: bytes, pub_bytes: bytes) -> bytes:
    """Perform ECDH and return 32-byte shared secret."""
    private = X25519PrivateKey.from_private_bytes(priv_bytes)
    public = X25519PublicKey.from_public_bytes(pub_bytes)
    return private.exchange(public)


def pub_from_priv(priv_bytes: bytes) -> bytes:
    """Derive public key from private."""
    private = X25519PrivateKey.from_private_bytes(priv_bytes)
    return private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
