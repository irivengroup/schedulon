# Schedulon 1.0.1

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
