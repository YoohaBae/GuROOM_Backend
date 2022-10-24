import json

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


class MockDataBase:
    def __init__(self):
        self._db = None
        self.collection_name = "auth"

    @classmethod
    def get_user(cls, email):
        with open(absolute_path_to_data + "/auth.json") as json_file:
            data = json.load(json_file)
            for user in data:
                if user["email"] == email:
                    return user

    @classmethod
    def check_user_exists_when_exists(cls, email):
        return True

    @classmethod
    def check_user_exists_when_not_exists(cls, email):
        return False

    @classmethod
    def save_user(cls, email):
        pass
