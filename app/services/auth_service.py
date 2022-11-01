import logging


class AuthService:
    def __init__(self, auth, db):
        format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=format)
        self.logger = logging.getLogger()
        self.auth = auth
        self._db = db

    def get_auth_url(self):
        try:
            url = self.auth.get_authorization_url()
            return url
        except Exception as error:
            self.logger.error(error)
            return None

    def get_token(self, code):
        try:
            token = self.auth.get_token(code)
            return token
        except Exception as error:
            self.logger.error(error)
            return None

    def get_user(self, access_token):
        try:
            user = self.auth.get_user(access_token)
            return user
        except Exception as error:
            self.logger.error(error)
            return None

    def check_user_existence(self, email):
        try:
            if self._db.check_user_exists(email):
                return True
            else:
                self._db.save_user(email)
                return False
        except Exception as error:
            self.logger.error(error)
            return None

    def refresh_access_token(self, refresh_token):
        try:
            new_token = self.auth.refresh_token(refresh_token)
            return new_token
        except Exception as error:
            self.logger.error(error)
            return None

    def revoke_token(self, access_token):
        try:
            revoked = self.auth.revoke_token(access_token)
            return revoked
        except Exception as error:
            self.logger.error(error)
            return False
