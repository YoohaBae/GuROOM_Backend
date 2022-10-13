import logging
import json
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


def get_root_id(access_token):
    google_drive = GoogleDrive()
    try:
        root_id = google_drive.get_root_file_id(access_token)
        return root_id
    except Exception as error:
        logger.error(error)
        return None


def get_all_files(access_token):
    google_drive = GoogleDrive()
    try:
        files, next_page_token = google_drive.get_files(access_token)

        if files:
            # take snapshot
            while next_page_token is not None:
                new_files, next_page_token = google_drive.get_next_files(
                    access_token, next_page_token
                )
                files += new_files
        return files
    except Exception as error:
        logger.error(error)
        return None


def save_all_files(user_id, snapshot_name, files, root_id):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        snapshot_db.create_file_snapshot(snapshot_name, files, root_id)
        return True
    except Exception as error:
        logger.error(error)
        return False


def perform_inherit_direct_permission_analysis(user_id, snapshot_name):
    analysis = Analysis(user_id, snapshot_name)
    try:
        analysis.calculate_permission_and_path()
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


def get_files_of_shared_drive(user_id, snapshot_name, offset=None, limit=None):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        data = snapshot_db.get_file_under_folder(snapshot_name, offset, limit)
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


# def get_redundant_file_permissions(user_id, snapshot_name):
#     snapshot_db = SnapshotDataBase(user_id)
#     try:
#         all_permissions = snapshot_db.get_all_permission_of_snapshot(snapshot_name)
#         permission_grouped = group_permission_by_file_id(all_permissions)
#         for file_id in permission_grouped.keys():
#             inherit, direct = separate_permission_to_inherit_and_direct(permission_grouped[file_id])
#             get_permission_id_with_redundancy = None
#         return None
#     except Exception as error:
#         logger.error(error)
#         return None


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
