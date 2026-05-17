from schedulon.interfaces.api.app import create_app
def test_routes_present():
    paths={r.path for r in create_app().routes}
    assert '/api/v1/jobs' in paths
    assert '/api/v1/reports/{run_id}' in paths
    assert '/api/v1/audit-events' in paths
