"""Additional crypto test: X3DH handshake produces same secret."""

from src.crypto.handshake import x3dh_initiator, x3dh_responder
from src.crypto.keys import generate_keypair


def test_x3dh_shared():
    a_priv, a_pub = generate_keypair()
    a_eph_priv, a_eph_pub = generate_keypair()
    b_priv, b_pub = generate_keypair()
    s1 = x3dh_initiator(a_priv, a_eph_priv, b_pub)
    s2 = x3dh_responder(b_priv, a_pub, a_eph_pub)
    assert s1 == s2
