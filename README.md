# Schedulon 1.0.6

Livrable consolidé complet.

## Inclus

- CLI complète
- API FastAPI + Swagger/OpenAPI
- Web UI
- PostgreSQL + Alembic
- Workers distribués
- Scheduler leader foundation
- Multi-site DR ready
- PostgreSQL HA Patroni/etcd/HAProxy
- ITSM ticket obligatoire en production
- LDAP + restriction groupes autorisés
- RBAC
- approvals maker/checker
- dépendances inter-jobs
- fenêtres de maintenance / change freeze hooks
- rapports de campagne avec statut par target
- audit trail : qui, quoi, quand
- notifications email/webhook/Slack/Teams-ready
- inventaires TXT/CSV/YAML/Git/CMDB/NetBox/ServiceNow CMDB
- secrets abstraction
- dry-run, impact validation, rollback
- recovery runs orphelins / verrous obsolètes
- supervision Telegraf + InfluxDB + Grafana
- Docker, Helm, systemd, Ansible
- scripts bootstrap/upgrade/rollback/smoke/security

## Démarrage local

```bash
cd deploy/docker/prod
docker compose up --build
docker compose exec app schedulon db upgrade
docker compose exec app schedulon admin seed-demo
```

UI: http://localhost:8000/ui  
Swagger: http://localhost:8000/docs


## CI

Le projet inclut maintenant :
- `requirements.txt` pour les workflows qui installent uniquement `requirements.txt`
- `.github/workflows/python-package.yml` complet
- compatibilité syntaxique Python 3.9 → 3.12


- Compatibilité CI étendue jusqu'à Python 3.14.


## Python 3.9 compatibility fix

Pydantic v2 evaluates annotations during model construction. For Python 3.9,
`str | None` is not valid during that evaluation. Schedulon now uses
`typing.Optional[...]` in Pydantic-facing settings and includes `eval-type-backport`
as an additional safety dependency.


## CI fix 1.0.6

`build` and `twine` are now installed explicitly in GitHub Actions before
`python -m build` is executed. This avoids failures on Python 3.13/3.14 where
optional dev dependencies may not be available in the environment at that step.


## SQLAlchemy Python 3.9 compatibility fix

SQLAlchemy evaluates ORM annotations during mapper configuration. The ORM models
now use `typing.Optional[...]` instead of PEP 604 unions such as
`datetime | None`, which keeps Alembic migrations compatible with Python 3.9.


## Docker seed-demo validation

A Docker-specific validation script is included:

```bash
deploy/checks/docker_seed_demo_check.sh
```

It builds the Compose stack, runs Alembic migrations, executes
`schedulon admin seed-demo`, and verifies that `target_sources`, `targets`,
and `jobs` were inserted correctly.
