#!/usr/bin/env bash
set -euo pipefail
alembic upgrade head
echo PROD_READY
