"""
Dropbox Auth
"""
import os
import requests

from app.micro_apps.auth.services.models.user import User
from app.services.auth import Auth


class DropboxAuth(Auth):
    def __init__(self):
        super().__init__()
        self.client_id = str(os.getenv("DROPBOX_CLIENT_ID"))
        self.redirect_uri = str(os.getenv("DROPBOX_REDIRECT_URI"))
        self.client_secret = str(os.getenv("DROPBOX_CLIENT_SECRET"))

    def get_authorization_url(self):
        auth_url = (
            f"https://www.dropbox.com/oauth2/authorize?"
            f"client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&response_type=code"
            f"&token_access_type=offline",
        )
        return auth_url

    def get_token(self, code):
        token_request = requests.post(
            "https://api.dropboxapi.com/oauth2/token",
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
            "https://api.dropboxapi.com/2/auth/token/revoke",
            headers={"Authorization": f"Bearer {token}"},
        )

        status_code = getattr(revoke_request, "status_code")
        if status_code == 200:
            return True
        else:
            return False

    def refresh_token(self, refresh_token):
        refresh_request = requests.post(
            "https://api.dropboxapi.com/oauth2/token",
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )

        status_code = getattr(refresh_request, "status_code")
        if status_code == 200:
            return refresh_request.json()
        else:
            return None

    def get_user(self, token):
        user_request = requests.post(
            "https://api.dropboxapi.com/2/users/get_current_account",
            headers={"Authorization": f"Bearer {token}"},
        )
        status_code = getattr(user_request, "status_code")
        if status_code == 200:
            data = user_request.json()
            # format data to match user model
            formatted_data = {
                "name": data["name"]["display_name"],
                "given_name": data["name"]["given_name"],
                "family_name": data["name"]["surname"],
                "email": data["email"],
            }
            user = User(**formatted_data)
            return user
        else:
            return None
