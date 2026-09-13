<div align="center">

# 🔐 CipherChat

**End-to-end encrypted chat — X25519 + AES-GCM + Double Ratchet**

[![License: MIT](https://img.shields.io/badge/License-MIT-00C853?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![E2E](https://img.shields.io/badge/E2E-AES--GCM-FF6F00?style=for-the-badge&logo=letsencrypt&logoColor=white)](src/crypto)
[![WebSocket](https://img.shields.io/badge/WebSocket-Realtime-009688?style=for-the-badge&logo=socketdotio&logoColor=white)](src/api)

**Server never sees plaintext. Keys never leave the device. Forward secrecy via Double Ratchet.**

</div>

## Why CipherChat

Most chat demos send plaintext to the server. CipherChat is **real E2E**:

- 🔑 **X25519** ECDH for key exchange (32-byte)
- 🔒 **AES-GCM** (12-byte nonce, HKDF-SHA256 derived)
- 🔄 **Double Ratchet** — symmetric + DH ratchet for forward secrecy
- 🤝 **X3DH-like handshake** — long-term + ephemeral
- 💬 **FastAPI + WebSocket** — register, handshake, send, poll, live

## Architecture

```
Alice (privA, pubA) --ECDH--> shared -> HKDF -> AES key -> nonce+ct -> Server (opaque) -> Bob
                                      ^-- Ratchet advances per message, DH rotates
```

Server stores only `nonce+ciphertext`, never plaintext or private keys.

## Quick Start

```bash
pip install -e .

# Generate keys
cipherchat keygen alice
cipherchat keygen bob

# Start server
cipherchat serve
# open http://127.0.0.1:8080

# Register (via CLI or frontend)
cipherchat register alice
cipherchat register bob
```

## Crypto API

```python
from src.crypto.keys import generate_keypair, ecdh
from src.crypto.aes import derive_key, encrypt, decrypt

priv_a, pub_a = generate_keypair()
priv_b, pub_b = generate_keypair()
shared = ecdh(priv_a, pub_b)
key = derive_key(shared)
ct = encrypt(key, b"hello")
assert decrypt(key, ct) == b"hello"
```

## API

| Method | Path | Purpose |
|---|---|---|
| POST | `/v1/register` | Register username + pubkey |
| GET | `/v1/users` | List users |
| POST | `/v1/messages` | Send envelope (nonce+ct) |
| GET | `/v1/messages/{user}` | Poll queued |
| WS | `/v1/ws/{user}` | Live send/receive |

## Frontend

Static `src/frontend` — connect, load peer key, send. Server never decrypts. Demo uses `btoa` placeholder; real app encrypts in browser via WebCrypto.

## Tests

```bash
pytest  # 11 tests: crypto + API
```

## License

MIT — see [LICENSE](LICENSE)
