from __future__ import annotations
from fastapi import APIRouter
from schedulon.application.governance.service import validate_preflight
router=APIRouter()
@router.get('/precheck')
def precheck(): return validate_preflight()
@router.get('/freeze-status')
def freeze_status(): return {'freeze_active':False,'status':'execution_allowed'}
