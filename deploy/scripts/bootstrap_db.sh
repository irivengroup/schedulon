#!/usr/bin/env bash
set -euo pipefail

alembic upgrade head
schedulon admin seed-demo
echo PROD_READY
