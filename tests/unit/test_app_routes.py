from __future__ import annotations

from schedulon.interfaces.api.app import create_app


def test_routes_present():
    paths = {route.path for route in create_app().routes}
    assert "/api/v1/jobs" in paths
    assert "/api/v1/reports/{run_id}" in paths
    assert "/api/v1/audit-events" in paths
    assert "/api/v1/recovery/recover" in paths
    assert "/api/v1/governance/precheck" in paths
    assert "/metrics" in paths
