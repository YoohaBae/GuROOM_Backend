"""
    prefix: /apps/snapshot/v1/google
"""

import logging
import os
from datetime import datetime
from fastapi import APIRouter, status, Depends, Body, UploadFile, Form, File
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


@router.post("/files", tags=["file_snapshot"], status_code=status.HTTP_201_CREATED)
def take_file_snapshot(
        body: PostFileSnapshotBody = Body(...), authorize: AuthJWT = Depends()
):
    """
    operation takes file snapshot
    :param body: file snapshot name
    :param authorize: user authentication
    :return: None
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()
    snapshot_name = body.snapshot_name

    user_id = service.get_user_id_from_token(access_token)

    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # get root drive id
    root_id = service.get_root_id_from_api(access_token)
    if not root_id:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve root id",
        )

    shared_drives = service.get_all_shared_drives_from_api(access_token)
    if shared_drives is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve shared drives",
        )

    files = service.get_all_files_from_api(access_token)
    if files is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve files",
        )

    created = service.create_file_snapshot(
        user_id, snapshot_name, files, root_id, shared_drives
    )
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


@router.delete("/files", tags=["file_snapshot"])
def delete_file_snapshot(
        body: DeleteFileSnapshotBody = Body(...), authorize: AuthJWT = Depends()
):
    """
    operation: deletes file snapshot
    :param body: file snapshot name
    :param authorize: user authentication
    :return: None
    """
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


@router.put("/files", tags=["file_snapshot"])
def edit_file_snapshot_name(
    body: PutFileSnapshotBody = Body(...), authorize: AuthJWT = Depends()
):
    """
    operation: edits file snapshots
    :param body: file snapshot name to edit, what file snapshot name to edit to
    :param authorize: user authentication
    :return: None
    """
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


@router.get("/files/names", tags=["file_snapshot"])
def get_file_snapshot_names(authorize: AuthJWT = Depends()):
    """
    operation: gets list of file snapshots
    :param authorize: user authentication
    :return: list of file snapshot names
    """
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


@router.get("/files/drives", tags=["file_snapshot"])
def get_shared_drives(snapshot_name: str, authorize: AuthJWT = Depends()):
    """
    operation: gets name and id of shared drive
    :param snapshot_name: name of file snapshot
    :param authorize: user authentication
    :return: name and id of shared drive
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    shared_drives = service.get_shared_drives(user_id, snapshot_name)
    if shared_drives is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file snapshot names",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=shared_drives)


@router.get("/files", tags=["file_snapshot"])
def get_file_snapshots(
    snapshot_name: str,
    offset: int = None,
    limit: int = None,
    my_drive: bool = False,
    shared_with_me: bool = False,
    shared_drive: bool = True,
    folder_id: str = None,
    authorize: AuthJWT = Depends(),
):
    """
    operation: get all files under certain folder or drive
    :param snapshot_name:
    :param offset: what index to start
    :param limit: how many to retrieve
    :param my_drive: retrieve all files under my_drive
    :param shared_with_me: retrieve all files shared with me
    :param shared_drive: retrieve all files of a certain shared drive
    :param folder_id: the id of shared drive or folder to retrieve files from
    :param authorize: user authentication
    :return:
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    if my_drive:
        files = service.get_files_of_my_drive(user_id, snapshot_name, offset, limit)
    elif shared_with_me:
        files = service.get_files_of_shared_with_me(
            user_id, snapshot_name, offset, limit
        )
    elif shared_drive:
        files = service.get_files_of_shared_drive(
            user_id, snapshot_name, folder_id, offset, limit
        )
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


@router.get("/files/search", tags=["file_snapshot"])
def search_files(
    snapshot_name: str,
    query: str,
    authorize: AuthJWT = Depends(),
):
    """
    operation: perform search on a file snapshot
    :param snapshot_name: file snapshot name
    :param query: the search query
    :param authorize: user authentication
    :return: list of files
    """
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


@router.get("/files/differences/sharing", tags=["file_snapshot"])
def get_file_folder_sharing_difference(
    snapshot_name: str, file_id: str, authorize: AuthJWT = Depends()
):
    """
    operation: get the permission difference between a file and folder
    :param snapshot_name: file snapshot name
    :param file_id: the file id to perform the analysis
    :param authorize: user authentication
    :return:
        additional_folder_permissions: permissions that folder has but file doesn't
        changed_permissions: permissions that have been changed between folder and file
        additional_file_permissions: permissions that file has but folder doesn't
    """
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


@router.get("/files/differences", tags=["file_snapshot"])
def get_snapshot_difference(
    base_snapshot_name: str, compare_snapshot_name: str, authorize: AuthJWT = Depends()
):
    """
    operation: get files that are different between two file snapshots
    :param base_snapshot_name: name of base file snapshot
    :param compare_snapshot_name: name of comparing file snapshot
    :param authorize: user authentication
    :return:
        changed_files: files that permission have changed
        added_files: files that do not exist in base file snapshot
    """
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
            content="unable to perform file snapshot analysis",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=difference)


@router.post("/groups", tags=["group_snapshot"])
async def create_group_membership_snapshot(
        file: UploadFile = File(),
        group_name: str = Form(...),
        group_email: str = Form(...),
        create_time: datetime = Form(...),
        authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    memberships = await service.scratch_group_memberships_from_file(file)
    if memberships is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve memberships from html file",
        )

    created = service.create_group_snapshot(
        user_id, group_name, group_email, create_time, memberships
    )
    if not created:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to create group membership snapshot",
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="group membership snapshot created"
    )


@router.get("/groups", tags=["group_snapshot"])
def get_group_membership_snapshots(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    user_id = service.get_user_id_from_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    groups = service.get_recent_group_membership_snapshots(user_id)
    if groups is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to create group membership snapshot",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=groups)
