import json

mock_user_id = "MOCK_USER_ID1"
absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


class MockMongoDB:
    def __init__(self, url, db_name):
        self.db = None

    @classmethod
    def get_collection_names(cls):
        return [
            f"{mock_user_id}.FILE_SNAPSHOT1.files",
            f"{mock_user_id}.FILE_SNAPSHOT1.permissions",
            f"{mock_user_id}.FILE_SNAPSHOT2.files",
            f"{mock_user_id}.FILE_SNAPSHOT2.permissions",
        ]

    @classmethod
    def drop_collection(cls, collection_name):
        return None

    @classmethod
    def rename_collection(cls, collection_name, new_collection_name):
        return None

    @classmethod
    def insert_document(cls, collection_name: str, data):
        pass

    @classmethod
    def insert_documents(cls, collection_name: str, data):
        pass

    @classmethod
    def delete_document(cls, collection_name: str, query=None):
        pass

    @classmethod
    def delete_documents(cls, collection_name: str, query=None):
        pass

    @classmethod
    def find_document(cls, collection_name: str, query=None, filter_query=None):
        if query is None:
            query = {}
        if "file_snapshots" in collection_name:
            with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
                data = json.load(json_file)
                return data[0]
        if "files" in collection_name:
            with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
                data = json.load(json_file)
                if "id" in query:
                    for file in data:
                        if file["id"] == query["id"]:
                            return file
        return None

    @classmethod
    def find_documents(cls, collection_name: str, query=None, filter_query=None):
        if query is None:
            query = {}
        if "file_snapshots" in collection_name:
            with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
                data = json.load(json_file)
                return data
        if "files" in collection_name:
            with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
                data = json.load(json_file)
                result_file = []
                if query == {}:
                    return data
                if "parents" in query:
                    for file in data:
                        if "$size" in query["parents"]:
                            if len(file["parents"]) == 0:
                                result_file.append(file)
                        elif "$in" in query["parents"]:
                            if query["parents"]["$in"][0] in file["parents"]:
                                result_file.append(file)
                    return result_file
                if "path" in query:
                    for file in data:
                        if query["path"] == file["path"]:
                            result_file.append(file)
                    return result_file
        if "permissions" in collection_name:
            with open(
                absolute_path_to_data + "/snapshot1_permissions.json"
            ) as json_file:
                data = json.load(json_file)
                target_permissions = []
                if query == {}:
                    return data
                for permission in data:
                    if "file_id" in query:
                        if permission["file_id"] == query["file_id"]:
                            target_permissions.append(permission)
                return target_permissions
        if "group_membership_snapshots" in collection_name:
            with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
                data = json.load(json_file)
                return data
        return []

    @classmethod
    def update_document(cls, collection_name: str, update_query, query=None):
        pass

    @classmethod
    def update_documents(cls, collection_name: str, update_query, query=None):
        pass