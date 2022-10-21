import logging

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"
mock_user_id = "MOCK_USER_ID1"


class MockGoogleAuth:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.SCOPES = [
            "openid",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

    def get_user(self, access_token):
        return {"email": "yoobae@cs.stonybrook.edu"}
