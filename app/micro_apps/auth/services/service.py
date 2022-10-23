import logging
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.auth.services.database import DataBase

format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"

logging.basicConfig(format=format)

logger = logging.getLogger()


def get_google_auth_url():
    google_auth = GoogleAuth()
    try:
        url = google_auth.get_authorization_url()
        return url
    except Exception as error:
        logger.error(error)
        return None


def get_google_token(code):
    google_auth = GoogleAuth()
    try:
        token = google_auth.get_token(code)
        return token
    except Exception as error:
        logger.error(error)
        return None


def get_google_user(access_token):
    google_auth = GoogleAuth()
    try:
        user = google_auth.get_user(access_token)
        return user
    except Exception as error:
        logger.error(error)
        return None


def check_user_existence(email):
    db = DataBase()
    try:
        if db.check_user_exists(email):
            return True
        else:
            db.save_user(email)
            return False
    except Exception as error:
        logger.error(error)
        return None


def refresh_google_access_token(refresh_token):
    google_auth = GoogleAuth()
    try:
        new_token = google_auth.refresh_token(refresh_token)
        return new_token
    except Exception as error:
        logger.error(error)
        return None


def revoke_google_token(access_token):
    google_auth = GoogleAuth()
    try:
        revoked = google_auth.revoke_token(access_token)
        return revoked
    except Exception as error:
        logger.error(error)
        return False
