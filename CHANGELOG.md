# Changelog

All notable changes to CipherChat will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Contributing guidelines (CONTRIBUTING.md)
- Architecture documentation with flow diagrams and threat model
- Security policy for responsible disclosure
- X3DH handshake implementation with round-trip tests
- AES-256-GCM encryption for message payloads
- Double Ratchet protocol for forward secrecy
- Ed25519 digital signatures for message authentication
- CLI interface for interactive chat
- WebSocket-based real-time messaging
- SQLite message store with encrypted at-rest storage

### Changed
- Migrated from raw sockets to WebSocket protocol

### Fixed
- Key serialization edge cases in X25519 handshake

## [0.1.0] - 2026-09-14

### Added
- Initial release
- X25519 key exchange
- AES-256-GCM encryption
- Double Ratchet protocol
- Ed25519 signatures
- SQLite message store
- CLI interface
- WebSocket server
