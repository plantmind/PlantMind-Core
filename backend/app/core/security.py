class SecurityManager:
    def __init__(self):
        self.authentication_enabled = True
        self.authorization_enabled = True

    def is_authenticated(self):
        return self.authentication_enabled

    def is_authorized(self):
        return self.authorization_enabled
