"""
Google Drive Auth
"""
import logging
import requests
from .drive import Drive

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s:"
    "%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


class GoogleDrive(Drive):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def get_root_file_id(self, token):
        root_file_request = requests.get(
            "https://www.googleapis.com/drive/v3/files/root",
            params={"access_token": token},
        )

        status_code = getattr(root_file_request, "status_code")
        if status_code == 200:
            id = root_file_request.json()["id"]
            return id
        else:
            return None

    def get_files(self, token, next_page_token=None):
        if next_page_token is None:
            file_request = requests.get(
                "https://www.googleapis.com/drive/v3/files",
                params={
                    "access_token": token,
                    "fields": "files(kind, mimeType, id, name, parents, spaces, createdTime, modifiedTime, "
                    "sharedWithMeTime, sharingUser, owners, driveId, shared, ownedByMe, "
                    "capabilities, permissions, permissionIds, fullFileExtension, fileExtension, "
                    "size, contentRestrictions)",
                    "corpora": "allDrives",
                    "supportsAllDrives": True,
                    "includeItemsFromAllDrives": True,
                    "q": "trashed=False",
                    "pageSize": 500,
                    "orderBy": "folder",
                },
            )
        else:
            file_request = requests.get(
                "https://www.googleapis.com/drive/v3/files",
                params={
                    "access_token": token,
                    "fields": "files(kind, mimeType, id, name, parents, spaces, createdTime, modifiedTime, "
                    "sharedWithMeTime, sharingUser, owners, driveId, shared, ownedByMe, "
                    "capabilities, permissions, permissionIds, fullFileExtension, fileExtension, "
                    "size, contentRestrictions)",
                    "corpora": "allDrives",
                    "supportsAllDrives": True,
                    "includeItemsFromAllDrives": True,
                    "q": "trashed=False",
                    "pageToken": next_page_token,
                    "pageSize": 500,
                    "orderBy": "folder",
                },
            )
        status_code = getattr(file_request, "status_code")
        if status_code == 200:
            file_obj = file_request.json()
            next_page_token = None
            if "nextPageToken" in file_obj:
                next_page_token = file_obj["nextPageToken"]
            files = file_obj["files"]
            return files, next_page_token
        else:
            return None, None

    def get_shared_drives(self, token, next_page_token=None):
        if next_page_token is None:
            drive_request = requests.get(
                "https://www.googleapis.com/drive/v3/drives",
                params={
                    "access_token": token,
                    "pageSize": 100,
                    "useDomainAdminAccess": False,
                },
            )
        else:
            drive_request = requests.get(
                "https://www.googleapis.com/drive/v3/drives",
                params={
                    "access_token": token,
                    "pageSize": 100,
                    "useDomainAdminAccess": False,
                    "pageToken": next_page_token,
                },
            )
        status_code = getattr(drive_request, "status_code")
        if status_code == 200:
            drive_obj = drive_request.json()
            next_page_token = None
            if "nextPageToken" in drive_obj:
                next_page_token = drive_obj["nextPageToken"]
            drives = drive_obj["drives"]
            return drives, next_page_token
        else:
            return None, None

    def get_permission_detail_of_shared_drive_file(self, token, file_id, permission_id):
        permission_detail_request = requests.get(
            f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions/{permission_id}",
            params={
                "access_token": token,
                "fields": "*",
                "supportsAllDrives": True,
                "useDomainAdminAccess": False,
            },
        )

        status_code = getattr(permission_detail_request, "status_code")
        if status_code == 200:
            permission_detail = permission_detail_request.json()
            return permission_detail
        else:
            return None
