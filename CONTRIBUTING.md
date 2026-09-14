# Contributing to CipherChat

Thanks for your interest in contributing! This document provides guidelines for contributing to CipherChat.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/CipherChat.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Install dependencies: `pip install -e ".[dev]"`
5. Make your changes
6. Run tests: `pytest`
7. Commit and push your changes
8. Open a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/kamalesh404/CipherChat.git
cd CipherChat

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run the app
python -m src.cli.main
```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Write docstrings for public functions
- Keep functions focused and small

## Cryptography Guidelines

- Never implement your own cryptographic primitives â€” use `cryptography` library
- Always use authenticated encryption (AES-GCM, ChaCha20-Poly1305)
- Use X25519 for key exchange, Ed25519 for signatures
- Rotate keys regularly using the Double Ratchet protocol
- Never log or expose private keys

## Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Test edge cases and error handling
- Use `pytest` as the test framework

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure CI passes
4. Request a review from a maintainer

## Reporting Issues

- Use the GitHub issue tracker
- Include steps to reproduce
- Include your environment details
- Never include private keys or sensitive data in issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
