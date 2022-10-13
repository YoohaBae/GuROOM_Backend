from .database import DataBase
from app.utils.util import ListOfDictsComparor

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
        self.dfs(visited_file_ids, self.my_drive_path, [], my_drive_folder_id)

        # dfs for shared_drive
        visited_file_ids = []
        self.dfs(visited_file_ids, self.shared_drive_path, [], shared_folder_id)

    def dfs(self, visited, curr_folder_path, curr_permission, file_id=None):
        visited.append(file_id)
        child_files = self.db.get_file_under_folder(
            self.snapshot_name, folder_id=file_id
        )
        for child_file in child_files:
            child_file_id = child_file["id"]
            if child_file_id not in visited:
                child_path, child_permissions = self.db.update_path_and_permissions(
                    self.snapshot_name, curr_folder_path, curr_permission, child_file_id
                )
                self.dfs(visited, child_path, child_permissions, child_file_id)

    def get_sharing_differences(self, base_permissions, compare_permissions):
        comparor = ListOfDictsComparor()
        base_permission_ids = [permission['id'] for permission in base_permissions]
        compare_permission_ids = [permission['id'] for permission in compare_permissions]
        base_permission_more_ids = comparor.difference(
            base_permission_ids, compare_permission_ids
        )
        compare_permission_more_ids = comparor.difference(
            compare_permission_ids, base_permission_ids
        )
        intersection_permission_ids = comparor.intersection(
            base_permission_ids, compare_permission_ids
        )
        print(base_permissions)
        print(compare_permissions)
        print(base_permission_more_ids)
        print(compare_permission_more_ids)
        print(intersection_permission_ids)

    def compare_two_file_snapshots(self, base_snapshot_files, compare_snapshot_files):
        pass
