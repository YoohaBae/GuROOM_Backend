import json
import re
from app.micro_apps.snapshot.tests.data.dropbox.database_result import DataBaseResult

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"


class MockDB:
    def __init__(self, user_id):
        self.user_id = user_id

    @classmethod
    def create_file_snapshot(cls, snapshot_name, files, permissions):
        pass

    @classmethod
    def delete_file_snapshot(cls, snapshot_name):
        pass

    @classmethod
    def edit_file_snapshot_name(cls, snapshot_name, new_snapshot_name):
        pass

    @classmethod
    def get_file_snapshot_names(cls):
        with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_file_under_folder(cls, snapshot_name, offset=None, limit=None, path=None):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            target_files = []
            for file in data:
                if path == file["path"]:
                    target_files.append(file)
        return target_files

    @classmethod
    def get_all_files_of_snapshot(cls, snapshot_name):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def update_inherited_and_inherited_from(
        cls, snapshot_name, file_id, permission_id, inherited, inherited_from
    ):
        return None

    @classmethod
    def update_path_and_permissions(
        cls, snapshot_name, folder_path, folder_permission, file_id
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

    @classmethod
    def update_path(cls, snapshot_name, folder_path, file_id):
        file_name = None
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["id"] == file_id:
                    file_name = file["name"]
                    break
            new_path = folder_path + "/" + file_name
            return new_path

    @classmethod
    def get_all_permission_of_file(cls, snapshot_name, file_id):
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

    # @classmethod
    # def create_group_memberships_snapshot(
    #     cls, group_name, group_email, create_time, memberships
    # ):
    #     pass
    #
    # @classmethod
    # def get_all_group_membership_snapshots(cls):
    #     with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
    #         data = json.load(json_file)
    #         return data

    @classmethod
    def update_or_push_recent_queries(cls, email, query_obj):
        pass

    @classmethod
    def get_all_members_from_permissions(cls, snapshot_name):
        return DataBaseResult.all_members_from_permissions_result

    @classmethod
    def get_files_that_match_file_name_regex(cls, snapshot_name, regex_path):
        result_file = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if re.match(regex_path, file["name"]):
                    result_file.append(file)
            return result_file

    @classmethod
    def get_files_with_certain_role(cls, snapshot_name, role, email):
        target_permissions = []
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            for permission in data:
                if role == permission["role"] and email == permission["emailAddress"]:
                    target_permissions.append(permission)
        file_ids = [p["file_id"] for p in target_permissions]
        result_file = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["id"] in file_ids:
                    result_file.append(file)
            return result_file

    @classmethod
    def get_files_with_sharing_user(cls, snapshot_name, email):
        result_file = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["sharingUser"] is not None:
                    if "emailAddress" in file["sharingUser"]:
                        if file["sharingUser"]["emailAddress"] == email:
                            result_file.append(file)
            return result_file

    @classmethod
    def get_directly_shared_permissions_file_ids(cls, snapshot_name, email):
        target_permissions = []
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            for permission in data:
                if (
                    permission["role"] != "owner"
                    and email == permission["emailAddress"]
                    and permission["inherited"] is False
                ):
                    target_permissions.append(permission)
        file_ids = [p["file_id"] for p in target_permissions]
        return file_ids

    @classmethod
    def get_files_of_file_ids(cls, snapshot_name, unique_file_ids):
        result_file = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["id"] in unique_file_ids:
                    result_file.append(file)
            return result_file

    @classmethod
    def get_folders_with_regex(cls, snapshot_name, folder_name):
        result_file = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if folder_name in file["name"] and "folder" == file["mimeType"]:
                    result_file.append(file)
            return result_file

    @classmethod
    def get_files_with_path_regex(cls, snapshot_name, regex_path):
        result_file = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                regex_pattern = re.compile(regex_path)
                if re.match(regex_pattern, file["path"]):
                    result_file.append(file)
            return result_file

    @classmethod
    def get_not_shared_files(cls, snapshot_name):
        result_file = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["shared"] is None:
                    result_file.append(file)
            return result_file

    @classmethod
    def get_file_ids_shared_with_anyone(cls, snapshot_name):
        target_permissions = []
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            for permission in data:
                if permission["type"] == "anyone":
                    target_permissions.append(permission)
            return target_permissions

    @classmethod
    def get_file_ids_shared_with_users_from_domain(cls, snapshot_name, domain):
        target_permissions = []
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            for permission in data:
                if permission["emailAddress"]:
                    if (
                        permission["role"] != "owner"
                        and domain in permission["emailAddress"]
                        and permission["inherited"] is False
                    ):
                        target_permissions.append(permission)
        file_ids = [p["file_id"] for p in target_permissions]
        return file_ids

    @classmethod
    def get_access_control_requirement(cls, name):
        with open(
            absolute_path_to_data + "/access_control_requirement.json"
        ) as json_file:
            data = json.load(json_file)
            for acr in data:
                if acr["name"] == name:
                    return acr

    @classmethod
    def create_access_control_requirement(cls, access_control):
        pass

    @classmethod
    def check_duplicate_access_control_requirement(cls, access_control):
        with open(
            absolute_path_to_data + "/access_control_requirement.json"
        ) as json_file:
            data = json.load(json_file)
            for acr in data:
                if (
                    acr["AR"] == access_control["AR"]
                    and acr["AW"] == access_control["AW"]
                    and acr["DR"] == access_control["DR"]
                    and acr["DW"] == access_control["DW"]
                    and acr["Grp"] == access_control["Grp"]
                ):
                    return True
            return False

    @classmethod
    def get_access_control_requirements(cls):
        with open(
            absolute_path_to_data + "/access_control_requirement.json"
        ) as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def delete_access_control_requirement(cls, access_control_name):
        pass

    @classmethod
    def get_file_id_of_name(cls, snapshot_name, file_name):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["name"] == file_name:
                    return file["id"]
            return None

    @classmethod
    def get_path_of_file(cls, snapshot_name, file_id):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            for file in data:
                if file["id"] == file_id:
                    return file["path"]
            return None

    @classmethod
    def check_duplicate_file_snapshot_name(cls, snapshot_name):
        return False
