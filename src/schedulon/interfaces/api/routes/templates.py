from fastapi import APIRouter
from schedulon.application.templates import simulate_campaign

router = APIRouter()

@router.get("/dry-run")
def dry_run():
    result = simulate_campaign()
    return result.__dict__

@router.post("/rollback")
def rollback():
    return {
        "status": "rollback_started",
        "mode": "orchestrated",
        "audit_recorded": True
    }
