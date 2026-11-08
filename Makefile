# SPDX-FileCopyrightText: 2026 Leandro Ferreira and Ludus contributors
# SPDX-License-Identifier: MIT
#
# Verification entry points. CI runs `make check`; contributors run the same
# targets locally before opening a pull request (CONTRIBUTING.md).

PYTHON ?= python3
export PYTHONPATH := tools
RANGE ?= origin/main..HEAD

.PHONY: check lint format test trace matrix docs license release commits hooks

check: lint test trace docs license release

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .
	$(PYTHON) -m mypy

format:
	$(PYTHON) -m ruff format .

test:
	$(PYTHON) -m pytest --cov --cov-report=term-missing

trace:
	$(PYTHON) -m ludus_tools.trace check
	$(PYTHON) -m ludus_tools.trace matrix --check

matrix:
	$(PYTHON) -m ludus_tools.trace matrix --write

docs:
	$(PYTHON) -m ludus_tools.doccheck

license:
	$(PYTHON) -m reuse lint

release:
	$(PYTHON) -m ludus_tools.release

commits:
	$(PYTHON) -m ludus_tools.commitcheck --range $(RANGE)

hooks:
	git config core.hooksPath .githooks
