import json

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


class MockUserDataBase:
    def __init__(self):
        self._db = None
        self.collection_name = "auth"

    @classmethod
    def get_user(cls, email):
        with open(absolute_path_to_data + "/auth.json") as json_file:
            data = json.load(json_file)
            print(data)
            for user in data:
                if user["email"] == email and user["type"] == "google":
                    return user
