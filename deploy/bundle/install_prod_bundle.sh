#!/usr/bin/env bash
set -euo pipefail
deploy/scripts/bootstrap_db.sh
deploy/checks/smoke_test.sh
echo PROD_READY
