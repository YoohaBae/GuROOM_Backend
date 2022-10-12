"""
    prefix: /apps/snapshot/v1/google
"""

import logging
import os
from fastapi import APIRouter, status, Depends, Body
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.auth.services.database import DataBase as UserDataBase
from app.micro_apps.snapshot.services.google_drive import GoogleDrive
from app.micro_apps.snapshot.services.database import DataBase as SnapshotDataBase
from ..models.snapshot import (
    DeleteFileSnapshotBody,
    PutFileSnapshotBody,
    PostFileSnapshotBody,
)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter()
router.secret_key = os.getenv("SECRET_KEY")

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s"
    ":%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


@router.post("/files", tags=["snapshots"], status_code=status.HTTP_201_CREATED)
def take_file_snapshot(
    body: PostFileSnapshotBody = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()
    snapshot_name = body.snapshot_name

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
    files, incomplete, next_page_token = google_drive.get_files(access_token)

    if files:
        # take snapshot
        while incomplete:
            new_files, incomplete, next_page_token = google_drive.get_next_files(
                access_token, next_page_token
            )
            files += new_files

        snapshot_db = SnapshotDataBase()
        snapshot_db.create_file_snapshot(snapshot_name, files, user_obj["_id"])

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content="snapshot successfully created"
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve files",
        )


@router.delete("/files", tags=["snapshots"])
def delete_file_snapshot(
    body: DeleteFileSnapshotBody = Body(...), authorize: AuthJWT = Depends()
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

    snapshot_name = body.snapshot_name
    snapshot_db = SnapshotDataBase()

    try:
        snapshot_db.delete_file_snapshot(user_obj["_id"], snapshot_name)
        return JSONResponse(status_code=status.HTTP_200_OK, content="snapshot deleted")
    except Exception as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to delete snapshot",
        )


@router.put("/files", tags=["snapshots"])
def edit_file_snapshot_name(
    body: PutFileSnapshotBody = Body(...), authorize: AuthJWT = Depends()
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

    snapshot_name = body.snapshot_name
    new_snapshot_name = body.new_snapshot_name
    snapshot_db = SnapshotDataBase()

    try:
        snapshot_db.edit_file_snapshot_name(
            user_obj["_id"], snapshot_name, new_snapshot_name
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content="snapshot name updated"
        )
    except Exception as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to update snapshot name",
        )


@router.get("/files/names", tags=["snapshots"])
def get_file_snapshots(authorize: AuthJWT = Depends()):
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
    try:
        names = snapshot_db.get_file_snapshot_names(user_obj["_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=names)
    except Exception as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file snapshot names",
        )
