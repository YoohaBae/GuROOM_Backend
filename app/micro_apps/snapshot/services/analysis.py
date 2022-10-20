from .database import DataBase
from app.utils.util import (
    fix_key_in_dict_of_roots,
    remove_key_from_list_of_dict,
    ListOfDictsComparor,
)
from deepdiff import DeepDiff

collection_name = "file_snapshots"


class Analysis:
    def __init__(self, user_id):  # pragma: no cover
        self.db = DataBase(user_id)

        self.shared_with_me_drive_path = "/SharedWithMe"
        self.my_drive_path = "/MyDrive"

    def calculate_permission_and_path(self, snapshot_name):
        shared_with_me_folder_id = None
        my_drive_folder_id = self.db.get_root_id(snapshot_name)
        shared_drives = self.db.get_shared_drives(snapshot_name)

        # dfs for my_drive
        visited_file_ids = []
        self.dfs(
            visited_file_ids, self.my_drive_path, [], snapshot_name, my_drive_folder_id
        )

        # dfs for shared_with_me
        visited_file_ids = []
        self.dfs(
            visited_file_ids,
            self.shared_with_me_drive_path,
            [],
            snapshot_name,
            shared_with_me_folder_id,
        )

        # dfs for all shared_drives
        visited_file_ids = []
        for shared_drive in shared_drives:
            path = "/" + shared_drive["name"]
            folder_id = shared_drive["id"]
            # updates only the path for shared drives as they have separate inherit direct permissions
            self.dfs_shared(visited_file_ids, path, snapshot_name, folder_id)
        self.update_inherited_shared(snapshot_name)

    def update_inherited_shared(self, snapshot_name):
        all_permissions_of_snapshot = self.db.get_all_permission_of_snapshot(
            snapshot_name
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
                        snapshot_name, inherited_from_id
                    )
                    self.db.update_inherited_and_inherited_from(
                        snapshot_name,
                        permission["file_id"],
                        permission["id"],
                        inherited,
                        inherited_from_path,
                    )

    def dfs(
        self, visited, curr_folder_path, curr_permission, snapshot_name, file_id=None
    ):
        visited.append(file_id)
        child_files = self.db.get_file_under_folder(snapshot_name, folder_id=file_id)
        for child_file in child_files:
            child_file_id = child_file["id"]
            if child_file_id not in visited:
                child_path, child_permissions = self.db.update_path_and_permissions(
                    snapshot_name, curr_folder_path, curr_permission, child_file_id
                )
                self.dfs(
                    visited, child_path, child_permissions, snapshot_name, child_file_id
                )

    def dfs_shared(self, visited, curr_folder_path, snapshot_name, file_id=None):
        visited.append(file_id)
        child_files = self.db.get_file_under_folder(snapshot_name, folder_id=file_id)
        for child_file in child_files:
            child_file_id = child_file["id"]
            if child_file_id not in visited:
                child_path = self.db.update_path(
                    snapshot_name, curr_folder_path, child_file_id
                )
                self.dfs_shared(visited, child_path, snapshot_name, child_file_id)

    def get_sharing_differences(self, base_permissions, compare_permissions):
        delete_keys = ["file_id", "inherited_from", "inherited"]
        remove_key_from_list_of_dict(delete_keys, base_permissions)
        remove_key_from_list_of_dict(delete_keys, compare_permissions)

        # the id list of base permissions
        base_permission_ids = [x["id"] for x in base_permissions]

        # the id list of compare permissions
        compare_permission_ids = [x["id"] for x in compare_permissions]

        comparor = ListOfDictsComparor()

        base_permission_more_ids = comparor.difference(
            base_permission_ids, compare_permission_ids
        )
        compare_permission_more_ids = comparor.difference(
            compare_permission_ids, base_permission_ids
        )
        remaining_permission_ids = comparor.intersection(
            base_permission_ids, compare_permission_ids
        )
        sharing_changes = self.get_sharing_changes(
            base_permissions, compare_permissions, remaining_permission_ids
        )

        base_permission_more = [
            x for x in base_permissions if x["id"] in base_permission_more_ids
        ]
        compare_permission_more = [
            x for x in compare_permissions if x["id"] in compare_permission_more_ids
        ]
        return base_permission_more, sharing_changes, compare_permission_more

    def get_sharing_changes(
        self, base_permissions, compare_permissions, remaining_permission_ids
    ):
        changed_permissions = []
        for remain_id in remaining_permission_ids:
            equal_base_permission = [
                p for p in base_permissions if p["id"] == remain_id
            ][0]
            equal_compare_permission = [
                p for p in compare_permissions if p["id"] == remain_id
            ][0]
            change_deepdiff = DeepDiff(
                equal_base_permission, equal_compare_permission, verbose_level=2
            )
            if change_deepdiff == {}:
                continue
            values_changed_dict, types_changed_dict = {}, {}
            if "values_changed" in change_deepdiff:
                values_changed_dict = change_deepdiff["values_changed"]
            if "types_changed" in change_deepdiff:
                types_changed_dict = change_deepdiff["types_changed"]

            values_changed_dict = fix_key_in_dict_of_roots(values_changed_dict)
            types_changed_dict = fix_key_in_dict_of_roots(types_changed_dict)

            change_data = {
                "from": equal_base_permission,
                "to": equal_compare_permission,
                "value_changed": values_changed_dict,
                "type_changed": types_changed_dict,
            }
            changed_permissions.append(change_data)
        return changed_permissions

    def compare_two_file_snapshots(
        self,
        base_snapshot_name,
        compare_snapshot_name,
        base_snapshot_files,
        compare_snapshot_files,
    ):
        different_files = []
        base_snapshot_files_ids = [x["id"] for x in base_snapshot_files]
        for compare_snapshot_file in compare_snapshot_files:
            file_id = compare_snapshot_file["id"]
            # if file was newly added
            if file_id not in base_snapshot_files_ids:
                compare_snapshot_file["additional_base_file_snapshot_permissions"] = []
                compare_snapshot_file[
                    "additional_compare_file_snapshot_permissions"
                ] = self.db.get_all_permission_of_file(compare_snapshot_name, file_id)
                compare_snapshot_file["changed_permissions"] = []
                different_files.append(compare_snapshot_file)
                continue
            base_permissions = self.db.get_all_permission_of_file(
                base_snapshot_name, file_id
            )
            compare_permissions = self.db.get_all_permission_of_file(
                compare_snapshot_name, file_id
            )
            (
                base_more_permissions,
                changes,
                compare_more_permissions,
            ) = self.get_sharing_differences(base_permissions, compare_permissions)
            if (
                len(base_more_permissions) != 0
                or len(changes) != 0
                or len(compare_more_permissions) != 0
            ):
                compare_snapshot_file[
                    "additional_base_file_snapshot_permissions"
                ] = base_more_permissions
                compare_snapshot_file[
                    "additional_compare_file_snapshot_permissions"
                ] = compare_more_permissions
                compare_snapshot_file["changed_permissions"] = changes
                different_files.append(compare_snapshot_file)
        return different_files
