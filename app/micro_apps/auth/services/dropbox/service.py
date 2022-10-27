from app.micro_apps.auth.services.dropbox.dropbox_auth import DropboxAuth
from app.micro_apps.auth.services.dropbox.database import DropboxAuthDatabase
from app.services.auth_service import AuthService


class DropboxAuthService(AuthService):
    def __init__(self):
        super().__init__()

    def get_auth_url(self):
        dropbox_auth = DropboxAuth()
        try:
            url = dropbox_auth.get_authorization_url()
            return url
        except Exception as error:
            self.logger.error(error)
            return None

    def get_token(self, code):
        dropbox_auth = DropboxAuth()
        try:
            token = dropbox_auth.get_token(code)
            return token
        except Exception as error:
            self.logger.error(error)
            return None

    def get_user(self, access_token):
        dropbox_auth = DropboxAuth()
        try:
            user = dropbox_auth.get_user(access_token)
            return user
        except Exception as error:
            self.logger.error(error)
            return None

    def check_user_existence(self, email):
        db = DropboxAuthDatabase()
        try:
            if db.check_user_exists(email):
                return True
            else:
                db.save_user(email)
                return False
        except Exception as error:
            self.logger.error(error)
            return None

    def refresh_access_token(self, refresh_token):
        dropbox_auth = DropboxAuth()
        try:
            new_token = dropbox_auth.refresh_token(refresh_token)
            return new_token
        except Exception as error:
            self.logger.error(error)
            return None

    def revoke_token(self, access_token):
        dropbox_auth = DropboxAuth()
        try:
            revoked = dropbox_auth.revoke_token(access_token)
            return revoked
        except Exception as error:
            self.logger.error(error)
            return False
