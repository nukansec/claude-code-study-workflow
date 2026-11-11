# Uso: make setup && make check
# Funciona no Git Bash (Windows) e no Linux do CI.

ifeq ($(OS),Windows_NT)
  PYTHON_BOOT ?= py -3.12
  VENV_BIN := .venv/Scripts
else
  PYTHON_BOOT ?= python3.12
  VENV_BIN := .venv/bin
endif

PY := $(VENV_BIN)/python
PIP_VERSION := 26.3
MARKDOWNLINT := npx --yes markdownlint-cli2@0.24.0

.PHONY: help setup lint lint-py lint-md test gates check secrets hooks

help: ## Lista os targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'

setup: ## Cria a .venv e instala as dependências fixadas
	$(PYTHON_BOOT) -m venv .venv
	$(PY) -m pip install --quiet "pip==$(PIP_VERSION)"
	$(PY) -m pip install --quiet --group dev

lint: lint-py lint-md ## ruff + markdownlint

lint-py:
	$(PY) -m ruff check scripts tests
	$(PY) -m ruff format --check scripts tests

lint-md:
	$(MARKDOWNLINT)

test: ## pytest
	$(PY) -m pytest

gates: ## Os três contratos
	$(PY) scripts/validate_commands.py
	$(PY) scripts/validate_settings.py
	$(PY) scripts/check_privacy.py

check: lint test gates ## Tudo o que o CI roda (exceto gitleaks)

secrets: ## gitleaks no histórico (precisa do gitleaks no PATH)
	gitleaks git --redact --no-banner .

hooks: ## Instala os hooks do pre-commit
	$(PY) -m pre_commit install

