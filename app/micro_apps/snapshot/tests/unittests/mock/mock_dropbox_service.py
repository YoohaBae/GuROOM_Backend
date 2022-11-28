import json

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"


class MockService:
    @classmethod
    def get_user_id_from_access_token(cls, access_token):
        return "MOCK_USER_ID1"

    @classmethod
    def get_user_email_from_token(cls, access_token):
        return "MOCK_USER_EMAIL1"

    @classmethod
    def get_two_none(cls, *args, **kwargs):
        return None, None

    # @classmethod
    # def get_root_id_from_api(cls, access_token):
    #     return "MOCK_ROOT_ID1"
    #
    # @classmethod
    # def get_all_shared_drives_from_api(cls, access_token):
    #     with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
    #         data = json.load(json_file)
    #         return data[0]["shared_drives"]

    @classmethod
    def get_all_files_and_permissions_from_api(cls, access_token, email):
        files = []
        permissions = []
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            files = data
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            permissions = data
        return files, permissions

    @classmethod
    def get_none(cls, *args, **kwargs):
        return None

    @classmethod
    def create_file_snapshot(cls, user_id, snapshot_name, files, permissions):
        return True

    @classmethod
    def perform_inherit_direct_permission_analysis(cls, user_id, snapshot_name):
        return True

    @classmethod
    def get_false(cls, *args, **kwargs):
        return False

    @classmethod
    def get_true(cls, *args, **kwargs):
        return True

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

    # @classmethod
    # def get_shared_drives(cls, user_id, snapshot_name):
    #     with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
    #         data = json.load(json_file)
    #         return data[0]["shared_drives"]
    #
    # @classmethod
    # def get_files_of_my_drive(cls, user_id, snapshot_name, offset, limit):
    #     with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
    #         data = json.load(json_file)
    #         return data
    #
    # @classmethod
    # def get_files_of_shared_with_me(cls, user_id, snapshot_name, offset, limit):
    #     with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
    #         data = json.load(json_file)
    #         return data
    #
    # @classmethod
    # def get_files_of_shared_drive(
    #     cls, user_id, snapshot_name, folder_id, offset, limit
    # ):
    #     with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
    #         data = json.load(json_file)
    #         return data

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
    def get_recent_queries(cls, access_token):
        with open(absolute_path_to_data + "/auth.json") as json_file:
            data = json.load(json_file)
            return data[0]["recent_queries"]

    @classmethod
    def get_unique_members_of_file_snapshot(cls, user_id, snapshot_name):
        return []

    @classmethod
    def validate_query(cls, user_id, email, snapshot_name, query):
        return True

    @classmethod
    def validate_query_invalid(cls, user_id, email, snapshot_name, query):
        return "Invalid Boolean Operator: not is not one of: and, or, -"

    @classmethod
    def process_query_search(cls, user_id, email, snapshot_name, query):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data

    @classmethod
    def get_access_control_requirements(cls, user_id):
        with open(
            absolute_path_to_data + "/access_control_requirement.json"
        ) as json_file:
            data = json.load(json_file)
            return data
