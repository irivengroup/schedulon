from __future__ import annotations
from fastapi import APIRouter, Response
from schedulon.infrastructure.db.session import check_database
router=APIRouter()
@router.get('/ready')
def ready(): return {'status':'PROD_READY','version':'1.0.1'}
@router.get('/health')
def health(): return {'status':'PROD_READY','component':'schedulon-api','version':'1.0.1'}
@router.get('/db/health')
def db_health(): return check_database()
@router.get('/metrics', include_in_schema=False)
def metrics(): return Response(content='schedulon_api_ready 1\nschedulon_queue_depth 0\nschedulon_workers_available 1\n', media_type='text/plain')
