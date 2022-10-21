absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


class MockAnalysis:
    def __init__(self, user_id):
        self.db = None

        self.shared_with_me_drive_path = "/SharedWithMe"
        self.my_drive_path = "/MyDrive"

    def calculate_permission_and_path(self, snapshot_name):
        pass

    def get_empty_sharing_differences(self, base_permissions, compare_permissions):
        return [], [], []

    def get_sharing_differences(self, base_permissions, compare_permissions):
        return [{"id": "PERMISSIONID1"}], [], [{"id": "PERMISSIONID5"}]

    def compare_two_file_snapshots(
        self,
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
