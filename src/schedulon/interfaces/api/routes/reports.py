from __future__ import annotations
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from schedulon.infrastructure.db.session import get_session
from schedulon.application.services import campaign_report, report_markdown, export_csv
router=APIRouter()
@router.get('/{run_id}')
def report(run_id:str, db:Session=Depends(get_session)): return campaign_report(db,run_id)
@router.get('/{run_id}/markdown')
def md(run_id:str, db:Session=Depends(get_session)): return {'content': report_markdown(campaign_report(db,run_id))}
@router.get('/{run_id}/targets.csv')
def csv_report(run_id:str, db:Session=Depends(get_session)): return Response(content=export_csv(campaign_report(db,run_id)['targets']), media_type='text/csv')
