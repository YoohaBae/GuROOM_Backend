import json
import logging

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"
mock_user_id = "MOCK_USER_ID1"

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s:"
    "%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


class MockDropboxDrive:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @classmethod
    def get_root_file_id(cls, token):
        return "ROOTID1"

    @classmethod
    def get_shared_drives(cls, token, next_page_token=None):
        with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
            data = json.load(json_file)
            return data[0]["shared_drives"], None

    @classmethod
    def get_files(cls, token, next_page_token=None):
        with open(absolute_path_to_data + "/snapshot1_raw_files.json") as json_file:
            data = json.load(json_file)
            return data[0:4], data[4:], None

    @classmethod
    def get_files_next_page_token(cls, token, next_page_token=None):
        with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
            data = json.load(json_file)
            return data[0:4], data[4:], "NEXT_PAGE_TOKEN"

    @classmethod
    def get_permissions_of_files(cls, token, file_ids):
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            permissions = []
            for permission in permissions:
                if permission["file_id"] == data["id"]:
                    permissions.append(permission)
            return permissions

    @classmethod
    def get_permissions_of_shared_folders(cls, token, shared_folder_ids):
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
            permissions = []
            for permission in permissions:
                if permission["driveId"] == data["driveId"]:
                    permissions.append(permission)
            return permissions
