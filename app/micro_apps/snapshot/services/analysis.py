from .database import DataBase
from app.utils.util import ListOfDictsComparor

collection_name = "file_snapshots"


class Analysis:
    def __init__(self, user_id, snapshot_name):
        self.db = DataBase(user_id)
        self.snapshot_name = snapshot_name
        self.shared_with_me_drive_path = "/SharedWithMe"
        self.my_drive_path = "/MyDrive"

    def calculate_permission_and_path(self):
        shared_with_me_folder_id = None
        my_drive_folder_id = self.db.get_root_id(self.snapshot_name)
        shared_drives = self.db.get_shared_drives(self.snapshot_name)

        # dfs for my_drive
        visited_file_ids = []
        self.dfs(visited_file_ids, self.my_drive_path, [], my_drive_folder_id)

        # dfs for shared_with_me
        visited_file_ids = []
        self.dfs(
            visited_file_ids,
            self.shared_with_me_drive_path,
            [],
            shared_with_me_folder_id,
        )

        # dfs for all shared_drives
        visited_file_ids = []
        for shared_drive in shared_drives:
            path = "/" + shared_drive["name"]
            folder_id = shared_drive["id"]
            # updates only the path for shared drives as they have separate inherit direct permissions
            self.dfs_shared(visited_file_ids, path, folder_id)
        self.update_inherited_shared()

    def update_inherited_shared(self):
        all_permissions_of_snapshot = self.db.get_all_permission_of_snapshot(
            self.snapshot_name
        )
        for permission in all_permissions_of_snapshot:
            if (
                "permissionDetails" in permission
                and len(permission["permissionDetails"]) == 1
            ):
                inherited_from_id = permission["permissionDetails"][0]["inheritedFrom"]
                inherited = permission["permissionDetails"][0]["inherited"]
                if inherited_from_id is not None and inherited:
                    inherited_from_path = self.db.get_path_of_file(
                        self.snapshot_name, inherited_from_id
                    )
                    self.db.update_inherited_and_inherited_from(
                        self.snapshot_name,
                        permission["file_id"],
                        permission["id"],
                        inherited,
                        inherited_from_path,
                    )

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

    def dfs_shared(self, visited, curr_folder_path, file_id=None):
        visited.append(file_id)
        child_files = self.db.get_file_under_folder(
            self.snapshot_name, folder_id=file_id
        )
        for child_file in child_files:
            child_file_id = child_file["id"]
            if child_file_id not in visited:
                child_path = self.db.update_path(
                    self.snapshot_name, curr_folder_path, child_file_id
                )
                self.dfs_shared(visited, child_path, child_file_id)

    def get_sharing_differences(self, base_permissions, compare_permissions):
        comparor = ListOfDictsComparor()
        base_permission_ids = [permission["id"] for permission in base_permissions]
        compare_permission_ids = [
            permission["id"] for permission in compare_permissions
        ]
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
