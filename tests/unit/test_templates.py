from schedulon.application.templates import simulate_campaign

def test_dry_run():
    result = simulate_campaign()
    assert result.execution_allowed is True
    assert result.rollback_defined is True
