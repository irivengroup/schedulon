from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schedulon.infrastructure.db.session import get_session
from schedulon.application.services import seed_demo
router=APIRouter()
@router.post('/seed-demo')
def seed(db:Session=Depends(get_session)): return seed_demo(db)
