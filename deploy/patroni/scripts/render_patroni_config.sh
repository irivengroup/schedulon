#!/usr/bin/env bash
set -euo pipefail
envsubst < deploy/patroni/templates/patroni.yml.tpl > /tmp/schedulon-patroni.yml
echo PROD_READY
