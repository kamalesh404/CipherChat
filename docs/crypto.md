# Crypto Design

- **X25519**: 32-byte ECDH, `cryptography` lib
- **HKDF-SHA256**: derives 32-byte AES key from shared secret
- **AES-GCM**: 12-byte nonce, tag verified on decrypt
- **Ratchet**: `Ratchet` class advances chain key per message, rotates root on DH
- **Handshake**: X3DH-like combines long-term + ephemeral DHs
