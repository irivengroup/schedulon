from __future__ import annotations
from schedulon.infrastructure.security.tokens import TokenService
def test_token_roundtrip():
    svc=TokenService('x'*32); token=svc.issue('alice',['admin'],60); assert svc.decode(token)['sub']=='alice'
