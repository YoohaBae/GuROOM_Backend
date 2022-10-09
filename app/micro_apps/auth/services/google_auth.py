"""
Google Drive Auth
"""
import os
import logging
import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
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
            "openid",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

    def get_credentials(self, state, authorization_response, redirect_uri):
        flow = Flow.from_client_secrets_file(
            "./app/micro_apps/auth/services/credentials.json",
            scopes=self.SCOPES,
            state=state,
        )
        print(authorization_response)
        flow.redirect_uri = redirect_uri
        flow.fetch_token(authorization_response=authorization_response)
        return flow.credentials

    def credentials_to_dict(self, creds):
        return {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }

    def dict_to_credentials(self, creds):
        return google.oauth2.credentials.Credentials(**creds)

    def get_authorization_url(self):
        flow = Flow.from_client_secrets_file(
            "./app/micro_apps/auth/services/credentials.json", scopes=self.SCOPES
        )
        flow.redirect_uri = os.getenv("REDIRECT_URI")
        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )
        return authorization_url, state

    def get_user_service(self, creds):
        service = build("oauth2", "v2", credentials=creds)
        return service

    def get_user(self, creds):
        service = self.get_user_service(creds)
        user_info = service.userinfo().get().execute()
        return user_info

    def check_for_sufficient_permissions(self, scope):
        for s in self.SCOPES:
            if s not in scope:
                return False
        return True

    def add_user_to_database(self, user_info):
        pass
