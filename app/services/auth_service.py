import logging


class AuthService:
    def __init__(self):
        format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=format)
        self.logger = logging.getLogger()

    def get_auth_url(self):
        pass

    def get_token(self, code):
        pass

    def get_user(self, access_token):
        pass

    def check_user_existence(self, email):
        pass

    def refresh_access_token(self, refresh_token):
        pass

    def revoke_token(self, access_token):
        pass
