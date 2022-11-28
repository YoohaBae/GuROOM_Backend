import os
import logging
from app.services.mongodb import MongoDB


class SnapshotDatabase:
    def __init__(self, user_id):
        url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB_NAME")
        format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=format)
        self.user_id = user_id
        self.logger = logging.getLogger()
        self._db = MongoDB(url, db_name)

    def create_file_snapshot(self, **args):
        raise NotImplementedError("Must be implemented by child class")

    def get_file_snapshot_names(self):
        raise NotImplementedError("Must be implemented by child class")

    def get_file_under_folder(
        self, snapshot_name, offset=None, limit=None, folder_id=None
    ):
        raise NotImplementedError("Must be implemented by child class")

    def edit_file_snapshot_name(self, snapshot_name, new_snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def edit_all_collections_starting_with(self, query, new_snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def delete_file_snapshot(self, snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def delete_all_collections_starting_with(self, query):
        raise NotImplementedError("Must be implemented by child class")

    def get_file_name(self, snapshot_name, file_id):
        raise NotImplementedError("Must be implemented by child class")

    def get_all_permission_of_file(self, snapshot_name, file_id):
        raise NotImplementedError("Must be implemented by child class")

    def get_all_files_of_snapshot(self, snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def get_path_of_file(self, snapshot_name, file_id):
        raise NotImplementedError("Must be implemented by child class")

    def get_all_members_from_permissions(self, snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def get_files_with_path_regex(self, snapshot_name, path):
        raise NotImplementedError("Must be implemented by child class")

    def get_files_that_match_file_name_regex(self, snapshot_name, file_name):
        raise NotImplementedError("Must be implemented by child class")

    def get_files_with_certain_role(self, snapshot_name, role_name, email):
        raise NotImplementedError("Must be implemented by child class")

    def get_folders_with_regex(self, snapshot_name, folder_name):
        raise NotImplementedError("Must be implemented by child class")

    def get_directly_shared_permissions_file_ids(self, snapshot_name, email):
        raise NotImplementedError("Must be implemented by child class")

    # def get_files_with_sharing_user(self, snapshot_name, email):
    #     raise NotImplementedError("Must be implemented by child class")

    def get_files_of_file_ids(self, snapshot_name, file_ids):
        raise NotImplementedError("Must be implemented by child class")

    def get_file_ids_shared_with_users_from_domain(self, snapshot_name, domain):
        raise NotImplementedError("Must be implemented by child class")

    def get_not_shared_files(self, snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    # def get_file_ids_shared_with_anyone(self, snapshot_name):
    #     raise NotImplementedError("Must be implemented by child class")

    def create_access_control_requirement(self, access_control):
        raise NotImplementedError("Must be implemented by child class")

    def get_access_control_requirements(self):
        raise NotImplementedError("Must be implemented by child class")

    def check_duplicate_access_control_requirement(self, access_control):
        raise NotImplementedError("Must be implemented by child class")

    def get_access_control_requirement(self, access_control_requirement_name):
        raise NotImplementedError("Must be implemented by child class")
