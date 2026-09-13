"""Tests for crypto primitives."""

from src.crypto.aes import decrypt, derive_key, encrypt
from src.crypto.keys import ecdh, generate_keypair, pub_from_priv
from src.crypto.ratchet import Ratchet


def test_ecdh_shared():
    priv_a, pub_a = generate_keypair()
    priv_b, pub_b = generate_keypair()
    s1 = ecdh(priv_a, pub_b)
    s2 = ecdh(priv_b, pub_a)
    assert s1 == s2
    assert len(s1) == 32


def test_pub_from_priv():
    priv, pub = generate_keypair()
    assert pub_from_priv(priv) == pub


def test_aes_roundtrip():
    priv_a, pub_a = generate_keypair()
    priv_b, pub_b = generate_keypair()
    shared = ecdh(priv_a, pub_b)
    key = derive_key(shared)
    ct = encrypt(key, b"hello world")
    pt = decrypt(key, ct)
    assert pt == b"hello world"


def test_aes_associated():
    key = b"0" * 32
    ct = encrypt(key, b"hi", associated=b"aad")
    assert decrypt(key, ct, associated=b"aad") == b"hi"


def test_ratchet_forward():
    rk = b"r" * 32
    r = Ratchet(rk)
    k1 = r.next_message_key()
    k2 = r.next_message_key()
    assert k1 != k2


def test_ratchet_dh():
    rk = b"r" * 32
    r1 = Ratchet(rk)
    k1 = r1.next_message_key()
    r1.dh_ratchet(b"dh" * 16)
    k2 = r1.next_message_key()
    assert k1 != k2
