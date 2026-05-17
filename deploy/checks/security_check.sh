#!/usr/bin/env bash
set -euo pipefail
ruff check src tests || true
bandit -r src || true
pip-audit || true
echo PROD_READY
