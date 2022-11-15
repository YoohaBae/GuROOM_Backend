"""
Dropbox Drive
"""
import requests
from app.micro_apps.snapshot.services.models.dropbox.files import File
from app.services.drive import Drive


class DropboxDrive(Drive):
    def __init__(self):
        super().__init__()

    # def get_root_file_id(self, token):
    #     root_file_request = requests.get(
    #         "https://www.googleapis.com/drive/v3/files/root",
    #         params={"access_token": token},
    #     )
    #
    #     status_code = getattr(root_file_request, "status_code")
    #     if status_code == 200:
    #         id = root_file_request.json()["id"]
    #         return id
    #     else:
    #         return None

    def get_files(self, token, next_page_token=None):
        if next_page_token is None:
            file_request = requests.post(
                "https://api.dropboxapi.com/2/files/list_folder",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "recursive": True,
                    "path": "",
                    "include_has_explicit_shared_members": True,
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
                if "sharing_info" in file:
                    formatted_folder = {
                        "mimeType": file[".tag"],
                        "id": file["id"],
                        "name": file["name"],
                        "driveId": file["shared_folder_id"],
                        "shared": True,
                        "size": size,
                        "path": file["path_display"]
                    }
                    formatted_shared_folders.append(formatted_folder)
                else:
                    formatted_file = {
                        "mimeType": file[".tag"],
                        "id": file["id"],
                        "name": file["name"],
                        "shared": False,
                        "path": file["path_display"]
                    }
                    formatted_files.append(formatted_file)
            files = [File(**file) for file in formatted_files]
            folders = [File(**folder) for folder in formatted_shared_folders]
            return files, folders, next_page_token
        else:
            return None, None, None

    def get_files_under_shared_folders(self, token, shared_folder_id, next_page_token=None):
        if next_page_token is None:
            file_request = requests.post(
                "https://api.dropboxapi.com/2/files/list_folder",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "recursive": True,
                    "path": f"ns:{shared_folder_id}",
                    "include_has_explicit_shared_members": True,
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
            for file in files:
                if "size" in file:
                    size = file["size"]
                else:
                    size = 0
                formatted_file = {
                    "mimeType": file[".tag"],
                    "id": file["id"],
                    "name": file["name"],
                    "driveId": file["shared_folder_id"],
                    "shared": True,
                    "size": size,
                    "path": file["path_display"]
                }
                formatted_files.append(formatted_file)
            files = [File(**file) for file in formatted_files]
            return files, next_page_token
        else:
            return None, None

    def get_permissions_of_files(self, token, file_ids):
        permission_request = requests.get(
            "https://api.dropboxapi.com/2/file_requests/list",
            headers={"Authorization": f"Bearer {token}"},
            params={"actions": ["enable_viewer_info"], "files": file_ids},
        )
        status_code = getattr(permission_request, "status_code")
        if status_code == 200:
            file_obj = permission_request.json()
            files = file_obj["files"]
            return files
        else:
            return None
