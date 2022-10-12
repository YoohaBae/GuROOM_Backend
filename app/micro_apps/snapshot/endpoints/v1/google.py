"""
    prefix: /apps/snapshot/v1/google
"""

import logging
import os
import json
from fastapi import APIRouter, status, Depends, Body
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from app.utils.util import DateTimeEncoder
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
    user_id = str(user_obj["_id"])

    # get root drive id
    root_id = google_drive.get_root_file_id(access_token)
    if not root_id:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve files",
        )

    # get files from google drive
    files, next_page_token = google_drive.get_files(access_token)

    if files:
        # take snapshot
        while next_page_token is not None:
            new_files, next_page_token = google_drive.get_next_files(
                access_token, next_page_token
            )
            files += new_files

        # TODO: calculate inherit direct permissions and file path

        snapshot_db = SnapshotDataBase(user_id)
        snapshot_db.create_file_snapshot(snapshot_name, root_id, files)

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
    user_id = str(user_obj["_id"])

    snapshot_name = body.snapshot_name
    snapshot_db = SnapshotDataBase(user_id)

    try:
        snapshot_db.delete_file_snapshot(snapshot_name)
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
    user_id = str(user_obj["_id"])

    snapshot_name = body.snapshot_name
    new_snapshot_name = body.new_snapshot_name
    snapshot_db = SnapshotDataBase(user_id)

    try:
        snapshot_db.edit_file_snapshot_name(snapshot_name, new_snapshot_name)
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
def get_file_snapshot_names(authorize: AuthJWT = Depends()):
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
    user_id = str(user_obj["_id"])

    snapshot_db = SnapshotDataBase(user_id)
    try:
        names = snapshot_db.get_file_snapshot_names()
        data = {"names": names}
        data = json.loads(json.dumps(data, cls=DateTimeEncoder))
        return JSONResponse(status_code=status.HTTP_200_OK, content=data)
    except Exception as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file snapshot names",
        )


@router.get("/files", tags=["snapshots"])
def get_file_snapshots(
    snapshot_name: str,
    offset: int,
    limit: int,
    folder_id: str = None,
    my_drive: bool = False,
    authorize: AuthJWT = Depends(),
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
    user_id = str(user_obj["_id"])

    snapshot_db = SnapshotDataBase(user_id)

    if my_drive:
        folder_id = snapshot_db.get_root_id(snapshot_name)

    try:
        files = snapshot_db.get_file_under_folder(
            snapshot_name, offset, limit, folder_id
        )
        data = json.loads(json.dumps(files, cls=DateTimeEncoder))
        return JSONResponse(status_code=status.HTTP_200_OK, content=data)
    except Exception as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file under folder",
        )


@router.get("/")
def test(snapshot_name: str, authorize: AuthJWT = Depends()):
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
    user_id = str(user_obj["_id"])
    snapshot_db = SnapshotDataBase(user_id)
    file = snapshot_db.get_file(snapshot_name, "16nC4KxfzL5AY7BSakb_i_3d3Mp-ZbU9D")
    return file
