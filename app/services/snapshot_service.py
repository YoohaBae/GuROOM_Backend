import logging


class SnapshotService:
    def __init__(self):
        format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=format)
        self.logger = logging.getLogger()

    def get_user_id_from_access_token(self, access_token):
        raise NotImplementedError("Must be implemented by child class")

    def get_user_email_from_token(self, access_token):
        raise NotImplementedError("Must be implemented by child class")

    def perform_inherit_direct_permission_analysis(self, user_id, snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def delete_file_snapshot(self, user_id, snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def edit_file_snapshot_name(self, user_id, snapshot_name, new_snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def get_file_snapshot_names(self, user_id):
        raise NotImplementedError("Must be implemented by child class")

    def get_files_of_folder(
        self, user_id, snapshot_name, folder_id, offset=None, limit=None
    ):
        raise NotImplementedError("Must be implemented by child class")

    def get_permission_of_files(self, user_id, snapshot_name, files):
        raise NotImplementedError("Must be implemented by child class")

    def get_files_with_diff_permission_from_folder(self, user_id, snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def get_file_folder_sharing_difference(self, user_id, snapshot_name, file_id):
        raise NotImplementedError("Must be implemented by child class")

    def get_sharing_difference_of_two_files(
        self, user_id, snapshot_name, base_file_id, compare_file_id
    ):
        raise NotImplementedError("Must be implemented by child class")

    def get_sharing_difference_of_two_files_different_snapshots(
        self, user_id, base_snapshot_name, compare_snapshot_name, file_id
    ):
        raise NotImplementedError("Must be implemented by child class")

    def get_difference_of_two_snapshots(
        self, user_id, base_snapshot_name, compare_snapshot_name
    ):
        raise NotImplementedError("Must be implemented by child class")

    def separate_permission_to_inherit_and_direct(self, permissions):
        raise NotImplementedError("Must be implemented by child class")

    def process_query_search(self, *args, **kwargs):
        raise NotImplementedError("Must be implemented by child class")

    def validate_query(self, user_id, user_email, snapshot_name, query):
        raise NotImplementedError("Must be implemented by child class")

    def get_unique_members_of_file_snapshot(self, *args, **kwargs):
        raise NotImplementedError("Must be implemented by child class")

    def get_recent_queries(self, email):
        raise NotImplementedError("Must be implemented by child class")
