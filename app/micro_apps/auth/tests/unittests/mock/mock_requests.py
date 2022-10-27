class MockRequests:
    @classmethod
    def mocked_requests_valid_get_token(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {"access_token": "ACCESS_TOKEN1", "refresh_token": "REFRESH_TOKEN1"}, 200
        )

    @classmethod
    def mocked_requests_invalid_get_token(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

        return MockResponse(None, 500)

    @classmethod
    def mocked_requests_valid_revoke_token(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, status_code):
                self.status_code = status_code

        return MockResponse(200)

    @classmethod
    def mocked_requests_invalid_revoke_token(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, status_code):
                self.status_code = status_code

        return MockResponse(500)

    @classmethod
    def mocked_requests_valid_refresh_token(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {"access_token": "ACCESS_TOKEN1", "refresh_token": "REFRESH_TOKEN1"}, 200
        )

    @classmethod
    def mocked_requests_invalid_refresh_token(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

        return MockResponse(None, 500)

    @classmethod
    def mocked_requests_valid_get_user(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "email": "yoobae@cs.stonybrook.edu",
                "name": "Yooha Bae",
                "given_name": "Yooha",
                "family_name": "Bae",
            },
            200,
        )

    @classmethod
    def mocked_requests_invalid_get_user(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

        return MockResponse(None, 500)
