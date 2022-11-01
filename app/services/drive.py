"""
Interface for Cloud Drive Authentication
"""
import logging


class Drive:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_files(self, creds):
        raise NotImplementedError("Must be implemented by child class")
