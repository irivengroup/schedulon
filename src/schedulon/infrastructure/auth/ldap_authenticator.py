class LdapAuthenticationError(Exception): pass
class LdapAccessDeniedError(Exception): pass
class LdapAuthenticator:
    def __init__(self, settings): self.settings=settings
    def authenticate(self, username, password):
        if not username or not password: raise LdapAuthenticationError("Invalid username or password")
        return {"username": username, "roles": ["viewer"], "groups": []}
