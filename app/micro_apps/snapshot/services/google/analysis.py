from app.services.analysis import Analysis
from app.micro_apps.snapshot.services.google.database import GoogleSnapshotDatabase
from app.utils.util import (
    fix_key_in_dict_of_roots,
    remove_key_from_list_of_dict,
    ListOfDictsComparor,
)
from deepdiff import DeepDiff

collection_name = "file_snapshots"


class GoogleAnalysis(Analysis):
    def __init__(self, user_id):  # pragma: no cover
        super().__init__()
        self._snapshot_db = GoogleSnapshotDatabase(user_id)
        self.shared_with_me_drive_path = "/SharedWithMe"
        self.my_drive_path = "/MyDrive"

    def calculate_permission_and_path(self, snapshot_name):
        shared_with_me_folder_id = None
        my_drive_folder_id = self._snapshot_db.get_root_id(snapshot_name)
        shared_drives = self._snapshot_db.get_shared_drives(snapshot_name)

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
        all_permissions_of_snapshot = self._snapshot_db.get_all_permission_of_snapshot(
            snapshot_name
        )
        # iterate through the entire permission of snapshot
        for permission in all_permissions_of_snapshot:
            # if permissionDetails exist: for shared drive only
            if (
                "permissionDetails" in permission
                and len(permission["permissionDetails"]) == 1
            ):
                # move the value of permissionDetails to (inherited and inherited_from field)
                inherited_from_id = permission["permissionDetails"][0]["inheritedFrom"]
                inherited = permission["permissionDetails"][0]["inherited"]
                if inherited_from_id is not None and inherited:
                    # get path of file
                    inherited_from_path = self._snapshot_db.get_path_of_file(
                        snapshot_name, inherited_from_id
                    )
                    # update the fields
                    self._snapshot_db.update_inherited_and_inherited_from(
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
        child_files = self._snapshot_db.get_file_under_folder(
            snapshot_name, folder_id=file_id
        )
        # iterate through children files
        for child_file in child_files:
            child_file_id = child_file["id"]
            # if not visited
            if child_file_id not in visited:
                # update the path
                # update permissions to inherited or not inherited
                (
                    child_path,
                    child_permissions,
                ) = self._snapshot_db.update_path_and_permissions(
                    snapshot_name, curr_folder_path, curr_permission, child_file_id
                )
                # perform dfs on children files
                self.dfs(
                    visited, child_path, child_permissions, snapshot_name, child_file_id
                )

    def dfs_shared(self, visited, curr_folder_path, snapshot_name, file_id=None):
        visited.append(file_id)
        child_files = self._snapshot_db.get_file_under_folder(
            snapshot_name, folder_id=file_id
        )
        # iterate through children files
        for child_file in child_files:
            child_file_id = child_file["id"]
            # if not visited
            if child_file_id not in visited:
                # update the path of file
                # (doesn't need to update inherited or not as it is shared drive)
                child_path = self._snapshot_db.update_path(
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

        # get ids of what base permission has more
        base_permission_more_ids = ListOfDictsComparor.difference(
            base_permission_ids, compare_permission_ids
        )

        # get ids of what compare permission has more
        compare_permission_more_ids = ListOfDictsComparor.difference(
            compare_permission_ids, base_permission_ids
        )

        # get the remaining permission ids
        remaining_permission_ids = ListOfDictsComparor.intersection(
            base_permission_ids, compare_permission_ids
        )

        # check if any of the remaining permission ids has permission changed
        sharing_changes = self.get_sharing_changes(
            base_permissions, compare_permissions, remaining_permission_ids
        )

        # get the permission for base_permission_more_ids
        base_permission_more = [
            x for x in base_permissions if x["id"] in base_permission_more_ids
        ]
        # get the permission for compare_permission_more_ids
        compare_permission_more = [
            x for x in compare_permissions if x["id"] in compare_permission_more_ids
        ]
        return base_permission_more, sharing_changes, compare_permission_more

    def get_sharing_changes(
        self, base_permissions, compare_permissions, remaining_permission_ids
    ):
        # list of permissions where permission has changed
        changed_permissions = []
        for remain_id in remaining_permission_ids:
            # get the permission object from base permission using id
            equal_base_permission = [
                p for p in base_permissions if p["id"] == remain_id
            ][0]
            # get the permission object from base permission using id
            equal_compare_permission = [
                p for p in compare_permissions if p["id"] == remain_id
            ][0]
            # get difference between two permissions using deepdiff
            change_deepdiff = DeepDiff(
                equal_base_permission, equal_compare_permission, verbose_level=2
            )
            # there is no difference
            if change_deepdiff == {}:
                continue
            values_changed_dict, types_changed_dict = {}, {}
            # value of permission has changed
            if "values_changed" in change_deepdiff:
                values_changed_dict = change_deepdiff["values_changed"]
            # type of permission has changed
            if "types_changed" in change_deepdiff:
                types_changed_dict = change_deepdiff["types_changed"]

            # fix format of the result of deepdiff
            values_changed_dict = fix_key_in_dict_of_roots(values_changed_dict)
            types_changed_dict = fix_key_in_dict_of_roots(types_changed_dict)

            # format the data into a dictionary
            change_data = {
                "from": equal_base_permission,
                "to": equal_compare_permission,
                "value_changed": values_changed_dict,
                "type_changed": types_changed_dict,
            }

            # add data to changed permissions
            changed_permissions.append(change_data)
        return changed_permissions

    def compare_two_file_snapshots(
        self,
        base_snapshot_name,
        compare_snapshot_name,
        base_snapshot_files,
        compare_snapshot_files,
    ):
        # list of files that are newly added or has different permissions
        different_files = []
        # list of file ids for base snapshot
        base_snapshot_files_ids = [x["id"] for x in base_snapshot_files]
        for compare_snapshot_file in compare_snapshot_files:
            file_id = compare_snapshot_file["id"]
            # if file was newly added
            if file_id not in base_snapshot_files_ids:
                compare_snapshot_file["additional_base_file_snapshot_permissions"] = []
                # store permissions of file in additional compare file snapshot permissions
                compare_snapshot_file[
                    "additional_compare_file_snapshot_permissions"
                ] = self._snapshot_db.get_all_permission_of_file(
                    compare_snapshot_name, file_id
                )
                # there is no changed permissions
                compare_snapshot_file["changed_permissions"] = []
                # add it to different files
                different_files.append(compare_snapshot_file)
                # go to next file
                continue
            # permissions of file in base snapshot
            base_permissions = self._snapshot_db.get_all_permission_of_file(
                base_snapshot_name, file_id
            )
            # permissions of file in compare snapshot
            compare_permissions = self._snapshot_db.get_all_permission_of_file(
                compare_snapshot_name, file_id
            )
            # compare the permissions of file
            (
                base_more_permissions,
                changes,
                compare_more_permissions,
            ) = self.get_sharing_differences(base_permissions, compare_permissions)
            # there is a different permission
            if (
                len(base_more_permissions) != 0
                or len(changes) != 0
                or len(compare_more_permissions) != 0
            ):
                # permissions that base snapshot has more
                compare_snapshot_file[
                    "additional_base_file_snapshot_permissions"
                ] = base_more_permissions
                # permissions that compare snapshot has more
                compare_snapshot_file[
                    "additional_compare_file_snapshot_permissions"
                ] = compare_more_permissions
                # permissions where fields were changed
                compare_snapshot_file["changed_permissions"] = changes
                # add file to different files
                different_files.append(compare_snapshot_file)
        return different_files

    def tag_files_and_permissions_with_violation_groups(
        self, snapshot_name, files, AR, AW, DR, DW
    ):
        violated_files_permissions = []
        violated_files = []
        for file in files:
            permissions = self._snapshot_db.get_all_permission_of_file(
                snapshot_name, file["id"]
            )
            file_violation = False
            for permission in permissions:
                emailAddress = permission["emailAddress"]
                group_mails = self._snapshot_db.get_group_emails_of_user_email(
                    emailAddress
                )
                role = permission["role"]
                violation = False
                violation_type = []
                violation_description = []
                if len(AR) != 0:
                    # role of permission can read
                    # email not in AR and not in AW
                    group_violation_tag = True
                    for mail in group_mails:
                        if mail in AR or mail in AW:
                            group_violation_tag = False
                            break
                    if group_violation_tag:
                        if emailAddress not in AR and emailAddress not in AW:
                            # violation
                            violation = True
                            violation_type.append("AR")
                            violation_description.append(
                                f"{emailAddress} is not in Allowed Readers"
                            )

                if len(AW) != 0:
                    # role of permission can write
                    if role in ["writer", "fileOrganizer", "organizer", "owner"]:
                        # emailAddress is not in AW
                        group_violation_tag = True
                        for mail in group_mails:
                            if mail in AW:
                                group_violation_tag = False
                                break
                        # violation
                        if group_violation_tag:
                            if emailAddress not in AW:
                                violation = True
                                violation_type.append("AW")
                                violation_description.append(
                                    f"{emailAddress} is not in Allowed Writers"
                                )

                if len(DR) != 0:
                    # role of permission can read
                    for mail in group_mails:
                        if mail in DR:
                            violation = True
                            violation_type.append("DR")
                            violation_description.append(
                                f"{emailAddress} is a member of group {mail} which is in Denied Readers"
                            )
                            break
                    # email in DR
                    if not violation:
                        if emailAddress in DR:
                            # violation
                            violation = True
                            violation_type.append("DR")
                            violation_description.append(
                                f"{emailAddress} is in Denied Readers"
                            )
                if len(DW) != 0:
                    # role of permission can write
                    if role in ["writer", "fileOrganizer", "organizer", "owner"]:
                        for mail in group_mails:
                            if mail in DW:
                                violation = True
                                violation_type.append("DW")
                                violation_description.append(
                                    f"{emailAddress} is a member of group {mail} which is in Denied Writers"
                                )
                                break
                        if not violation:
                            # email in DW
                            if emailAddress in DW:
                                # violation
                                violation = True
                                violation_type.append("AW")
                                violation_description.append(
                                    f"{emailAddress} is in Denied Writers"
                                )
                # save violation
                permission["violation"] = violation
                permission["violation_type"] = violation_type
                permission["violation_description"] = violation_description
                if violation:
                    file_violation = True
            file["violation"] = file_violation
            # if the file has violated ACR
            if file_violation:
                # add to violated files
                violated_files.append(file)
                # add permission to violated permissions
                violated_files_permissions.extend(permissions)
        return violated_files, violated_files_permissions

    def tag_files_and_permissions_with_violation_non_groups(
        self, snapshot_name, files, AR, AW, DR, DW
    ):
        violated_files_permissions = []
        violated_files = []

        for file in files:
            permissions = self._snapshot_db.get_all_permission_of_file(
                snapshot_name, file["id"]
            )
            file_violation = False
            for permission in permissions:
                emailAddress = permission["emailAddress"]
                role = permission["role"]
                violation = False
                violation_type = []
                violation_description = []
                if len(AR) != 0:
                    # role of permission can read
                    # email not in AR and not in AW
                    if emailAddress not in AR and emailAddress not in AW:
                        # violation
                        violation = True
                        violation_type.append("AR")
                        violation_description.append(
                            f"{emailAddress} is not in Allowed Readers"
                        )
                if len(AW) != 0:
                    # role of permission can write
                    if role in ["writer", "fileOrganizer", "organizer", "owner"]:
                        # emailAddress is not in AW
                        if emailAddress not in AW:
                            # violation
                            violation = True
                            violation_type.append("AW")
                            violation_description.append(
                                f"{emailAddress} is not in Allowed Writers"
                            )
                if len(DR) != 0:
                    # role of permission can read
                    # email in DR
                    if emailAddress in DR:
                        # violation
                        violation = True
                        violation_type.append("DR")
                        violation_description.append(
                            f"{emailAddress} is in Denied Readers"
                        )
                if len(DW) != 0:
                    # role of permission can write
                    if role in ["writer", "fileOrganizer", "organizer", "owner"]:
                        # email in DW
                        if emailAddress in DW:
                            # violation
                            violation = True
                            violation_type.append("AW")
                            violation_description.append(
                                f"{emailAddress} is in Denied Writers"
                            )
                # save violation
                permission["violation"] = violation
                permission["violation_type"] = violation_type
                permission["violation_description"] = violation_description
                if violation:
                    file_violation = True
            file["violation"] = file_violation

            # if the file has violated ACR
            if file_violation:
                # add to violated files
                violated_files.append(file)
                # add permission to violated permissions
                violated_files_permissions.extend(permissions)
        return violated_files, violated_files_permissions

    def tag_files_and_permissions_with_violation(
        self, snapshot_name, files, access_control_requirement
    ):
        AR = access_control_requirement["AR"]
        AW = access_control_requirement["AW"]
        DR = access_control_requirement["DR"]
        DW = access_control_requirement["DW"]
        Grp = access_control_requirement["Grp"]

        # groups:true
        if Grp:
            (
                violated_files,
                violated_files_permissions,
            ) = self.tag_files_and_permissions_with_violation_groups(
                snapshot_name, files, AR, AW, DR, DW
            )
        # groups:false
        else:
            (
                violated_files,
                violated_files_permissions,
            ) = self.tag_files_and_permissions_with_violation_non_groups(
                snapshot_name, files, AR, AW, DR, DW
            )
        return violated_files, violated_files_permissions
