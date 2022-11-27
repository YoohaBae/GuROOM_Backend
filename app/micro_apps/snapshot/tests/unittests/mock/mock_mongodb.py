import json

mock_user_id = "MOCK_USER_ID1"
absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/google"


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
                if "shared" in query:
                    for file in data:
                        if file["shared"] is None:
                            result_file.append(file)
                    return result_file
                if "sharingUser.emailAddress" in query:
                    for file in data:
                        if file["sharingUser"] is not None:
                            if "emailAddress" in file["sharingUser"]:
                                if (
                                    file["sharingUser"]["emailAddress"]
                                    == query["sharingUser.emailAddress"]
                                ):
                                    result_file.append(file)
                    return result_file
                if "id" in query:
                    for file in data:
                        if file["id"] in query["id"]["$in"]:
                            result_file.append(file)
                    return result_file
                if "name" in query and "$regex" in query["name"]:
                    if "mimeType" in query:
                        for file in data:
                            if (
                                query["name"]["$regex"] in file["name"]
                                and query["mimeType"] == file["mimeType"]
                            ):
                                result_file.append(file)
                        return result_file
                    else:
                        for file in data:
                            if query["name"]["$regex"] in file["name"]:
                                result_file.append(file)
                        return result_file
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
                    if query["path"] is None:
                        with open(
                            absolute_path_to_data + "/snapshot1_files_with_no_path.json"
                        ) as json_file2:
                            data = json.load(json_file2)
                            for file in data:
                                if query["path"] == file["path"]:
                                    result_file.append(file)
                            return result_file
                    elif query["path"] and "$regex" in query["path"]:
                        for file in data:
                            if query["path"]["$regex"] in file["path"]:
                                result_file.append(file)
                        return result_file
                    else:
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
                if "type" in query:
                    for permission in data:
                        if permission["type"] == query["type"]:
                            target_permissions.append(permission)
                    return target_permissions
                if "role" in query:
                    if "$ne" in query["role"]:
                        if "inherited" in query:
                            for permission in data:
                                if permission["emailAddress"]:
                                    if (
                                        permission["role"] != "owner"
                                        and query["emailAddress"]
                                        in permission["emailAddress"]
                                        and permission["inherited"] is False
                                    ):
                                        target_permissions.append(permission)
                        else:
                            for permission in data:
                                if permission["role"] != "owner":
                                    if permission["emailAddress"] is not None:
                                        if (
                                            query["emailAddress"]["$regex"]
                                            in permission["emailAddress"]
                                        ):
                                            target_permissions.append(permission)
                        return target_permissions
                    else:
                        for permission in data:
                            if (
                                query["role"] == permission["role"]
                                and query["emailAddress"] == permission["emailAddress"]
                            ):
                                target_permissions.append(permission)
                        return target_permissions
                if "file_id" in query:
                    for permission in data:
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
