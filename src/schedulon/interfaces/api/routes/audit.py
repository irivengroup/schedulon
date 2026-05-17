from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from schedulon.infrastructure.db import models
from schedulon.infrastructure.db.session import get_session
router=APIRouter()
@router.get('')
def list_audit(db:Session=Depends(get_session)): return {'items':[r.__dict__ for r in db.scalars(select(models.AuditEvent).order_by(models.AuditEvent.created_at.desc()).limit(500)).all()]}
