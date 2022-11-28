import datetime


class MockRequests:
    @classmethod
    def mocked_requests_valid_get_files(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "entries": [
                    {
                        "size": 1000,
                        ".tag": "file",
                        "path_display": "/FOLDER1/FILE1",
                        "name": "FILE1",
                        "id": "id:FILE_ID1",
                    }
                ],
                "cursor": None,
                "has_more": False,
            },
            200,
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
                "entries": [
                    {
                        "size": 1000,
                        ".tag": "file",
                        "path_display": "/FOLDER1/FILE1",
                        "name": "FILE1",
                        "id": "id:FILE_ID1",
                    },
                    {
                        "server_modified": datetime.datetime.utcnow(),
                        ".tag": "file",
                        "path_display": "/FILE1",
                        "name": "FOLDER1",
                        "shared_folder_id": "SHARED_FOLDER_ID1",
                        "id": "id:FILE_ID2",
                    },
                    {
                        "server_modified": datetime.datetime.utcnow(),
                        ".tag": "file",
                        "path_display": "/FOLDER1/FILE2",
                        "name": "FILE2",
                        "parent_shared_folder_id": "SHARED_FOLDER_ID1",
                        "id": "id:FILE_ID3",
                    },
                ],
                "cursor": None,
                "has_more": False,
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
    def mocked_requests_valid_get_permissions_of_file(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "cursor": None,
                "users": [
                    {
                        "user": {
                            "email": "yooha.bae@stonybrook.edu",
                            "account_id": "ACCOUNT_ID1",
                            "display_name": "Yooha Bae",
                        },
                        "access_type": {".tag": "editor"},
                    },
                    {
                        "user": {
                            "email": "yoolbi.lee@stonybrook.edu",
                            "account_id": "ACCOUNT_ID2",
                            "display_name": "Yool Bi Lee",
                        },
                        "access_type": {".tag": "owner"},
                    },
                    {
                        "user": {
                            "email": "haeun.park.1@stonybrook.edu",
                            "account_id": "ACCOUNT_ID3",
                            "display_name": "Haeun Park",
                        },
                        "access_type": {".tag": "viewer"},
                    },
                    {
                        "user": {
                            "email": "john.doe@stonybrook.edu",
                            "account_id": "ACCOUNT_ID4",
                            "display_name": "John Doe",
                        },
                        "access_type": {".tag": "viewer_no_comment"},
                    },
                ],
            },
            200,
        )

    @classmethod
    def mocked_requests_invalid_get_permissions_of_file(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({}, 500)

    @classmethod
    def mocked_requests_invalid_role_get_permissions_of_file(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "cursor": None,
                "users": [
                    {
                        "user": {
                            "email": "yooha.bae@stonybrook.edu",
                            "account_id": "ACCOUNT_ID1",
                            "display_name": "Yooha Bae",
                        },
                        "access_type": {".tag": "invalid_role"},
                    },
                    {
                        "user": {
                            "email": "yoolbi.lee@stonybrook.edu",
                            "account_id": "ACCOUNT_ID2",
                            "display_name": "Yool Bi Lee",
                        },
                        "access_type": {".tag": "owner"},
                    },
                    {
                        "user": {
                            "email": "haeun.park.1@stonybrook.edu",
                            "account_id": "ACCOUNT_ID3",
                            "display_name": "Haeun Park",
                        },
                        "access_type": {".tag": "invalid_role2"},
                    },
                    {
                        "user": {
                            "email": "john.doe@stonybrook.edu",
                            "account_id": "ACCOUNT_ID4",
                            "display_name": "John Doe",
                        },
                        "access_type": {".tag": "viewer_no_comment"},
                    },
                ],
            },
            200,
        )

    @classmethod
    def mocked_requests_valid_get_permissions_of_shared_folder(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "cursor": None,
                "users": [
                    {
                        "user": {
                            "email": "yooha.bae@stonybrook.edu",
                            "account_id": "ACCOUNT_ID1",
                            "display_name": "Yooha Bae",
                        },
                        "access_type": {".tag": "editor"},
                    },
                    {
                        "user": {
                            "email": "yoolbi.lee@stonybrook.edu",
                            "account_id": "ACCOUNT_ID2",
                            "display_name": "Yool Bi Lee",
                        },
                        "access_type": {".tag": "owner"},
                    },
                    {
                        "user": {
                            "email": "haeun.park.1@stonybrook.edu",
                            "account_id": "ACCOUNT_ID3",
                            "display_name": "Haeun Park",
                        },
                        "access_type": {".tag": "viewer"},
                    },
                    {
                        "user": {
                            "email": "john.doe@stonybrook.edu",
                            "account_id": "ACCOUNT_ID4",
                            "display_name": "John Doe",
                        },
                        "access_type": {".tag": "viewer_no_comment"},
                    },
                ],
            },
            200,
        )

    @classmethod
    def mocked_requests_invalid_get_permissions_of_shared_folder(cls, *args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({}, 500)

    @classmethod
    def mocked_requests_invalid_role_get_permissions_of_shared_folders(
        cls, *args, **kwargs
    ):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {
                "cursor": None,
                "users": [
                    {
                        "user": {
                            "email": "yooha.bae@stonybrook.edu",
                            "account_id": "ACCOUNT_ID1",
                            "display_name": "Yooha Bae",
                        },
                        "access_type": {".tag": "invalid_role"},
                    },
                    {
                        "user": {
                            "email": "yoolbi.lee@stonybrook.edu",
                            "account_id": "ACCOUNT_ID2",
                            "display_name": "Yool Bi Lee",
                        },
                        "access_type": {".tag": "owner"},
                    },
                    {
                        "user": {
                            "email": "haeun.park.1@stonybrook.edu",
                            "account_id": "ACCOUNT_ID3",
                            "display_name": "Haeun Park",
                        },
                        "access_type": {".tag": "viewer"},
                    },
                    {
                        "user": {
                            "email": "john.doe@stonybrook.edu",
                            "account_id": "ACCOUNT_ID4",
                            "display_name": "John Doe",
                        },
                        "access_type": {".tag": "viewer_no_comment"},
                    },
                ],
            },
            200,
        )
