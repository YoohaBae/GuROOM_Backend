"""
Google Drive Auth
"""
import os
import requests
from urllib.parse import quote_plus

from app.micro_apps.auth.services.models.user import User
from app.services.auth import Auth


class GoogleAuth(Auth):
    def __init__(self):
        super().__init__()
        self.SCOPES = [
            "openid",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]
        self.client_id = str(os.getenv("GOOGLE_CLIENT_ID"))
        self.redirect_uri = str(os.getenv("REDIRECT_URI"))
        self.client_secret = str(os.getenv("GOOGLE_CLIENT_SECRET"))

    def get_authorization_url(self):
        scope = " ".join(self.SCOPES)
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={quote_plus(self.client_id)}"
            f"&response_type=code&scope={quote_plus(scope)}"
            f"&redirect_uri={quote_plus(self.redirect_uri)}"
            f"&include_granted_scopes=true&access_type=offline&prompt=consent"
        )
        return auth_url

    def get_token(self, code):
        token_request = requests.post(
            "https://oauth2.googleapis.com/token",
            params={
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code",
            },
        )

        status_code = getattr(token_request, "status_code")
        if status_code == 200:
            return token_request.json()
        else:
            return None

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

    def refresh_token(self, refresh_token):
        refresh_request = requests.post(
            "https://oauth2.googleapis.com/token",
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        )

        status_code = getattr(refresh_request, "status_code")
        if status_code == 200:
            return refresh_request.json()
        else:
            return None

    def get_user(self, token):
        user_request = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={"access_token": token, "alt": "json"},
        )
        status_code = getattr(user_request, "status_code")
        if status_code == 200:
            data = user_request.json()
            user = User(**data)
            return user
        else:
            return None
