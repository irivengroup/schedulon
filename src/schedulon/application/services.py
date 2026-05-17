from __future__ import annotations

import csv
import io
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from schedulon.infrastructure.db import models


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:16]}"


def audit(
    db: Session,
    actor: Dict[str, Any] | str | None,
    action: str,
    entity_type: str,
    entity_id: Optional[str],
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    db.add(
        models.AuditEvent(
            id=new_id("audit"),
            actor_type="user",
            actor_id=actor.get("actor_id") if isinstance(actor, dict) else actor,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata_json=metadata or {},
        )
    )


def seed_demo(db: Session) -> Dict[str, str]:
    """Seed a deterministic demo source/job.

    Important: Target rows reference TargetSource by FK. Because the model does
    not define ORM relationships yet, we explicitly flush the parent row before
    inserting child rows. This keeps PostgreSQL FK enforcement happy in Docker
    and production.
    """

    existing = db.scalar(select(models.Job).where(models.Job.name == "demo-check-uptime"))
    if existing:
        return {"status": "already_seeded", "job_id": existing.id}

    try:
        src = models.TargetSource(
            id=new_id("src"),
            name="demo-targets",
            source_type="inline",
            config={},
        )
        db.add(src)
        db.flush()  # parent row must exist before targets use source_id

        db.add_all(
            [
                models.Target(
                    id=new_id("target"),
                    source_id=src.id,
                    name="localhost",
                    address="127.0.0.1",
                    vars={},
                    is_active=True,
                ),
                models.Target(
                    id=new_id("target"),
                    source_id=src.id,
                    name="demo-node-2",
                    address="10.0.0.2",
                    vars={},
                    is_active=True,
                ),
            ]
        )

        job = models.Job(
            id=new_id("job"),
            name="demo-check-uptime",
            execution_backend="command",
            backend_config={"command": "uptime"},
            target_source_id=src.id,
            environment="development",
            schedule_type="manual",
            dependencies=[],
        )
        db.add(job)

        audit(db, "system", "demo.seeded", "job", job.id, {"source_id": src.id})
        db.commit()

        return {"status": "seeded", "job_id": job.id, "target_source_id": src.id}

    except Exception:
        db.rollback()
        raise


def create_job(db: Session, actor: Dict[str, Any], payload: Dict[str, Any]) -> models.Job:
    try:
        job = models.Job(
            id=new_id("job"),
            name=payload["name"],
            execution_backend=payload["execution_backend"],
            backend_config=payload.get("backend_config", {}),
            target_source_id=payload.get("target_source_id"),
            environment=payload.get("environment", "development"),
            schedule_type=payload.get("schedule_type", "manual"),
            dependencies=payload.get("dependencies", []),
            requires_approval=payload.get("requires_approval", False),
        )
        db.add(job)
        audit(db, actor, "job.created", "job", job.id, {"name": job.name})
        db.commit()
        return job
    except Exception:
        db.rollback()
        raise


def list_jobs(db: Session, actor: Dict[str, Any]) -> List[models.Job]:
    return list(db.scalars(select(models.Job).order_by(models.Job.created_at.desc())))


def trigger_job(
    db: Session,
    actor: Dict[str, Any],
    job_id: str,
    payload: Dict[str, Any],
) -> models.JobRun:
    job = db.get(models.Job, job_id)
    if not job:
        raise ValueError("Job not found")

    if job.environment == "production" and not payload.get("ticket_number"):
        raise ValueError("production_ticket_required")

    try:
        run = models.JobRun(
            id=new_id("run"),
            job_id=job.id,
            status="queued",
            actor_id=actor.get("actor_id"),
            ticket_number=payload.get("ticket_number"),
            environment=job.environment,
            runtime_config=payload.get("runtime_config", {}),
        )
        db.add(run)
        db.flush()

        targets = (
            list(db.scalars(select(models.Target).where(models.Target.source_id == job.target_source_id)))
            if job.target_source_id
            else []
        )

        if not targets:
            targets = [
                models.Target(
                    id="inline-localhost",
                    source_id="inline",
                    name="localhost",
                    address="127.0.0.1",
                    vars={},
                    is_active=True,
                )
            ]

        for target in targets:
            db.add(
                models.TargetRun(
                    id=new_id("tr"),
                    run_id=run.id,
                    target_id=target.id,
                    target_name=target.name,
                    target_address=target.address,
                    target_vars=target.vars,
                    status="queued",
                )
            )

        audit(db, actor, "campaign.triggered", "campaign", run.id, {"job_id": job.id})
        db.commit()
        return run

    except Exception:
        db.rollback()
        raise


def campaign_report(db: Session, run_id: str) -> Dict[str, Any]:
    run = db.get(models.JobRun, run_id)
    if not run:
        raise ValueError("Run not found")

    job = db.get(models.Job, run.job_id)
    target_runs = list(db.scalars(select(models.TargetRun).where(models.TargetRun.run_id == run_id)))

    return {
        "campaign_id": run.id,
        "job_name": job.name if job else None,
        "status": run.status,
        "summary": {
            "total_targets": len(target_runs),
            "succeeded_targets": sum(t.status == "succeeded" for t in target_runs),
            "failed_targets": sum(t.status == "failed" for t in target_runs),
        },
        "targets": [
            {
                "target_name": t.target_name,
                "target_address": t.target_address,
                "status": t.status,
                "exit_code": t.exit_code,
                "error_message": t.error_message,
            }
            for t in target_runs
        ],
    }


def report_markdown(report: Dict[str, Any]) -> str:
    return "# Schedulon campaign report\n" + str(report)


def export_csv(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return ""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def import_targets(
    db: Session,
    actor: Dict[str, Any],
    name: str,
    source_type: str,
    rows: List[Dict[str, Any]],
) -> models.TargetSource:
    try:
        source = models.TargetSource(
            id=new_id("src"),
            name=name,
            source_type=source_type,
            config={},
        )
        db.add(source)
        db.flush()

        for row in rows:
            db.add(
                models.Target(
                    id=new_id("target"),
                    source_id=source.id,
                    name=row["name"],
                    address=row["address"],
                    vars=row.get("vars", {}),
                    is_active=True,
                )
            )

        audit(db, actor, "target_source.imported", "target_source", source.id, {"count": len(rows)})
        db.commit()
        return source
    except Exception:
        db.rollback()
        raise
