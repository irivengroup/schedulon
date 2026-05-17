from __future__ import annotations
from fastapi import APIRouter
router=APIRouter()
@router.post('/claim/{worker_id}')
def claim(worker_id:str): return {'target_run': None}
