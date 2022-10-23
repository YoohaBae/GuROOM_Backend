class MockService:
    @classmethod
    def get_google_auth_url(cls):
        return "URL"

    @classmethod
    def get_google_token(cls, code):
        return {"access_token": "MOCK_ACCESS_TOKEN1",
                "refresh_token": "MOCK_REFRESH_TOKEN1"}

    @classmethod
    def get_google_user(cls, access_token):
        return {"email": "yooha.bae@stonybrook.edu"}

    @classmethod
    def get_none(cls, *args, **kwargs):
        return None

    @classmethod
    def user_not_exist(cls, email):
        return False

    @classmethod
    def user_exists(cls, email):
        return True

    @classmethod
    def refresh_google_access_token(cls, refresh_token):
        return {"access_token": "MOCK_NEW_ACCESS_TOKEN1",
                "refresh_token": refresh_token}

    @classmethod
    def revoke_google_token(cls, access_token):
        return True
