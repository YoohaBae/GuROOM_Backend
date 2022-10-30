import json

mock_user_id = "MOCK_USER_ID1"
absolute_path_to_data = "./app/micro_apps/auth/tests/data"


class MockMongoDB:
    def __init__(self, url, db_name, drive_type):
        self.db = None
        self.drive_type = drive_type

    def insert_document(self, collection_name: str, data):
        pass

    def find_document(self, collection_name: str, query=None, filter_query=None):
        if "auth" in collection_name:
            with open(absolute_path_to_data + "/auth.json") as json_file:
                data = json.load(json_file)
                for user in data:
                    if (
                        user["email"] == query["email"]
                        and user["type"] == self.drive_type
                    ):
                        return user

    def update_document(self, collection_name: str, update_query=None, query=None):
        pass
