import logging
from app.micro_apps.auth.services.models.user import User


class MockDropboxAuth:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(__name__)

    @classmethod
    def get_user(cls, access_token):
        data = {
            "email": "yooha.bae@stonybrook.edu",
            "name": "Yooha Bae",
            "given_name": "Yooha",
            "family_name": "Bae",
        }
        return User(**data)

    @classmethod
    def get_token(cls, code):
        return {
            "access_token": "MOCK_ACCESS_TOKEN1",
            "refresh_token": "MOCK_REFRESH_TOKEN1",
        }

    @classmethod
    def get_authorization_url(cls):
        return "MOCK_AUTH_URL"
