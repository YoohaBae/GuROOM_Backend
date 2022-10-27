"""
Interface for Cloud Drive Authentication
"""
import logging
import os


class Auth:
    def __init__(self):
        format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=format)
        self.logger = logging.getLogger()
        self.SECRET = os.getenv("JWT_SECRET_KEY")
        self.ALGORITHM = "HS256"
        self._logger = logging.getLogger(__name__)

    def get_user(self, creds):
        pass

    def add_user_to_database(self, user_info):
        pass
