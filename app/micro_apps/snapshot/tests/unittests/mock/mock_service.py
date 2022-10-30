import json
import asyncio

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


class MockService:
    @classmethod
    def get_user_id_from_token(cls, access_token):
        return "MOCK_USER_ID1"

    @classmethod
    def get_user_email_from_token(cls, access_token):
        return "MOCK_USER_EMAIL1"

    @classmethod
    def get_root_id_from_api(cls, access_token):
        return "MOCK_ROOT_ID1"

    @classmethod
    def get_all_shared_drives_from_api(cls, access_token):
        with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
            data = json.load(json_file)
            return data[0]["shared_drives"]

    @classmethod
    def get_all_files_from_api(cls, access_token):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_none(cls, *args, **kwargs):
        return None

    @classmethod
    def create_file_snapshot(
        cls, user_id, snapshot_name, files, root_id, shared_drives
    ):
        return True

    @classmethod
    def perform_inherit_direct_permission_analysis(cls, user_id, snapshot_name):
        return True

    @classmethod
    def get_false(cls, *args, **kwargs):
        return False

    @classmethod
    def delete_file_snapshot(cls, user_id, snapshot_name):
        return True

    @classmethod
    def edit_file_snapshot_name(cls, user_id, snapshot_name, new_snapshot_name):
        return True

    @classmethod
    def get_file_snapshot_names(cls, user_id):
        with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_shared_drives(cls, user_id, snapshot_name):
        with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
            data = json.load(json_file)
            return data[0]["shared_drives"]

    @classmethod
    def get_files_of_my_drive(cls, user_id, snapshot_name, offset, limit):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_files_of_shared_with_me(cls, user_id, snapshot_name, offset, limit):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_files_of_shared_drive(
        cls, user_id, snapshot_name, folder_id, offset, limit
    ):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_files_of_folder(cls, user_id, snapshot_name, folder_id, offset, limit):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_permission_of_files(cls, user_id, snapshot_name, files):
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_file_folder_sharing_difference(cls, user_id, snapshot_name, file_id):
        return [], [], []

    @classmethod
    def get_difference_of_two_snapshots(
        cls, user_id, base_snapshot_name, compare_snapshot_name
    ):
        return []

    @classmethod
    def scratch_group_memberships_from_file(cls, file):
        with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
            data = json.load(json_file)
            function = asyncio.Future()
            function.set_result(data[0]["memberships"])
            return function

    @classmethod
    def get_invalid_scratch_group_memberships_from_file(cls, file):
        function = asyncio.Future()
        function.set_result(None)
        return function

    @classmethod
    def create_group_snapshot(
        cls, user_id, group_name, group_email, create_time, memberships
    ):
        return True

    @classmethod
    def get_recent_group_membership_snapshots(cls, user_id):
        with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_recent_queries(cls, access_token):
        with open(absolute_path_to_data + "/auth.json") as json_file:
            data = json.load(json_file)
            return data[0]["recent_queries"]

    @classmethod
    def get_unique_members_of_file_snapshot(cls, user_id, snapshot_name, is_groups):
        return []

    @classmethod
    def validate_query(cls, user_id, email, snapshot_name, query):
        return True

    @classmethod
    def validate_query_invalid(cls, user_id, email, snapshot_name, query):
        return "Invalid Boolean Operator: not is not one of: and, or, -"

    @classmethod
    def process_query_search(cls, user_id, email, snapshot_name, query, is_groups):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data
