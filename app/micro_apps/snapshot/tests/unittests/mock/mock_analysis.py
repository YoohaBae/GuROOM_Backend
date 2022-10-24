absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


class MockAnalysis:
    def __init__(self, user_id):
        self.db = None

        self.shared_with_me_drive_path = "/SharedWithMe"
        self.my_drive_path = "/MyDrive"

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
