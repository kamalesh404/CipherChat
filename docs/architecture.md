# Architecture

## Flow

1. `keygen` → X25519 keypair per user (priv kept in `.cipherchat/*.key`).
2. `register` → POST pubkey to `/v1/register`.
3. Handshake → X3DH combines long-term + ephemeral ECDH → HKDF → AES key.
4. `encrypt`/`decrypt` → AES-GCM with 12-byte nonce, HKDF per message.
5. Ratchet → `Ratchet` advances chain key per message; `dh_ratchet` rotates root for forward secrecy.
6. Server → stores only `nonce+ct`, never plaintext; delivers via WebSocket or poll.

## Components

- `src/crypto/keys.py` — X25519
- `src/crypto/aes.py` — HKDF + AES-GCM
- `src/crypto/ratchet.py` — Double Ratchet
- `src/crypto/handshake.py` — X3DH
- `src/core/store.py` — JSON file store
- `src/api/server.py` — FastAPI + WS
- `src/frontend/*` — static E2E UI

## Threat Model

- Server is untrusted: compromise leaks only ciphertext.
- Forward secrecy: ratchet ensures past messages stay safe if a key leaks.
- Out-of-band pubkey verification recommended before first message.
