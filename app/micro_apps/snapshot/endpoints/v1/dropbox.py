"""
    prefix: /apps/snapshot/v1/dropbox
"""

import logging
import os
from fastapi import APIRouter, status, Depends, Body
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from ...services.dropbox.service import DropboxSnapshotService
from ..models.snapshot import (
    DeleteFileSnapshotBody,
    PutFileSnapshotBody,
    PostFileSnapshotBody,
)
from ..models.access_control import (
    DropboxAccessControlBody,
    DeleteAccessControlRequirementBody,
)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter()
router.secret_key = os.getenv("SECRET_KEY")

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s"
    ":%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)

service = DropboxSnapshotService()


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

    # get the user id
    user_id = service.get_user_id_from_access_token(access_token)

    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # check if snapshot with same name exists
    duplicate = service.check_duplicate_file_snapshot_name(user_id, snapshot_name)

    # if it is duplicate
    if duplicate:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="snapshot with name already exists",
        )

    # get email of user
    email = service.get_user_email_from_token(access_token)

    if email is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="unable to retrieve user email",
        )

    # get the files and permissions from dropbox api
    files, permissions = service.get_all_files_and_permissions_from_api(
        access_token, email
    )
    if files is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve files",
        )

    # create file snapshot
    created = service.create_file_snapshot(user_id, snapshot_name, files, permissions)
    if not created:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="snapshot creation failed",
        )

    # perform analysis of inherit and direct permissions
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

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # delete file snapshot
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

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # edit name of file snapshot
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

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # get list of file snapshot names
    names = service.get_file_snapshot_names(user_id)
    if names is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file snapshot names",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=names)


@router.get("/queries", tags=["queries"])
def get_recent_queries(authorize: AuthJWT = Depends()):
    """
    Get the 10 most recent queries
    :param authorize: retrieves access token
    :return: 10 recent queries as a list
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    # get email of user
    email = service.get_user_email_from_token(access_token)
    if email is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="unable to retrieve user email",
        )

    # get the recent queries searched by user
    queries = service.get_recent_queries(email)
    if queries is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve recent queries",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=queries)


@router.get("/files", tags=["file_snapshot"])
def get_file_snapshot(
    snapshot_name: str,
    offset: int = None,
    limit: int = None,
    folder_path: str = None,
    authorize: AuthJWT = Depends(),
):
    """
    operation: get all files under certain folder or drive
    :param snapshot_name:
    :param offset: what index to start
    :param limit: how many to retrieve
    :param folder_path: the path of shared drive or folder to retrieve files from
    :param authorize: user authentication
    :return:
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # files directly of folder path
    files = service.get_files_of_folder(
        user_id, snapshot_name, folder_path, offset, limit
    )

    if files is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of file under folder",
        )
    # permissions of file list
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

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # get email of user
    email = service.get_user_email_from_token(access_token)
    if email is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="unable to retrieve user email",
        )

    # check if the query is a valid format
    valid = service.validate_query(user_id, email, snapshot_name, query)

    # if not valid return the error message explaining reason of invalidness
    if type(valid) == str:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=valid,
        )

    # query result data
    query_result = service.process_query_search(user_id, email, snapshot_name, query)

    if query_result is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of files of query",
        )

    # access control requirement search
    if (
        len(query_result) == 2
        and type(query_result[0]) == list
        and type(query_result[1]) == dict
    ):
        files, permissions = query_result

    # normal query search
    else:
        files = query_result
        # get permissions of file list
        permissions = service.get_permission_of_files(user_id, snapshot_name, files)

    if permissions is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve list of permissions under folder",
        )
    data = {"files": files, "permissions": permissions}

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

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # get the difference between two snapshots
    difference = service.get_difference_of_two_snapshots(
        user_id, base_snapshot_name, compare_snapshot_name
    )
    if difference is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to perform file snapshot analysis",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=difference)


@router.get("/files/differences/sharing", tags=["file_snapshot"])
def get_file_folder_sharing_difference(
    snapshot_name: str, file_id: str, authorize: AuthJWT = Depends()
):
    """
    operation: get the permission difference between a file and folder
    :param snapshot_name: file snapshot name
    :param file_id: the id of file to perform the analysis
    :param authorize: user authentication
    :return:
        additional_folder_permissions: permissions that folder has but file doesn't
        changed_permissions: permissions that have been changed between folder and file
        additional_file_permissions: permissions that file has but folder doesn't
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # get difference between file and folder
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


@router.get("/files/members", tags=["file_snapshot"])
def get_unique_members_of_file_snapshot(
    snapshot_name: str, authorize: AuthJWT = Depends()
):
    """
    operation: get unique memberships of a file snapshot (for autocomplete)
    :param snapshot_name: file snapshot name
    :param authorize: user authentication
    :return: list of unique members
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # get the unique member emails and names that exist in permissions of file snapshot
    members = service.get_unique_members_of_file_snapshot(user_id, snapshot_name)
    if members is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve members",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=members)


@router.post("/access-controls", tags=["access_control_requirements"])
def create_access_control_requirements(
    access_control: DropboxAccessControlBody = Body(...), authorize: AuthJWT = Depends()
):
    """
    operation: creates an access control requirement
    :param access_control: the access control requirement body object
    :param authorize: user authentication
    :return: status code and content
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # check if access control requirement fields are duplicate
    duplicate = service.check_duplicate_access_control_requirement(
        user_id, access_control
    )

    # checking for duplicate access control requirement failed
    if duplicate is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to check if duplicate access control requirement exists",
        )

    # there exists a duplicate access control requirement
    if duplicate:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="access control requirement with same properties exists",
        )

    created = service.create_access_control_requirement(user_id, access_control)

    # creating an access control requirement failed
    if not created:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to create access control requirement",
        )

    # successfully created access control requirement
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="access control requirement created",
    )


@router.get("/access-controls", tags=["access_control_requirements"])
def get_access_control_requirements(authorize: AuthJWT = Depends()):
    """
    operation: retrieve the access control requirements
    :param authorize: user authentication
    :return: list of created access control requirements of user
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # get all access control requirements
    access_control_requirements = service.get_access_control_requirements(user_id)

    # failed to retrieve access control requirements
    if access_control_requirements is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve access control requirements",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=access_control_requirements
    )


@router.delete("/access-controls", tags=["access_control_requirements"])
def delete_access_control_requirements(
    body: DeleteAccessControlRequirementBody = Body(...), authorize: AuthJWT = Depends()
):
    """
    operation: deletes file snapshot
    :param body: file snapshot name
    :param authorize: user authentication
    :return: None
    """
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()
    access_control_requirement_name = body.name

    # get user id of user
    user_id = service.get_user_id_from_access_token(access_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="unable to retrieve user id"
        )

    # delete access control requirement
    deleted = service.delete_access_control_requirement(
        user_id, access_control_requirement_name
    )

    # deleting failed
    if not deleted:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to delete requirement",
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content="requirement deleted")
