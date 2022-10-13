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
        names = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return names
    except Exception as error:
        logger.error(error)
        return None


def get_files_of_my_drive(user_id, snapshot_name, offset, limit):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        folder_id = snapshot_db.get_root_id(snapshot_name)
        data = snapshot_db.get_file_under_folder(snapshot_name, offset, limit, folder_id)
        files = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return files
    except Exception as error:
        logger.error(error)
        return None


def get_files_of_shared_drive(user_id, snapshot_name, offset, limit):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        data = snapshot_db.get_file_under_folder(snapshot_name, offset, limit)
        files = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return files
    except Exception as error:
        logger.error(error)
        return None


def get_files_of_folder(user_id, snapshot_name, offset, limit, folder_id):
    snapshot_db = SnapshotDataBase(user_id)
    try:
        data = snapshot_db.get_file_under_folder(snapshot_name, offset, limit, folder_id)
        files = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return files
    except Exception as error:
        logger.error(error)
        return None