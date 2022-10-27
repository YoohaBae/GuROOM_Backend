from app.micro_apps.auth.services.google.google_auth import GoogleAuth
from app.micro_apps.auth.services.google.database import GoogleAuthDatabase
from app.services.auth_service import AuthService


class GoogleAuthService(AuthService):
    def __init__(self):
        super().__init__()

    def get_auth_url(self):
        google_auth = GoogleAuth()
        try:
            url = google_auth.get_authorization_url()
            return url
        except Exception as error:
            self.logger.error(error)
            return None

    def get_token(self, code):
        google_auth = GoogleAuth()
        try:
            token = google_auth.get_token(code)
            return token
        except Exception as error:
            self.logger.error(error)
            return None

    def get_user(self, access_token):
        google_auth = GoogleAuth()
        try:
            user = google_auth.get_user(access_token)
            return user
        except Exception as error:
            self.logger.error(error)
            return None

    def check_user_existence(self, email):
        db = GoogleAuthDatabase()
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
        google_auth = GoogleAuth()
        try:
            new_token = google_auth.refresh_token(refresh_token)
            return new_token
        except Exception as error:
            self.logger.error(error)
            return None

    def revoke_token(self, access_token):
        google_auth = GoogleAuth()
        try:
            revoked = google_auth.revoke_token(access_token)
            return revoked
        except Exception as error:
            self.logger.error(error)
            return False
