class MockRequests:
    @classmethod
    def mocked_requests_valid_get_root_id(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({"id": "ROOTID1"}, 200)

    @classmethod
    def mocked_requests_invalid_get_root_id(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(None, 500)

    @classmethod
    def mocked_requests_valid_get_files(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {"files": [{"name": "FILE1", "id": "FILEID1"}], "nextPageToken": None}, 200
        )

    @classmethod
    def mocked_requests_valid_get_files_next_page(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "files": [{"name": "FILE1", "id": "FILEID1"}],
                "nextPageToken": "NEXT_PAGE_TOKEN",
            },
            200,
        )

    @classmethod
    def mocked_requests_invalid_get_files(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({"nextPageToken": None}, 500)

    @classmethod
    def mocked_requests_valid_get_shared_drives(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "drives": [{"name": "WeByte", "id": "SHAREDDRIVE1"}],
                "nextPageToken": None,
            },
            200,
        )

    @classmethod
    def mocked_requests_valid_get_shared_drives_next_page(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "drives": [{"name": "WeByte", "id": "SHAREDDRIVE1"}],
                "nextPageToken": "NEXT_PAGE_TOKEN",
            },
            200,
        )

    @classmethod
    def mocked_requests_invalid_get_shared_drives(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({"nextPageToken": None}, 500)

    @classmethod
    def mocked_requests_valid_get_permission_detail_of_shared_drive_file(
            cls, *args, **kwargs
    ):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {"permissionDetails": [{"id": "PERMISSIONID1", "role": "reader"}]}, 200
        )

    @classmethod
    def mocked_requests_invalid_get_permission_detail_of_shared_drive_file(
            cls, *args, **kwargs
    ):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(None, 500)
