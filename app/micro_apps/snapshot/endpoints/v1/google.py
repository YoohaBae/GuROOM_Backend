"""
    prefix: /apps/snapshot/v1/google
"""

import logging
import os
import json
from fastapi import APIRouter, Cookie, status
from fastapi.responses import JSONResponse
from typing import Optional
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.snapshot.services.google_drive import GoogleDrive
from app.micro_apps.snapshot.services.database import DataBase as SnapshotDataBase
from app.micro_apps.auth.services.database import DataBase as UserDataBase

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter()
router.secret_key = os.getenv("SECRET_KEY")

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s"
    ":%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


@router.post("/files", tags=["snapshots"])
def take_file_snapshot(snapshot_name: str, credentials: Optional[str] = Cookie(None)):
    if credentials:
        credentials = json.loads(credentials)
        if credentials["refresh_token"] is None:
            logging.info("no refresh token in cookie")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content="Refresh token invalid",
            )
    else:
        logging.info("no cookie")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="no credentials in cookie. Login again",
        )

    try:
        google_auth = GoogleAuth()
        google_drive = GoogleDrive()
        credentials = google_auth.dict_to_credentials(credentials)

        # get current user id
        user = google_auth.get_user(credentials)
        user_db = UserDataBase()
        user_obj = user_db.get_user(user["email"])

        # get files from google drive
        files = google_drive.get_files(credentials)

        # take snapshot
        snapshot_db = SnapshotDataBase()
        snapshot_db.create_file_snapshot(snapshot_name, files, user_obj["_id"])

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content="snapshot successfully created"
        )
    except Exception as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="snapshot creation failed",
        )


@router.get("/files", tags=["snapshots"])
def get_file_snapshots(
    name_only: bool,
    snapshot_name: Optional[str] = None,
    credentials: Optional[str] = Cookie(None),
):
    if credentials:
        credentials = json.loads(credentials)
        if credentials["refresh_token"] is None:
            logging.info("no refresh token in cookie")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content="Refresh token invalid",
            )
    else:
        logging.info("no cookie")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="no credentials in cookie. Login again",
        )
    google_auth = GoogleAuth()
    credentials = google_auth.dict_to_credentials(credentials)

    # get current user id
    user = google_auth.get_user(credentials)
    user_db = UserDataBase()
    user_obj = user_db.get_user(user["email"])
    snapshot_db = SnapshotDataBase()
    data = snapshot_db.get_file_snapshots(user_obj["_id"], snapshot_name, name_only)
    return data
