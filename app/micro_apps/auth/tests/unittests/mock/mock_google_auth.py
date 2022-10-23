class MockGoogleAuth:
    def __init__(self, *args, **kwargs):
        pass

    def get_token(self, code):
        return {"access_token": "MOCK_ACCESS_TOKEN1",
                "refresh_token": "MOCK_REFRESH_TOKEN1"}

    def get_authorization_url(self):
        return "MOCK_AUTH_URL"
