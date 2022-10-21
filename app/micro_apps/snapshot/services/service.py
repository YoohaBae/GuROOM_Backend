import logging
import json
from collections import defaultdict
from bs4 import BeautifulSoup
from app.utils.util import DateTimeEncoder
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.auth.services.database import DataBase as UserDataBase
from app.micro_apps.snapshot.services.google_drive import GoogleDrive
from app.micro_apps.snapshot.services.analysis import Analysis
from app.micro_apps.snapshot.services.database import DataBase as SnapshotDataBase

format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"

logging.basicConfig(format=format)

logger = logging.getLogger()


def get_user_id_from_token(access_token):
    google_auth = GoogleAuth()
    user_db = UserDataBase()

    try:
        user = google_auth.get_user(access_token)
        user_obj = user_db.get_user(user["email"])
        user_id = str(user_obj["_id"])
        return user_id
    except Exception as error:
        logger.error(error)
        return None


def get_root_id_from_api(access_token):
    google_drive = GoogleDrive()
    try:
        root_id = google_drive.get_root_file_id(access_token)
        return root_id
    except Exception as error:
        logger.error(error)
        return None


def get_all_shared_drives_from_api(access_token):
    google_drive = GoogleDrive()
    try:
        drives, next_page_token = google_drive.get_shared_drives(access_token)

        if drives:
            # take snapshot
            while next_page_token is not None:
                new_drives, next_page_token = google_drive.get_shared_drives(
                    access_token, next_page_token
                )
                drives += new_drives
        return drives
    except Exception as error:
        logger.error(error)
        return None


def get_all_files_from_api(access_token):
    google_drive = GoogleDrive()
    try:
        files, next_page_token = google_drive.get_files(access_token)

        if files:
            # take snapshot
            while next_page_token is not None:
                new_files, next_page_token = google_drive.get_files(
                    access_token, next_page_token
                )
                files += new_files
        for file in files:
            shared_drive_permissions_for_file = []
            if (
                "driveId" in file
                and file["driveId"] is not None
                and "permissionIds" in file
                and "permissionIds" != []
            ):
                permission_ids = file["permissionIds"]
                for pid in permission_ids:
                    permission = (
                        google_drive.get_permission_detail_of_shared_drive_file(
                            access_token, file["id"], pid
                        )
                    )
                    shared_drive_permissions_for_file.append(permission)
                file["permissions"] = shared_drive_permissions_for_file
        return files
    except Exception as error:
        logger.error(error)
        return None


def create_file_snapshot(user_id, snapshot_name, files, root_id, shared_drives):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        snapshot_db.create_file_snapshot(snapshot_name, files, root_id, shared_drives)
        return True
    except Exception as error:
        logger.error(error)
        return False


def perform_inherit_direct_permission_analysis(user_id, snapshot_name):
    analysis = Analysis(user_id)
    try:
        analysis.calculate_permission_and_path(snapshot_name)
        return True
    except Exception as error:
        logger.error(error)
        return False


def delete_file_snapshot(user_id, snapshot_name):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        snapshot_db.delete_file_snapshot(snapshot_name)
        return True
    except Exception as error:
        logger.error(error)
        return False


def edit_file_snapshot_name(user_id, snapshot_name, new_snapshot_name):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        snapshot_db.edit_file_snapshot_name(snapshot_name, new_snapshot_name)
        return True
    except Exception as error:
        logger.error(error)
        return False


def get_file_snapshot_names(user_id):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        data = snapshot_db.get_file_snapshot_names()
        if len(data) == 0:
            return data
        names = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return names
    except Exception as error:
        logger.error(error)
        return None


def get_files_of_my_drive(user_id, snapshot_name, offset=None, limit=None):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        folder_id = snapshot_db.get_root_id(snapshot_name)
        data = snapshot_db.get_file_under_folder(
            snapshot_name, offset, limit, folder_id
        )
        if len(data) == 0:
            return []
        files = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return files
    except Exception as error:
        logger.error(error)
        return None


def get_files_of_shared_with_me(user_id, snapshot_name, offset=None, limit=None):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        # get all files with no parent attribute
        no_parent = snapshot_db.get_file_under_folder(snapshot_name)
        # get all files that do not have a path attribute -> has a parent but that parent is not in snapshot
        no_path = snapshot_db.get_files_with_no_path(snapshot_name)
        yes_path = []
        for no_path_file in no_path:
            no_path_file["path"] = "/SharedWithMe"
            yes_path.append(no_path_file)
        data = yes_path + no_parent
        # slice data
        if offset is not None and limit is not None:
            data = data[offset : (offset + limit)]  # noqa: E203
        if len(data) == 0:
            return []
        files = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return files
    except Exception as error:
        logger.error(error)
        return None


def get_files_of_shared_drive(
    user_id, snapshot_name, drive_id, offset=None, limit=None
):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        data = snapshot_db.get_file_under_folder(snapshot_name, offset, limit, drive_id)
        if len(data) == 0:
            return []
        files = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return files
    except Exception as error:
        logger.error(error)
        return None


def get_files_of_folder(user_id, snapshot_name, folder_id, offset=None, limit=None):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        data = snapshot_db.get_file_under_folder(
            snapshot_name, offset, limit, folder_id
        )
        if len(data) == 0:
            return []
        files = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return files
    except Exception as error:
        logger.error(error)
        return None


def get_permission_of_files(user_id, snapshot_name, files):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        permissions = []
        for file in files:
            permission = snapshot_db.get_all_permission_of_file(
                snapshot_name, file["id"]
            )
            permissions.extend(permission)
        permission_grouped = group_permission_by_file_id(permissions)
        for file_id in permission_grouped.keys():
            inherit, direct = separate_permission_to_inherit_and_direct(
                permission_grouped[file_id]
            )
            permission_grouped[file_id] = {
                "inherit_permissions": inherit,
                "direct_permissions": direct,
            }
        return permission_grouped
    except Exception as error:
        logger.error(error)
        return None


def get_files_with_diff_permission_from_folder(user_id, snapshot_name):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        all_files = snapshot_db.get_all_files_of_snapshot(snapshot_name)
        different_files = []
        root_id = snapshot_db.get_root_id(snapshot_name)
        shared_drives = snapshot_db.get_shared_drives(snapshot_name)
        shared_drive_ids = [x["id"] for x in shared_drives]
        for file in all_files:
            file_id = file["id"]
            parents = file["parents"]

            if (
                len(parents) == 0
                or parents[0] == root_id
                or parents[0] in shared_drive_ids
            ):
                continue

            folder_id = parents[0]

            file_permissions = snapshot_db.get_all_permission_of_file(
                snapshot_name, file_id
            )
            folder_permissions = snapshot_db.get_all_permission_of_file(
                snapshot_name, folder_id
            )

            # no folder with such id
            if folder_permissions is None:
                continue
            analysis = Analysis(user_id)
            (
                base_more_permissions,
                changes,
                compare_more_permissions,
            ) = analysis.get_sharing_differences(file_permissions, folder_permissions)
            if (
                len(base_more_permissions) != 0
                or len(changes) != 0
                or len(compare_more_permissions) != 0
            ):
                different_files.append(file)
        different_files = json.loads(json.dumps(different_files, cls=DateTimeEncoder))
        return different_files
    except Exception as error:
        logger.error(error)
        return None


def get_file_folder_sharing_difference(user_id, snapshot_name, file_id):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        folder_id = snapshot_db.get_parent_id(snapshot_name, file_id)
        folder_more, changes, file_more = get_sharing_difference_of_two_files(
            user_id, snapshot_name, folder_id, file_id
        )
        return folder_more, changes, file_more
    except Exception as error:
        logger.error(error)
        return None


def get_sharing_difference_of_two_files(
    user_id, snapshot_name, base_file_id, compare_file_id
):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        base_file_permissions = snapshot_db.get_all_permission_of_file(
            snapshot_name, base_file_id
        )
        compare_file_permissions = snapshot_db.get_all_permission_of_file(
            snapshot_name, compare_file_id
        )
        analysis = Analysis(user_id)
        (
            base_more_permissions,
            changes,
            compare_more_permissions,
        ) = analysis.get_sharing_differences(
            base_file_permissions, compare_file_permissions
        )
        return base_more_permissions, changes, compare_more_permissions
    except Exception as error:
        logger.error(error)
        return None


def get_sharing_difference_of_two_files_different_snapshots(
    user_id, base_snapshot_name, compare_snapshot_name, file_id
):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        base_snapshot_file_permissions = snapshot_db.get_all_permission_of_file(
            base_snapshot_name, file_id
        )
        compare_snapshot_file_permissions = snapshot_db.get_all_permission_of_file(
            compare_snapshot_name, file_id
        )
        analysis = Analysis(user_id)
        (
            base_more_permissions,
            changes,
            compare_more_permissions,
        ) = analysis.get_sharing_differences(
            base_snapshot_file_permissions, compare_snapshot_file_permissions
        )
        return base_more_permissions, changes, compare_more_permissions
    except Exception as error:
        logger.error(error)
        return None


def get_difference_of_two_snapshots(user_id, base_snapshot_name, compare_snapshot_name):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        base_snapshot_files = snapshot_db.get_all_files_of_snapshot(base_snapshot_name)
        compare_snapshot_files = snapshot_db.get_all_files_of_snapshot(
            compare_snapshot_name
        )
        # get new files: files that exist in compare_snapshot_files and not base_snapshot_files
        analysis = Analysis(user_id)
        data = analysis.compare_two_file_snapshots(
            base_snapshot_name,
            compare_snapshot_name,
            base_snapshot_files,
            compare_snapshot_files,
        )
        different_files = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return different_files
    except Exception as error:
        logger.error(error)
        return None


def get_shared_drives(user_id, snapshot_name):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        shared_drives = snapshot_db.get_shared_drives(snapshot_name)
        return shared_drives
    except Exception as error:
        logger.error(error)
        return None


def group_permission_by_file_id(permissions):
    permission_grouped = {}
    for permission in permissions:
        permission_grouped.setdefault(permission["file_id"], []).append(permission)
    return permission_grouped


def separate_permission_to_inherit_and_direct(permissions):
    inherit = []
    direct = []
    for permission in permissions:
        if permission["inherited"]:
            inherit.append(permission)
        else:
            direct.append(permission)
    return inherit, direct


def scratch_group_memberships_from_file(file):
    try:
        MEMBERSHIP_ROW_CLASS = "cXEmmc B9Uude hFgAsc J6Lkdb"
        MEMBERSHIP_NAME_CLASS = "LnLepd"
        MEMBERSHIP_ROLE_CLASS = "y7VPke"
        MEMBERSHIP_JOIN_DATE_CLASS = "y7VPke"
        memberships = []
        file.seek(0)
        html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        membership_html_rows = soup.find_all("div", {"class": MEMBERSHIP_ROW_CLASS})
        for membership_html in membership_html_rows:
            membership_html_member = membership_html.find_all(
                "span", {"class": "eois5"}
            )
            [
                membership_html_name,
                membership_html_role,
                membership_html_join_date,
            ] = membership_html_member
            name = membership_html_name.find(
                "div", {"class": MEMBERSHIP_NAME_CLASS}
            ).contents[0]
            role = membership_html_role.find(
                "div", {"class": MEMBERSHIP_ROLE_CLASS}
            ).contents[0]
            join_date = membership_html_join_date.find(
                "div", {"class": MEMBERSHIP_JOIN_DATE_CLASS}
            ).contents[0]
            membership = {"member": name, "role": role, "join_date": join_date}
            memberships.append(membership)
        return memberships
    except Exception as error:
        logger.error(error)
        return None


def create_group_snapshot(user_id, group_name, group_email, create_time, memberships):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        snapshot_db.create_group_memberships_snapshot(
            group_name, group_email, create_time, memberships
        )
        return True
    except Exception as error:
        logger.error(error)
        return False


def get_recent_group_membership_snapshots(user_id):
    snapshot_db = SnapshotDataBase(user_id)

    try:
        all_groups = snapshot_db.get_all_group_membership_snapshots()

        if all_groups == []:
            return []

        def def_value():
            return []

        grouped_groups = defaultdict(def_value)
        for group in all_groups:
            grouped_groups[group["group_name"]].append(group)
        result_groups = []
        for key in grouped_groups.keys():
            if len(grouped_groups[key]) > 1:
                recent = grouped_groups[key][0]
                for group in grouped_groups[key]:
                    if recent["create_time"] < group["create_time"]:
                        recent = group
                result_groups.append(recent)
            else:
                result_groups.append(grouped_groups[key][0])
        json_result_groups = json.loads(json.dumps(result_groups, cls=DateTimeEncoder))
        return json_result_groups
    except Exception as error:
        logger.error(error)
        return False
