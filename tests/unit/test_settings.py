from schedulon.infrastructure.config.settings import Settings
def test_settings_default(): assert Settings().api_port == 8000
