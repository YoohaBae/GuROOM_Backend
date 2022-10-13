"""
    prefix: /apps/snapshot/v1/google
"""

import logging
import os
from fastapi import APIRouter, status, Depends, Body
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from app.micro_apps.snapshot.services import service
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

    user_id = service.get_user_id_from_token(access_token)

    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # get root drive id
    root_id = service.get_root_id(access_token)
    if not root_id:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve root id",
        )

    files = service.get_all_files(access_token)
    if len(files) != 0 and not files:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve files",
        )

    created = service.save_all_files(user_id, snapshot_name, files, root_id)
    if not created:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="snapshot creation failed",
        )

    analysis_performed = service.perform_inherit_direct_permission_analysis(
        user_id, snapshot_name
    )
    if not analysis_performed:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="analysis failure",
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="snapshot successfully created"
    )


@router.delete("/files", tags=["snapshots"])
def delete_file_snapshot(
        body: DeleteFileSnapshotBody = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()
    snapshot_name = body.snapshot_name

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    deleted = service.delete_file_snapshot(user_id, snapshot_name)
    if not deleted:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to delete snapshot",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content="snapshot deleted")


@router.put("/files", tags=["snapshots"])
def edit_file_snapshot_name(
        body: PutFileSnapshotBody = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()
    snapshot_name = body.snapshot_name
    new_snapshot_name = body.new_snapshot_name

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    edited = service.edit_file_snapshot_name(user_id, snapshot_name, new_snapshot_name)
    if not edited:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to update snapshot name",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content="snapshot name updated")


@router.get("/files/names", tags=["snapshots"])
def get_file_snapshot_names(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    names = service.get_file_snapshot_names(user_id)
    if len(names) != 0 and not names:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file snapshot names",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=names)


@router.get("/files", tags=["snapshots"])
def get_file_snapshots(
        snapshot_name: str,
        offset: int,
        limit: int,
        folder_id: str = None,
        shared_drive: bool = False,
        my_drive: bool = False,
        authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    if my_drive:
        files = service.get_files_of_my_drive(user_id, snapshot_name, offset, limit)
    elif shared_drive:
        files = service.get_files_of_shared_drive(user_id, snapshot_name, offset, limit)
    else:
        files = service.get_files_of_folder(
            user_id, snapshot_name, offset, limit, folder_id
        )

    if len(files) != 0 and not files:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file under folder",
        )

    permissions = service.get_permission_of_files(user_id, snapshot_name, files)

    if len(permissions) != 0 and not permissions:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of permissions under folder",
        )

    data = {
        "files": files,
        "permissions": permissions
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)
