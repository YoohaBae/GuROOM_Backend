import json

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"


class MockQueryBuilder:
    def __init__(self, user_id, email, snapshot_name):
        self.user_email = email
        self.user_id = user_id
        self.snapshot_name = snapshot_name

    @classmethod
    def get_files_of_query(cls, query):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
        return data

    @classmethod
    def create_tree_and_validate(cls, query):
        pass
