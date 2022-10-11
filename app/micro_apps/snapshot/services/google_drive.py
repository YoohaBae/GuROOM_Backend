"""
Google Drive Auth
"""
import logging
from googleapiclient.discovery import build
from .models.files import File
from .drive import Drive
from pydantic import parse_obj_as
from typing import List

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s:"
    "%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


class GoogleDrive(Drive):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def get_drive_service(self, creds):
        service = build("drive", "v3", credentials=creds)
        return service

    def get_groups(self, creds):
        pass

    def get_files(self, creds):
        service = self.get_drive_service(creds)
        file_obj = (
            service.files()
            .list(fields="*", corpora="allDrives", supportsAllDrives=True, includeItemsFromAllDrives=True,
                  q="trashed=false")
            .execute()
        )
        try:
            files = parse_obj_as(List[File], file_obj["files"])
            return files
        except Exception as error:
            self._logger.error("marshalling", error)
        return []
