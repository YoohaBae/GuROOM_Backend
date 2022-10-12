"""
    prefix: /apps/snapshot/v1/google
"""

import logging
import os
from typing import Optional
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from app.services.models.config import Settings
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.auth.services.database import DataBase as UserDataBase
from app.micro_apps.snapshot.services.google_drive import GoogleDrive
from app.micro_apps.snapshot.services.database import DataBase as SnapshotDataBase

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter()
router.secret_key = os.getenv("SECRET_KEY")

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s"
    ":%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/files", tags=["snapshots"])
def take_file_snapshot(snapshot_name: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    google_auth = GoogleAuth()
    google_drive = GoogleDrive()

    user = google_auth.get_user(access_token)

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="user not found"
        )

    user_db = UserDataBase()

    user_obj = user_db.get_user(user["email"])

    # get files from google drive
    files = google_drive.get_files(access_token)

    # take snapshot
    snapshot_db = SnapshotDataBase()
    snapshot_db.create_file_snapshot(snapshot_name, files, user_obj["_id"])

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="snapshot successfully created"
    )


@router.get("/files", tags=["snapshots"])
def get_file_snapshots(
    name_only: bool, snapshot_name: Optional[str] = None, authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    google_auth = GoogleAuth()

    user = google_auth.get_user(access_token)

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="user not found"
        )

    user_db = UserDataBase()

    user_obj = user_db.get_user(user["email"])

    snapshot_db = SnapshotDataBase()
    data = snapshot_db.get_file_snapshots(user_obj["_id"], snapshot_name, name_only)
    return data
