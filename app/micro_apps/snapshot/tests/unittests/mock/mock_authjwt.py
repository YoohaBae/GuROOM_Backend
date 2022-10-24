class MockAuthJWT:
    def __init__(self, *args, **kwargs):
        self.access_token = "MOCK_ACCESS_TOKEN1"
        self.refresh_token = "MOCK_REFRESH_TOKEN1"
        self.isAccess = True

    def create_access_token(self, subject):
        pass

    def create_refresh_token(self, subject):
        pass

    def set_access_cookies(self, access_token, response, *args, **kwargs):
        pass

    def set_refresh_cookies(self, refresh_token, response, *args, **kwargs):
        pass

    def jwt_refresh_token_required(self, *args, **kwargs):
        self.isAccess = False

    def jwt_required(self, *args, **kwargs):
        self.isAccess = True

    def unset_access_cookies(self, *args, **kwargs):
        pass

    def unset_jwt_cookies(self, *args, **kwargs):
        pass

    def get_jwt_subject(self, *args, **kwargs):
        if self.isAccess:
            return self.access_token
        return self.refresh_token
