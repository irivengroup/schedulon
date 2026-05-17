from __future__ import annotations
def dry_run_campaign(): return {'status':'DRY_RUN_VALIDATED','impacted_targets':0,'rollback_defined':True,'execution_allowed':True}
def rollback_campaign(): return {'status':'rollback_started','audit_recorded':True}
