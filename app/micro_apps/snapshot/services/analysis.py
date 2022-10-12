from .database import DataBase

collection_name = "file_snapshots"


class Analysis:
    def __init__(self, user_id, snapshot_name):
        self.db = DataBase(user_id)
        self.snapshot_name = snapshot_name

    def calculate_permission_and_path(self):
        shared_folder_id = None
        my_drive_folder_id = self.db.get_root_id(self.snapshot_name)

        # bfs for my_drive
        visited_file_ids = []
        path = "/MyDrive"

        self.dfs(visited_file_ids, my_drive_folder_id, path, [])

        # bfs for shared_drive
        visited_file_ids = []
        path = "/SharedWithMe"
        self.dfs(visited_file_ids, shared_folder_id, path, [])

    def dfs(self, visited, file_id, parent_path, parent_permissions):
        visited.append(file_id)
        children_files = self.db.get_file_under_folder(
            self.snapshot_name, folder_id=file_id
        )
        for children_file in children_files:
            if children_file["files"]["id"] not in visited:
                (
                    path,
                    updated_permissions,
                ) = self.db.update_inherited_permission_and_path(
                    self.snapshot_name,
                    children_file["files"]["id"],
                    parent_path,
                    parent_permissions,
                )
                self.dfs(
                    visited, children_file["files"]["id"], path, updated_permissions
                )
