"""
Interface for Cloud Drive Authentication
"""
import logging
import os


class Auth:
    def __init__(self):
        format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=format)
        self.logger = logging.getLogger()
        self.SECRET = os.getenv("JWT_SECRET_KEY")
        self.ALGORITHM = "HS256"
        self._logger = logging.getLogger(__name__)
        self.client_id = None
        self.redirect_uri = None
        self.client_secret = None

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
