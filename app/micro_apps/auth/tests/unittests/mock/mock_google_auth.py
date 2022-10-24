import logging


class MockGoogleAuth:
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(__name__)
        self.SCOPES = [
            "openid",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

    @classmethod
    def get_user(cls, access_token):
        return {"email": "yoobae@cs.stonybrook.edu"}

    @classmethod
    def get_token(cls, code):
        return {"access_token": "MOCK_ACCESS_TOKEN1",
                "refresh_token": "MOCK_REFRESH_TOKEN1"}

    @classmethod
    def get_authorization_url(cls):
        return "MOCK_AUTH_URL"

    @classmethod
    def refresh_token(cls, refresh_token):
        return "NEW_ACCESS_TOKEN1"

    @classmethod
    def revoke_token(cls, access_token):
        return True
