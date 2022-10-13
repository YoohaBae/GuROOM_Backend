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
    if files is None:
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
    if names is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file snapshot names",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=names)


@router.get("/files", tags=["snapshots"])
def get_file_snapshots(
    snapshot_name: str,
    offset: int = None,
    limit: int = None,
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
            user_id, snapshot_name, folder_id, offset, limit
        )

    if files is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file under folder",
        )

    permissions = service.get_permission_of_files(user_id, snapshot_name, files)

    if permissions is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of permissions under folder",
        )

    data = {"files": files, "permissions": permissions}

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@router.get("/files/search", tags=["snapshot"])
def search_files(
    snapshot_name: str,
    query: str,
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    queries = query.split(" ")

    result_files = []

    if "is:file_folder_diff" in queries:
        different_files = service.get_files_with_diff_permission_from_folder(
            user_id,
            snapshot_name,
        )
        if different_files is None:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="failed to perform file_folder_diff search",
            )
        result_files = different_files

    permissions = service.get_permission_of_files(user_id, snapshot_name, result_files)

    if permissions is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of permissions under folder",
        )
    data = {"files": result_files, "permissions": permissions}

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@router.get("/files/differences/sharing", tags=["snapshot"])
def get_file_folder_sharing_difference(
    snapshot_name: str,
    file_id: str,
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    difference = service.get_file_folder_sharing_difference(
        user_id, snapshot_name, file_id
    )
    if difference is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve ",
        )
    base_more_permissions, changes, compare_more_permissions = difference
    data = {
        "additional_folder_permissions": base_more_permissions,
        "changed_permissions": changes,
        "additional_file_permissions": compare_more_permissions,
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@router.get("/files/differences", tags=["snapshot"])
def get_snapshot_difference(
    base_snapshot_name: str, compare_snapshot_name: str, authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    difference = service.get_difference_of_two_snapshots(
        user_id, base_snapshot_name, compare_snapshot_name
    )
    if difference is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve ",
        )

    changes, compare_more_files = difference
    data = {"changed_files": changes, "compare_additional_files": compare_more_files}

    return JSONResponse(status_code=status.HTTP_200_OK, content=data)
