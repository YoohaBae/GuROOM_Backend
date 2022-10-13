from .database import DataBase

collection_name = "file_snapshots"


class Analysis:
    def __init__(self, user_id, snapshot_name):
        self.db = DataBase(user_id)
        self.snapshot_name = snapshot_name
        self.shared_drive_path = "/SharedDrive"
        self.my_drive_path = "/MyDrive"

    def calculate_permission_and_path(self):
        shared_folder_id = None
        my_drive_folder_id = self.db.get_root_id(self.snapshot_name)

        # dfs for my_drive
        visited_file_ids = []
        self.dfs(visited_file_ids, my_drive_folder_id, self.my_drive_path, [])

        # dfs for shared_drive
        visited_file_ids = []
        self.dfs(visited_file_ids, shared_folder_id, self.shared_drive_path, [])

    def dfs(self, visited, file_id, curr_folder_path, curr_permission):
        visited.append(file_id)
        child_files = self.db.get_file_under_folder(
            self.snapshot_name, folder_id=file_id
        )
        for child_file in child_files:
            child_file_id = child_file["id"]
            if child_file_id not in visited:
                child_path, child_permissions = self.db.update_path_and_permissions(self.snapshot_name,
                                                                                    curr_folder_path,
                                                                                    curr_permission, child_file_id)
                self.dfs(
                    visited, child_file_id, child_path, child_permissions
                )
