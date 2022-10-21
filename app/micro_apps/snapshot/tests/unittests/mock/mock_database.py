import json

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


class MockDB:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_root_id(self, snapshot_name):
        return "ROOTID1"

    def get_parent_id(self, snapshot_name, file_id):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["id"] == file_id:
                    return file["parents"][0]

    def create_file_snapshot(self, snapshot_name, data, root_id, shared_drives):
        pass

    def delete_file_snapshot(self, snapshot_name):
        pass

    def edit_file_snapshot_name(self, snapshot_name, new_snapshot_name):
        pass

    def get_file_snapshot_names(self):
        with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
            data = json.load(json_file)
            return data

    def get_shared_drives(self, snapshot_name):
        with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
            data = json.load(json_file)
            target_snapshot = None
            for file_snapshot in data:
                if file_snapshot["name"] == snapshot_name:
                    target_snapshot = file_snapshot
                    break
        return target_snapshot["shared_drives"]

    def get_file_under_folder(
        self, snapshot_name, offset=None, limit=None, folder_id=None
    ):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            target_files = []
            for file in data:
                if folder_id in file["parents"]:
                    target_files.append(file)
        return target_files

    def get_empty_file_under_folder(
        self, snapshot_name, offset=None, limit=None, folder_id=None
    ):
        return []

    def get_files_with_no_path(self, snapshot_name):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            target_files = []
            for file in data:
                if file["path"] is None:
                    target_files.append(file)
            return target_files

    def get_all_files_of_snapshot(self, snapshot_name):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data

    def get_path_of_file(self, snapshot_name, file_id):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["id"] == file_id:
                    return file["path"]
        return None

    def get_all_permission_of_snapshot(self, snapshot_name):
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            return data

    def update_inherited_and_inherited_from(
        self, snapshot_name, file_id, permission_id, inherited, inherited_from
    ):
        return None

    def update_path_and_permissions(
        self, snapshot_name, folder_path, folder_permission, file_id
    ):
        file_name = None
        new_permissions = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["id"] == file_id:
                    file_name = file["name"]
                    break
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            for permission in data:
                if permission["file_id"] == file_id:
                    new_permissions.append(permission)
        new_path = folder_path + "/" + file_name
        return new_path, new_permissions

    def update_path(self, snapshot_name, folder_path, file_id):
        file_name = None
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["id"] == file_id:
                    file_name = file["name"]
                    break
            new_path = folder_path + "/" + file_name
            return new_path

    def get_all_permission_of_file(self, snapshot_name, file_id):
        if snapshot_name == "FILE_SNAPSHOT1":
            with open(
                absolute_path_to_data + "/snapshot1_permissions.json"
            ) as json_file:
                data = json.load(json_file)
                target_permissions = []
                for permission in data:
                    if permission["file_id"] == file_id:
                        target_permissions.append(permission)
                return target_permissions
        elif snapshot_name == "FILE_SNAPSHOT2":
            with open(
                absolute_path_to_data + "/snapshot2_permissions.json"
            ) as json_file:
                data = json.load(json_file)
                target_permissions = []
                for permission in data:
                    if permission["file_id"] == file_id:
                        target_permissions.append(permission)
                return target_permissions

    def create_group_memberships_snapshot(
        self, group_name, group_email, create_time, memberships
    ):
        pass

    def get_all_group_membership_snapshots(self):
        with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
            data = json.load(json_file)
            return data
