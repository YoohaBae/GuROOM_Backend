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
        self.client_id = None
        self.redirect_uri = None
        self.client_secret = None

    def get_authorization_url(self):
        """
        Retrieve the authorization url of drive oauth
        :return: url
        """
        raise NotImplementedError("Must be implemented by child class")

    def get_token(self, code):
        """
        Retrieves the access token and refresh token
        :param code: code retrieved by user authentication
        :return: access token and refresh token as a dict
        """
        raise NotImplementedError("Must be implemented by child class")

    def revoke_token(self, token):
        """
        Revoke the refresh token of cloud drive oauth2
        :param token: access token
        :return: Boolean for success or failure
        """
        raise NotImplementedError("Must be implemented by child class")

    def refresh_token(self, refresh_token):
        """
        Refreshes access token with refresh token
        :param refresh_token: refresh token
        :return: access token
        """
        raise NotImplementedError("Must be implemented by child class")

    def get_user(self, token):
        """
        Get user information of cloud drive oauth2
        :param token: access token
        :return: user information -> may need to format in User model
        """
        raise NotImplementedError("Must be implemented by child class")
