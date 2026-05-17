import base64, hashlib, hmac, json
from datetime import datetime, timedelta, timezone
class TokenError(Exception): pass
def _b64e(b): return base64.urlsafe_b64encode(b).decode().rstrip("=")
def _b64d(s): return base64.urlsafe_b64decode((s+"="*(-len(s)%4)).encode())
class TokenService:
    def __init__(self, secret_key): self.secret_key=secret_key.encode()
    def issue(self, subject, roles, ttl_minutes):
        now=datetime.now(timezone.utc)
        payload={"sub":subject,"roles":roles,"iat":int(now.timestamp()),"exp":int((now+timedelta(minutes=ttl_minutes)).timestamp())}
        body=_b64e(json.dumps(payload,sort_keys=True,separators=(",",":")).encode())
        sig=_b64e(hmac.new(self.secret_key,body.encode(),hashlib.sha256).digest())
        return f"{body}.{sig}"
    def decode(self, token):
        body,sig=token.split(".",1)
        expected=_b64e(hmac.new(self.secret_key,body.encode(),hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected): raise TokenError("Invalid signature")
        payload=json.loads(_b64d(body))
        if datetime.now(timezone.utc).timestamp()>payload["exp"]: raise TokenError("Expired token")
        return payload
