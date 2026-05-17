#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../docker/prod"

docker compose up -d --build postgres app
docker compose exec -T app schedulon db upgrade
docker compose exec -T app schedulon admin seed-demo
docker compose exec -T app python - <<'PY'
from schedulon.infrastructure.db.session import SessionLocal
from schedulon.infrastructure.db import models
from sqlalchemy import select

with SessionLocal() as db:
    sources = list(db.scalars(select(models.TargetSource)))
    targets = list(db.scalars(select(models.Target)))
    jobs = list(db.scalars(select(models.Job)))
    assert sources, "no target sources seeded"
    assert targets, "no targets seeded"
    assert jobs, "no jobs seeded"
    print({
        "sources": len(sources),
        "targets": len(targets),
        "jobs": len(jobs),
        "status": "PROD_READY",
    })
PY
