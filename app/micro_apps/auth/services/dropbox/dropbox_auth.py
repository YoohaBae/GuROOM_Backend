"""
Dropbox Auth
"""
from app.services.auth import Auth


class DropboxAuth(Auth):
    def __init__(self):
        super().__init__()
        self.SCOPES = []

    def get_authorization_url(self):
        pass

    def get_token(self, code):
        pass

    def revoke_token(self, token):
        pass

    def refresh_token(self, refresh_token):
        pass

    def get_user(self, token):
        pass
