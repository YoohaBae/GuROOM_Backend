collection_name = "file_snapshots"


class Analysis:
    def __init__(self):
        pass

    def calculate_permission_and_path(self, snapshot_name):
        raise NotImplementedError("Must be implemented by child class")

    def dfs(
        self, visited, curr_folder_path, curr_permission, snapshot_name, file_id=None
    ):
        raise NotImplementedError("Must be implemented by child class")

    def get_sharing_differences(self, base_permissions, compare_permissions):
        raise NotImplementedError("Must be implemented by child class")

    def get_sharing_changes(
        self, base_permissions, compare_permissions, remaining_permission_ids
    ):
        raise NotImplementedError("Must be implemented by child class")

    def compare_two_file_snapshots(
        self,
        base_snapshot_name,
        compare_snapshot_name,
        base_snapshot_files,
        compare_snapshot_files,
    ):
        raise NotImplementedError("Must be implemented by child class")
