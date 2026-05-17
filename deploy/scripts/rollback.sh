#!/usr/bin/env bash
set -euo pipefail
alembic downgrade "${1:--1}"
echo ROLLBACK_DONE
