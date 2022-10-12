"""
Interface for Cloud Drive Authentication
"""
import logging


class Drive:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_files(self, creds):
        pass

    def change_permissions(self, file, permission):
        pass

    def change_permission(self, file, permission):
        pass
