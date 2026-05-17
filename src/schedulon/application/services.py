import uuid, io, csv
from sqlalchemy import select
from sqlalchemy.orm import Session
from schedulon.infrastructure.db import models
def new_id(prefix): return f"{prefix}-{uuid.uuid4().hex[:16]}"
def audit(db, actor, action, entity_type, entity_id, metadata=None):
    db.add(models.AuditEvent(id=new_id("audit"), actor_type="user", actor_id=actor.get("actor_id") if isinstance(actor,dict) else actor, action=action, entity_type=entity_type, entity_id=entity_id, metadata_json=metadata or {}))
def seed_demo(db):
    existing=db.scalar(select(models.Job).where(models.Job.name=="demo-check-uptime"))
    if existing: return {"status":"already_seeded","job_id":existing.id}
    src=models.TargetSource(id=new_id("src"), name="demo-targets", source_type="inline", config={}); db.add(src)
    db.add(models.Target(id=new_id("target"), source_id=src.id, name="localhost", address="127.0.0.1", vars={}, is_active=True))
    job=models.Job(id=new_id("job"), name="demo-check-uptime", execution_backend="command", backend_config={"command":"uptime"}, target_source_id=src.id, environment="development", schedule_type="manual", dependencies=[])
    db.add(job); audit(db,"system","demo.seeded","job",job.id,{"source_id":src.id}); db.commit()
    return {"status":"seeded","job_id":job.id,"target_source_id":src.id}
def create_job(db, actor, payload):
    job=models.Job(id=new_id("job"), name=payload["name"], execution_backend=payload["execution_backend"], backend_config=payload.get("backend_config",{}), target_source_id=payload.get("target_source_id"), environment=payload.get("environment","development"), schedule_type=payload.get("schedule_type","manual"), dependencies=payload.get("dependencies",[]), requires_approval=payload.get("requires_approval",False))
    db.add(job); audit(db,actor,"job.created","job",job.id,{"name":job.name}); db.commit(); return job
def list_jobs(db, actor): return list(db.scalars(select(models.Job).order_by(models.Job.created_at.desc())))
def trigger_job(db, actor, job_id, payload):
    job=db.get(models.Job, job_id)
    if not job: raise ValueError("Job not found")
    if job.environment=="production" and not payload.get("ticket_number"): raise ValueError("production_ticket_required")
    run=models.JobRun(id=new_id("run"), job_id=job.id, status="queued", actor_id=actor.get("actor_id"), ticket_number=payload.get("ticket_number"), environment=job.environment, runtime_config=payload.get("runtime_config",{}))
    db.add(run)
    targets=list(db.scalars(select(models.Target).where(models.Target.source_id==job.target_source_id))) if job.target_source_id else []
    if not targets: targets=[models.Target(id="inline-localhost", source_id="inline", name="localhost", address="127.0.0.1", vars={}, is_active=True)]
    for t in targets: db.add(models.TargetRun(id=new_id("tr"), run_id=run.id, target_id=t.id, target_name=t.name, target_address=t.address, target_vars=t.vars, status="queued"))
    audit(db,actor,"campaign.triggered","campaign",run.id,{"job_id":job.id}); db.commit(); return run
def campaign_report(db, run_id):
    run=db.get(models.JobRun, run_id); job=db.get(models.Job, run.job_id)
    trs=list(db.scalars(select(models.TargetRun).where(models.TargetRun.run_id==run_id)))
    return {"campaign_id":run.id,"job_name":job.name,"status":run.status,"summary":{"total_targets":len(trs),"succeeded_targets":sum(t.status=="succeeded" for t in trs),"failed_targets":sum(t.status=="failed" for t in trs)},"targets":[{"target_name":t.target_name,"target_address":t.target_address,"status":t.status,"exit_code":t.exit_code,"error_message":t.error_message} for t in trs]}
def report_markdown(report): return "# Schedulon campaign report\n" + str(report)
def export_csv(rows):
    if not rows: return ""
    buf=io.StringIO(); w=csv.DictWriter(buf, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows); return buf.getvalue()
def import_targets(db, actor, name, source_type, rows):
    src=models.TargetSource(id=new_id("src"), name=name, source_type=source_type, config={}); db.add(src)
    for r in rows: db.add(models.Target(id=new_id("target"), source_id=src.id, name=r["name"], address=r["address"], vars=r.get("vars",{}), is_active=True))
    audit(db,actor,"target_source.imported","target_source",src.id,{"count":len(rows)}); db.commit(); return src
