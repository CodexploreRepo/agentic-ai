# Agentic AI knowledge hub.
#
# `make help` lists everything. Targets that spend money say so.

.DEFAULT_GOAL := help
SHELL := /bin/bash

PY := uv run
SITE := docs-site

.PHONY: help setup lint format test check docs docs-serve docs-clean \
        nb2md labs-exec lab-01 eval-01 clean

help: ## Show this help
	@grep -hE '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1;36m%-14s\033[0m %s\n", $$1, $$2}'

# --- setup ----------------------------------------------------------------

setup: ## Install Python deps (incl. labs extras) and git hooks
	uv sync --extra labs
	$(PY) pre-commit install
	@echo
	@echo "Next: cp .env.example .env and add ONE model provider key."
	@echo "Then: make test   (works with no keys at all)"

# --- quality --------------------------------------------------------------

lint: ## Ruff check + mypy
	$(PY) ruff check src tests tools
	$(PY) ruff format --check src tests tools
	$(PY) mypy src tools

format: ## Autoformat and autofix
	$(PY) ruff check --fix src tests tools
	$(PY) ruff format src tests tools

test: ## Unit tests. No API keys, no network, no spend
	$(PY) pytest tests -q

check: lint test ## Everything CI runs

# --- labs -----------------------------------------------------------------
# These call real model APIs and cost real money.

lab-01: ## Open Module 01's notebook
	$(PY) jupyter lab labs/01-foundations/01_first_agentic_workflow.ipynb

eval-01: ## [SPENDS MONEY] Run Module 01's eval set, write a scorecard
	$(PY) python labs/01-foundations/run_evals.py

labs-exec: ## [SPENDS MONEY] Execute every lab notebook in place
	@for nb in labs/*/*.ipynb; do \
		echo "executing $$nb"; \
		$(PY) jupyter nbconvert --to notebook --execute --inplace "$$nb" || exit 1; \
	done

# --- docs -----------------------------------------------------------------

nb2md: ## Render lab notebooks into docs/labs/
	$(PY) python tools/nb2md.py

docs: nb2md ## Build the site (fails on broken links)
	cd $(SITE) && npm ci && npm run build

docs-serve: nb2md ## Serve the site locally with hot reload
	cd $(SITE) && npm start

docs-clean: ## Remove generated notebook pages and site build output
	find docs/labs -name '*.md' ! -name 'index.md' -delete
	rm -rf $(SITE)/build $(SITE)/.docusaurus

# --- housekeeping ---------------------------------------------------------

clean: docs-clean ## Also remove caches and run artefacts
	rm -rf .pytest_cache .ruff_cache .mypy_cache .runs
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
