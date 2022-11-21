"""
Dropbox Drive
"""
import requests
from app.micro_apps.snapshot.services.models.dropbox.files import File
from app.services.drive import Drive
from app.micro_apps.snapshot.services.models.dropbox.files import Permission


class DropboxDrive(Drive):
    def __init__(self):
        super().__init__()

    def get_files(self, token, next_page_token=None):
        if next_page_token is None:
            file_request = requests.post(
                "https://api.dropboxapi.com/2/files/list_folder",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "recursive": True,
                    "path": "",
                    "include_has_explicit_shared_members": True,
                    "include_mounted_folders": True,
                },
            )
        else:
            file_request = requests.post(
                "https://api.dropboxapi.com/2/files/list_folder/continue",
                headers={"Authorization": f"Bearer {token}"},
                json={"cursor": next_page_token},
            )
        status_code = getattr(file_request, "status_code")
        if status_code == 200:
            file_obj = file_request.json()
            next_page_token = None
            if file_obj["has_more"]:
                next_page_token = file_obj["cursor"]
            files = file_obj["entries"]
            formatted_files = []
            formatted_shared_folders = []
            for file in files:
                if "size" in file:
                    size = file["size"]
                else:
                    size = 0
                if "server_modified" in file:
                    modified_time = file["server_modified"]
                else:
                    modified_time = None
                if "shared_folder_id" in file:
                    formatted_folder = {
                        "mimeType": file[".tag"],
                        "id": file["id"],
                        "name": file["name"],
                        "driveId": file["shared_folder_id"],
                        "shared": True,
                        "size": size,
                        "path": "",
                        "modifiedTime": modified_time,
                    }
                    formatted_shared_folders.append(formatted_folder)
                else:
                    path = file["path_display"].rsplit("/", 1)[0]
                    if "parent_shared_folder_id" in file:
                        driveId = [file["parent_shared_folder_id"]]
                    else:
                        driveId = None
                    formatted_file = {
                        "mimeType": file[".tag"],
                        "id": file["id"],
                        "name": file["name"],
                        "shared": False,
                        "path": path,
                        "driveId": driveId,
                        "parents": [],
                        "modifiedTime": modified_time,
                    }
                    formatted_files.append(formatted_file)
            files = [File(**file).dict() for file in formatted_files]
            folders = [File(**folder).dict() for folder in formatted_shared_folders]
            return files, folders, next_page_token
        else:
            return None, None, None

    def get_permissions_of_files(self, token, file_ids, next_page_token=None):
        if next_page_token is None:
            permission_request = requests.post(
                "https://api.dropboxapi.com/2/sharing/list_file_members/batch",
                headers={"Authorization": f"Bearer {token}"},
                json={"files": file_ids, "limit": 20},
            )
        else:
            permission_request = requests.post(
                "https://api.dropboxapi.com/2/sharing/list_file_members/continue",
                headers={"Authorization": f"Bearer {token}"},
                json={"cursor": next_page_token},
            )
        status_code = getattr(permission_request, "status_code")

        if status_code == 200:
            file_obj = permission_request.json()
            if "cursor" in file_obj:
                next_page_token = file_obj["cursor"]
            formatted_permissions = []
            for file in file_obj:
                permissions = file["result"]["members"]["users"]
                if permissions is []:
                    continue
                file_id = file["file"]
                for permission in permissions:
                    user = permission["user"]
                    raw_role = permission["access_type"][".tag"]
                    if raw_role == "editor":
                        role = "writer"
                    elif raw_role == "owner":
                        role = raw_role
                    elif raw_role == "viewer":
                        role = "commenter"
                    elif raw_role == "viewer_no_comment":
                        role = "reader"
                    else:
                        raise ValueError("invalid role")
                    formatted_permission = {
                        "file_id": file_id,
                        "type": "user",
                        "id": user["account_id"],
                        "emailAddress": user["email"],
                        "displayName": user["display_name"],
                        "role": role,
                        "inherited": permission["is_inherited"],
                    }

                    formatted_permissions.append(
                        Permission(**formatted_permission).dict()
                    )
            return formatted_permissions, next_page_token
        else:
            return None, None

    def get_permissions_of_folder(self, token, folder_id, next_page_token=None):
        if next_page_token is None:
            permission_request = requests.post(
                "https://api.dropboxapi.com/2/sharing/list_folder_members",
                headers={"Authorization": f"Bearer {token}"},
                json={"shared_folder_id": folder_id, "limit": 20},
            )
        else:
            permission_request = requests.post(
                "https://api.dropboxapi.com/2/sharing/list_folder_members/continue",
                headers={"Authorization": f"Bearer {token}"},
                json={"cursor": next_page_token},
            )
        status_code = getattr(permission_request, "status_code")
        if status_code == 200:
            folder_obj = permission_request.json()
            if "cursor" in folder_obj:
                next_page_token = folder_obj["cursor"]
            formatted_permissions = []
            permissions = folder_obj["users"]
            for permission in permissions:
                user = permission["user"]
                raw_role = permission["access_type"][".tag"]
                if raw_role == "editor":
                    role = "writer"
                elif raw_role == "owner":
                    role = raw_role
                elif raw_role == "viewer":
                    role = "commenter"
                elif raw_role == "viewer_no_comment":
                    role = "reader"
                else:
                    raise ValueError("invalid role")
                formatted_permission = {
                    "file_id": folder_id,
                    "type": "user",
                    "id": user["account_id"],
                    "emailAddress": user["email"],
                    "displayName": user["display_name"],
                    "role": role,
                    "inherited": permission["is_inherited"],
                }
                formatted_permissions.append(Permission(**formatted_permission).dict())
            return formatted_permissions, next_page_token
        else:
            return None, None

    def get_permissions_of_folders(self, token, folder_ids):
        formatted_permissions = []
        for folder_id in folder_ids:
            folder_permissions, next_page_token = self.get_permissions_of_folder(
                token, folder_id
            )
            if folder_permissions:
                # there are more permissions to be retrieved
                while next_page_token is not None:
                    (
                        new_folder_permissions,
                        next_page_token,
                    ) = self.get_permissions_of_folder(token, [], next_page_token)
                    folder_permissions += new_folder_permissions
            elif folder_permissions is None:
                return None
            formatted_permissions.extend(folder_permissions)
        return formatted_permissions