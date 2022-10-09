"""
    prefix: /apps/snapshot/v1/google
"""

import logging
import os
from fastapi import APIRouter, Request
from app.micro_apps.auth.endpoints.v1.google import router as auth_router
from fastapi.responses import RedirectResponse
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.snapshot.services.google_drive import GoogleDrive

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "0"

router = APIRouter()
router.secret_key = os.getenv("SECRET_KEY")

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s"
    ":%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


@router.get("/files", tags=["snapshots"])
def get_files(request: Request):
    if "credentials" not in request.session:
        return RedirectResponse(
            "/apps/auth/v1/google" + auth_router.url_path_for("create_google_auth")
        )

    google_auth = GoogleAuth()
    google_drive = GoogleDrive()
    credentials = google_auth.dict_to_credentials(request.session["credentials"])
    files = google_drive.get_files(credentials)
    request.session["credentials"] = google_auth.credentials_to_dict(credentials)
    return files
