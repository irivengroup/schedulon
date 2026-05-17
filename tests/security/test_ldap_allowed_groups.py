from __future__ import annotations
from schedulon.infrastructure.config.settings import Settings
def test_allowed_groups_parse(): assert 'cn=a,dc=example' in Settings(ldap_allowed_groups='CN=A,DC=example').allowed_ldap_groups()
