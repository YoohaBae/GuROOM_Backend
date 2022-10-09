"""
Google Drive Auth
"""
import logging
from googleapiclient.discovery import build

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

    def get_drive_service(self, creds):
        service = build("snapshot", "v3", credentials=creds)
        return service

    def save_file_snapshot(self, creds):
        pass

    def save_group_snapshot(self, creds):
        pass

    def get_files(self, creds):
        pass
