"""
Interface for Cloud Drive Authentication
"""
import logging
import os


class Auth:
    def __init__(self):
        self.SECRET = os.getenv("JWT_SECRET_KEY")
        self.ALGORITHM = "HS256"
        self._logger = logging.getLogger(__name__)

    def authenticate_user(self, encoded_token):
        pass

    def get_credentials_from_tokens(self, decoded_token):
        pass

    def refresh_credentials(self, creds):
        pass

    def create_credentials(self):
        pass

    def get_user(self, creds):
        pass

    def get_files(self, creds):
        pass

    def get_drive_service(self, creds):
        pass
