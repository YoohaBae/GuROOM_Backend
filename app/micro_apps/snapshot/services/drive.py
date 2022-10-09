"""
Interface for Cloud Drive Authentication
"""
import logging
import os


class Drive:
    def __init__(self):
        self.SECRET = os.getenv("JWT_SECRET_KEY")
        self.ALGORITHM = "HS256"
        self._logger = logging.getLogger(__name__)

    def get_files(self, creds):
        pass

    def save_file_snapshot(self, creds):
        pass

    def save_group_snapshot(self, creds):
        pass
