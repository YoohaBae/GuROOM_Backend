"""
Google Drive Auth
"""
import os
import logging
import requests
from urllib.parse import quote_plus

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

    def get_authorization_url(self):
        client_id = str(os.getenv("CLIENT_ID"))
        redirect_uri = str(os.getenv("REDIRECT_URI"))
        scope = " ".join(self.SCOPES)
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={quote_plus(client_id)}"
            f"&response_type=code&scope={quote_plus(scope)}"
            f"&redirect_uri={quote_plus(redirect_uri)}"
            f"&include_granted_scopes=true&access_type=offline&prompt=consent"
        )
        return auth_url

    def get_token(self, code):
        token_request = requests.post(
            "https://oauth2.googleapis.com/token",
            params={
                "code": code,
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
                "redirect_uri": os.getenv("REDIRECT_URI"),
                "grant_type": "authorization_code",
            },
        )

        status_code = getattr(token_request, "status_code")
        if status_code == 200:
            return token_request.json()
        else:
            return False

    def revoke_token(self, token):
        revoke_request = requests.post(
            "https://oauth2.googleapis.com/revoke",
            params={"token": token},
        )

        status_code = getattr(revoke_request, "status_code")
        if status_code == 200:
            return True
        else:
            return False

    def get_user(self, token):
        user_request = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={"access_token": token, "alt": "json"},
        )
        status_code = getattr(user_request, "status_code")
        if status_code == 200:
            return user_request.json()
        else:
            return False
