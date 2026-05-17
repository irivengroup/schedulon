from fastapi import APIRouter
router=APIRouter()
@router.get('')
def approvals(): return {'items': []}
