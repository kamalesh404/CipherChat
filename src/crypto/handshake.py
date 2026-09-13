"""X3DH-like handshake: combine long-term and ephemeral ECDH."""

from __future__ import annotations

from src.crypto.keys import ecdh


def x3dh_initiator(
    initiator_priv: bytes,
    initiator_eph_priv: bytes,
    responder_pub: bytes,
    responder_eph_pub: bytes | None = None,
) -> bytes:
    """Initiator combines DHs to derive shared secret."""
    dh1 = ecdh(initiator_priv, responder_pub)
    dh2 = ecdh(initiator_eph_priv, responder_pub)
    # If responder has ephemeral, include it for forward secrecy
    if responder_eph_pub is not None:
        dh3 = ecdh(initiator_eph_priv, responder_eph_pub)
        return dh1 + dh2 + dh3
    return dh1 + dh2


def x3dh_responder(
    responder_priv: bytes,
    initiator_pub: bytes,
    initiator_eph_pub: bytes,
) -> bytes:
    """Responder derives same secret."""
    dh1 = ecdh(responder_priv, initiator_pub)
    dh2 = ecdh(responder_priv, initiator_eph_pub)
    return dh1 + dh2
