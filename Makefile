.PHONY: install test lint serve

install:
	pip install -e .

test:
	pytest

lint:
	ruff check src/ tests/

serve:
	cipherchat serve
