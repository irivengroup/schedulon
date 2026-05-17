from fastapi import APIRouter
from schedulon.application.templates.service import dry_run_campaign, rollback_campaign
router=APIRouter()
@router.get('/dry-run')
def dry_run(): return dry_run_campaign()
@router.post('/rollback')
def rollback(): return rollback_campaign()
