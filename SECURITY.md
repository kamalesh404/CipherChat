# Security Policy

## Reporting a Vulnerability

If you find a security issue in CipherChat's crypto (X25519, AES-GCM, Ratchet) or server:

1. Do not open a public issue.
2. Email the maintainer via the GitHub profile with `Subject: [CipherChat] Security`.
3. Include steps to reproduce and the affected version/commit.

We will acknowledge within 48 hours and coordinate a fix.

## Scope

- `src/crypto/*` — key exchange, encryption, ratchet
- `src/api/server.py` — WebSocket and envelope handling
- `src/frontend/*` — client-side key handling

## Best Practices for Users

- Generate keys with `cipherchat keygen <name>` and keep `.cipherchat/*.key` private.
- Never share private keys over the network.
- Verify peer `public_key` via an out-of-band channel before first message.
