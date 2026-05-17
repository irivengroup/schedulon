from schedulon.infrastructure.security.rbac import has_permission
def test_admin_all(): assert has_permission(['admin'],'anything')
