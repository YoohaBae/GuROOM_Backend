from app.micro_apps.auth.services.dropbox.dropbox_auth import DropboxAuth
from app.micro_apps.auth.services.dropbox.database import DropboxAuthDatabase
from app.services.auth_service import AuthService


class DropboxAuthService(AuthService):
    def __init__(self):
        super().__init__(DropboxAuth(), DropboxAuthDatabase())
