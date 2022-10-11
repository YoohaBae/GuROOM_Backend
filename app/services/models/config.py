from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = False
    # Enable csrf double submit protection. default is True
    authjwt_cookie_csrf_protect: bool = False
