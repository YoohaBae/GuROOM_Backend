"""
Google Drive Auth
"""
import logging
import requests
from pydantic import parse_obj_as
from typing import List
from .models.files import File
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

    def get_files(self, token):
        file_request = requests.get(
            "https://www.googleapis.com/drive/v3/files",
            params={
                "access_token": token,
                "fields": "*",
                "corpora": "allDrives",
                "supportAllDrives": True,
                "includeItemsFromAllDrives": True,
                "q": "trashed=False",
            },
        )
        status_code = getattr(file_request, "status_code")
        if status_code == 200:
            file_obj = file_request.json()
            files = parse_obj_as(List[File], file_obj["files"])
            return files
        else:
            return []
