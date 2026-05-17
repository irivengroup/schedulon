from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from schedulon.infrastructure.db.session import get_session
from schedulon.interfaces.api.dependencies import get_actor
from schedulon.application import services
router=APIRouter()
class JobCreate(BaseModel):
    name:str; execution_backend:str; backend_config:dict=Field(default_factory=dict); target_source_id:str|None=None; environment:str='development'; dependencies:list[str]=Field(default_factory=list); requires_approval:bool=False
class TriggerRequest(BaseModel):
    runtime_config:dict=Field(default_factory=dict); ticket_number:str|None=None; idempotency_key:str|None=None
@router.get('')
def list_jobs(db:Session=Depends(get_session), actor:dict=Depends(get_actor)): return {'items':[j.__dict__ for j in services.list_jobs(db,actor)]}
@router.post('')
def create_job(payload:JobCreate, db:Session=Depends(get_session), actor:dict=Depends(get_actor)):
    try: return services.create_job(db,actor,payload.model_dump()).__dict__
    except Exception as exc: raise HTTPException(status_code=409, detail=str(exc))
@router.post('/{job_id}/trigger')
def trigger(job_id:str, payload:TriggerRequest, db:Session=Depends(get_session), actor:dict=Depends(get_actor)):
    try: return services.trigger_job(db,actor,job_id,payload.model_dump()).__dict__
    except Exception as exc: raise HTTPException(status_code=409, detail=str(exc))
