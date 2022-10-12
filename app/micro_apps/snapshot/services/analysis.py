from database import DataBase

collection_name = "file_snapshots"


class Analysis:
    def __init__(self, user_id, snapshot_name):
        self.db = DataBase(user_id)
        self.snapshot_name = snapshot_name

    def calculate_permission_and_path(self):
        shared_folder_id = None
        my_drive_folder_id = self.db.get_root_id(collection_name)

        # bfs for my_drive
        visited_file_ids = []
        path = "/MyDrive"
        inherited_permissions = []
        self.dfs(visited_file_ids, my_drive_folder_id, path, inherited_permissions)

        # bfs for shared_drive
        visited_file_ids = []
        path = "SharedWithMe"
        inherited_permissions = []
        self.dfs(visited_file_ids, shared_folder_id, path, inherited_permissions)

    def dfs(self, visited, file_id, parent_path, parent_inherited_permission):
        visited.append(file_id)

        children_file_ids = self.db.get_file_under_folder(
            self.snapshot_name, folder_id=file_id
        )
        for children_id in children_file_ids:
            if children_id not in visited:
                (
                    path,
                    inherited_permission,
                ) = self.db.update_inherited_permission_and_path(
                    self.snapshot_name,
                    children_id,
                    parent_path,
                    parent_inherited_permission,
                )
                visited.append(children_id)
                self.dfs(visited, children_id, path, inherited_permission)
