"""
Interface for Cloud Drive Authentication
"""
import logging
import os
import jwt
from datetime import datetime, timedelta


class Auth:
    def __init__(self):
        self.SECRET = os.getenv("JWT_SECRET_KEY")
        self.ALGORITHM = "HS256"
        self._logger = logging.getLogger(__name__)

    def encode_jwt(self, data: dict, expires_delta: timedelta | None = None):
        """
        :param data: token
        :param expires_delta: token expiration time
        :return: encoded_jwt
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET, algorithm=self.ALGORITHM)  # type: ignore  # noqa: E501
        return encoded_jwt

    def decode_jwt(self, encoded_jwt):
        try:
            decoded_jwt = jwt.decode(encoded_jwt, self.SECRET, self.ALGORITHM)
            return decoded_jwt
        except Exception as error:
            self._logger.info("Token unavailable", error)
            raise Exception("Token is not available.") from error

    def authenticate_user(self, encoded_token):
        pass

    def get_credentials_from_tokens(self, decoded_token):
        pass

    def refresh_credentials(self, creds):
        pass

    def create_credentials(self):
        pass

    def get_user(self, creds):
        pass

    def get_drive_service(self, creds):
        pass
