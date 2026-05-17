from __future__ import annotations
from fastapi import APIRouter
router=APIRouter()
@router.get('/config')
def config(): return {'auth_mode':'none'}
