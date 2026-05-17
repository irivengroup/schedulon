from __future__ import annotations
from fastapi import APIRouter
from schedulon.application.recovery.service import recover_orphan_runs
router=APIRouter()
@router.post('/recover')
def recover(): return recover_orphan_runs()
@router.post('/workers/drain/{worker_id}')
def drain_worker(worker_id:str): return {'worker_id':worker_id,'status':'draining'}
