from __future__ import annotations
ROLE_PERMISSIONS = {
    "admin": {"*"},
    "operator": {"job:read","job:create","job:trigger","run:read","report:read","report:send","target:import"},
    "approver": {"job:read","run:read","approval:approve","report:read"},
    "viewer": {"job:read","run:read","report:read","audit:read"},
}
class PermissionDenied(Exception): pass
def has_permission(roles, permission): return any("*" in ROLE_PERMISSIONS.get(r,set()) or permission in ROLE_PERMISSIONS.get(r,set()) for r in roles)
def require_permission(roles, permission):
    if not has_permission(roles, permission): raise PermissionDenied(f"Missing permission: {permission}")
