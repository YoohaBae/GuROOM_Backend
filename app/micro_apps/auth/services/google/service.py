from app.micro_apps.auth.services.google.google_auth import GoogleAuth
from app.micro_apps.auth.services.google.database import GoogleAuthDatabase
from app.services.auth_service import AuthService


class GoogleAuthService(AuthService):
    def __init__(self):
        super().__init__(GoogleAuth(), GoogleAuthDatabase())
