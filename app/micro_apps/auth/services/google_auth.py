"""
Google Drive Auth
"""
import logging
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .auth import Auth

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s:"
    "%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


class GoogleAuth(Auth):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self.SCOPES = [
            "https://www.googleapis.com/auth/drive",
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

    def authenticate_user(self, encoded_token):
        """
        :param encoded_token: encoded access token + user (email, name)
        :return: user model and auth model
        """
        user = None
        if encoded_token:
            try:
                decoded_token = self.decode_jwt(encoded_token)
                creds = self.get_credentials_from_tokens(decoded_token)
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        # access token doesn't exist or
                        # expired but refresh token exists
                        self.refresh_credentials(creds)
                        user = self.get_user(creds)
                else:
                    user = self.get_user(creds)
            except Exception:
                self._logger.error("No such user")
        return user, json.loads(creds.to_json())

    def authorize_user(self):
        creds = self.create_credentials()
        user = self.get_user(creds)
        try:
            auth = json.loads(creds.to_json())
        except Warning as error:
            self._logger.error(error)
            raise Warning("Insufficient Permissions")
        return user, auth

    def get_credentials_from_tokens(self, decoded_token):
        token = decoded_token["token"]
        refresh_token = decoded_token["refresh_token"]
        token_uri = decoded_token["token_uri"]
        client_id = decoded_token["client_id"]
        client_secret = decoded_token["client_secret"]
        scopes = decoded_token["scopes"]
        creds = Credentials(
            token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
        )
        return creds

    def refresh_credentials(self, creds):
        creds.refresh(Request())

    def create_credentials(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            "./app/micro_apps/auth/services/credentials.json", self.SCOPES
        )
        creds = flow.run_local_server(port=0)
        return creds

    def get_user(self, creds):
        user_info_service = build("oauth2", "v2", credentials=creds)
        user_info = user_info_service.userinfo().get().execute()
        return user_info

    def get_drive_service(self, creds):
        service = build("drive", "v3", credentials=creds)
        return service
