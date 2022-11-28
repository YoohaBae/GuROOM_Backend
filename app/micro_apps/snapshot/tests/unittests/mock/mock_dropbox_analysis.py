import json

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"


class MockAnalysis:
    def __init__(self, user_id):
        self.db = None

        self.base_path = ""

    @classmethod
    def calculate_permission_and_path(cls, snapshot_name):
        pass

    @classmethod
    def get_empty_sharing_differences(cls, base_permissions, compare_permissions):
        return [], [], []

    @classmethod
    def get_sharing_differences(cls, base_permissions, compare_permissions):
        return [{"id": "PERMISSIONID1"}], [], [{"id": "PERMISSIONID5"}]

    @classmethod
    def compare_two_file_snapshots(
        cls,
        base_snapshot_name,
        compare_snapshot_name,
        base_snapshot_files,
        compare_snapshot_files,
    ):
        return [
            {
                "id": "FILEID1",
                "additional_base_file_snapshot_permissions": [{"id": "PERMISSIONID1"}],
            }
        ]

    @classmethod
    def tag_files_and_permissions_with_violation(cls, snapshot_name, files, acr):
        permissions = []
        with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
            data = json.load(json_file)
        for file in files:
            for permission in data:
                if permission["file_id"] == file["id"]:
                    permissions.append(permission)
        return files, permissions
