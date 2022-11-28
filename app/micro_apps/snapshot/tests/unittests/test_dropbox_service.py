import mock
import json
from app.micro_apps.snapshot.services.dropbox.service import (
    DropboxSnapshotService,
    DropboxAuth,
    DropboxAuthDatabase,
    DropboxDrive,
    DropboxSnapshotDatabase,
    DropboxAnalysis,
    DropboxQueryBuilder,
)
from .mock.mock_dropbox_auth import MockDropboxAuth
from .mock.mock_user_database import MockUserDataBase
from .mock.mock_dropbox_drive import MockDropboxDrive
from .mock.mock_dropbox_database import MockDB
from .mock.mock_dropbox_analysis import MockAnalysis
from .mock.mock_dropbox_query_builder import MockQueryBuilder
from ..data.dropbox import service_input

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"

mock_access_token = "ACCESS_TOKEN"

service = DropboxSnapshotService()


def mock_get_sharing_difference_of_two_files(
    user_id, snapshot_name, base_file_id, compare_file_id
):
    return [{"id": "PERMISSIONID1"}], [], [{"id": "PERMISSIONID4"}]


def mock_get_files_with_diff_permission_from_folder(user_id, snapshot_name):
    with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
        data = json.load(json_file)
        return data


def mock_get_recent_group_membership_snapshots(user_id):
    with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
        data = json.load(json_file)
        return data


@mock.patch.object(DropboxAuth, "__init__", MockDropboxAuth.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxAuth, "get_user", MockDropboxAuth.get_user)
@mock.patch.object(DropboxAuthDatabase, "get_user", MockUserDataBase.get_user)
def test_valid_get_user_id_from_token():
    user_id = service.get_user_id_from_access_token(mock_access_token)
    assert user_id == "MOCK_USER_ID2"


@mock.patch.object(DropboxAuth, "__init__", MockDropboxAuth.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxAuth, "get_user", side_effect=Exception)
def test_invalid_get_user_id_from_token(dropbox_auth_exception):
    user_id = service.get_user_id_from_access_token(mock_access_token)
    assert not user_id


@mock.patch.object(DropboxAuth, "__init__", MockDropboxAuth.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxAuth, "get_user", MockDropboxAuth.get_user)
@mock.patch.object(DropboxAuthDatabase, "get_user", MockUserDataBase.get_user)
def test_valid_get_user_email_from_token():
    user_email = service.get_user_email_from_token(mock_access_token)
    assert user_email == "yooha.bae@stonybrook.edu"


@mock.patch.object(DropboxAuth, "__init__", MockDropboxAuth.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxAuth, "get_user", side_effect=Exception)
def test_invalid_get_user_email_from_token(dropbox_auth_exception):
    user_email = service.get_user_email_from_token(mock_access_token)
    assert not user_email


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "check_duplicate_file_snapshot_name",
    DropboxSnapshotDatabase.check_duplicate_file_snapshot_name,
)
def test_valid_check_duplicate_file_snapshot_name():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    duplicate = service.check_duplicate_file_snapshot_name(
        mock_user_id, mock_snapshot_name
    )
    assert not duplicate


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "check_duplicate_file_snapshot_name", side_effect=Exception
)
def test_invalid_check_duplicate_file_snapshot_name(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    duplicate = service.check_duplicate_file_snapshot_name(
        mock_user_id, mock_snapshot_name
    )
    assert duplicate is None


@mock.patch.object(DropboxDrive, "__init__", MockDropboxDrive.__init__)
@mock.patch.object(DropboxDrive, "get_files", MockDropboxDrive.get_files)
@mock.patch.object(
    DropboxDrive, "get_permissions_of_files", MockDropboxDrive.get_permissions_of_files
)
@mock.patch.object(
    DropboxDrive,
    "get_permissions_of_shared_folders",
    MockDropboxDrive.get_permissions_of_shared_folders,
)
def test_valid_get_all_files_from_api():
    mock_email = "yooha.bae@stonybrook.edu"
    files, permissions = service.get_all_files_and_permissions_from_api(
        mock_access_token, mock_email
    )
    assert files
    assert permissions


@mock.patch.object(DropboxDrive, "__init__", MockDropboxDrive.__init__)
@mock.patch.object(DropboxDrive, "get_files", side_effect=Exception)
def test_invalid_get_all_files_from_api(dropbox_drive_exception):
    mock_email = "yooha.bae@stonybrook.edu"
    files, permissions = service.get_all_files_and_permissions_from_api(
        mock_access_token, mock_email
    )
    assert not files
    assert not permissions


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "create_file_snapshot", MockDB.create_file_snapshot
)
def test_valid_create_file_snapshot():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_files = []
    mock_permissions = []
    created = service.create_file_snapshot(
        mock_user_id, mock_snapshot_name, mock_files, mock_permissions
    )
    assert created


@mock.patch.object(service, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "create_file_snapshot", side_effect=Exception
)
def test_invalid_create_file_snapshot(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_files = []
    mock_permissions = []
    created = service.create_file_snapshot(
        mock_user_id, mock_snapshot_name, mock_files, mock_permissions
    )
    assert not created


@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAnalysis,
    "calculate_permission_and_path",
    MockAnalysis.calculate_permission_and_path,
)
def test_valid_perform_inherit_direct_permission_analysis():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    calculated = service.perform_inherit_direct_permission_analysis(
        mock_user_id, mock_snapshot_name
    )
    assert calculated


@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAnalysis, "calculate_permission_and_path", side_effect=Exception
)
def test_invalid_perform_inherit_direct_permission_analysis(analysis_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    calculated = service.perform_inherit_direct_permission_analysis(
        mock_user_id, mock_snapshot_name
    )
    assert not calculated


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "delete_file_snapshot", MockDB.delete_file_snapshot
)
def test_valid_delete_file_snapshot():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    deleted = service.delete_file_snapshot(mock_user_id, mock_snapshot_name)
    assert deleted


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "delete_file_snapshot", side_effect=Exception
)
def test_invalid_delete_file_snapshot(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    deleted = service.delete_file_snapshot(mock_user_id, mock_snapshot_name)
    assert not deleted


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "edit_file_snapshot_name", MockDB.edit_file_snapshot_name
)
def test_valid_edit_file_snapshot_name():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    new_mock_snapshot_name = "NEW_FILE_SNAPSHOT1"
    edited = service.edit_file_snapshot_name(
        mock_user_id, mock_snapshot_name, new_mock_snapshot_name
    )
    assert edited


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "edit_file_snapshot_name", side_effect=Exception
)
def test_invalid_edit_file_snapshot_name(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    new_mock_snapshot_name = "NEW_FILE_SNAPSHOT1"
    edited = service.edit_file_snapshot_name(
        mock_user_id, mock_snapshot_name, new_mock_snapshot_name
    )
    assert not edited


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_file_snapshot_names", MockDB.get_file_snapshot_names
)
def test_valid_get_file_snapshot_names():
    mock_user_id = "MOCK_USER_ID1"
    names = service.get_file_snapshot_names(mock_user_id)
    assert names


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxSnapshotDatabase, "get_file_snapshot_names", lambda x: [])
def test_valid_get_empty_file_snapshot_names():
    mock_user_id = "MOCK_USER_ID1"
    names = service.get_file_snapshot_names(mock_user_id)
    assert len(names) == 0


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_file_snapshot_names", side_effect=Exception
)
def test_invalid_get_file_snapshot_names(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    names = service.get_file_snapshot_names(mock_user_id)
    assert not names


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_file_under_folder", MockDB.get_file_under_folder
)
def test_valid_get_files_of_folder():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_path = "/WeByte"
    files = service.get_files_of_folder(mock_user_id, mock_snapshot_name, mock_path)
    assert files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_file_under_folder", side_effect=Exception
)
def test_invalid_get_files_of_folder(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_id = "id:FILE_ID13"
    files = service.get_files_of_folder(
        mock_user_id, mock_snapshot_name, mock_folder_id
    )
    assert not files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
def test_valid_get_permission_of_files():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_files = [{"id": "id:FILE_ID1"}, {"id": "id:FILE_ID2"}]
    permissions = service.get_permission_of_files(
        mock_user_id, mock_snapshot_name, mock_files
    )
    assert permissions


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_all_permission_of_file", side_effect=Exception
)
def test_invalid_get_permission_of_files(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_files = service_input.mock_file_input
    permissions = service.get_permission_of_files(
        mock_user_id, mock_snapshot_name, mock_files
    )
    assert not permissions


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_files_of_file_ids", MockDB.get_files_of_file_ids
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAnalysis, "get_sharing_differences", MockAnalysis.get_sharing_differences
)
def test_valid_check_if_files_have_different_permissions_from_folder():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_ids = ["id:FILE_ID1", "id:FILE_ID2", "id:FILE_ID3", "id:FILE_ID4"]
    different_files = service.check_if_files_have_different_permission_from_folder(
        mock_user_id, mock_snapshot_name, mock_file_ids
    )
    assert different_files


@mock.patch.object(
    DropboxSnapshotDatabase, "get_files_of_file_ids", side_effect=Exception
)
def test_invalid_check_if_files_have_different_permissions_from_folder(
    snapshot_db_exception,
):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_ids = ["id:FILE_ID13", "id:FILE_ID15", "id:FILE_ID10"]
    different_files = service.check_if_files_have_different_permission_from_folder(
        mock_user_id, mock_snapshot_name, mock_file_ids
    )
    assert not different_files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_file_id_of_name",
    MockDB.get_file_id_of_name,
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAnalysis, "get_sharing_differences", MockAnalysis.get_sharing_differences
)
def test_valid_get_files_with_diff_permission_from_folder():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    different_files = service.get_files_with_diff_permission_from_folder(
        mock_user_id, mock_snapshot_name
    )
    assert different_files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_file_id_of_name", MockDB.get_file_id_of_name
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAnalysis,
    "get_sharing_differences",
    MockAnalysis.get_empty_sharing_differences,
)
def test_valid_get_empty_files_with_diff_permission_from_folder():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    different_files = service.get_files_with_diff_permission_from_folder(
        mock_user_id, mock_snapshot_name
    )
    assert len(different_files) == 0


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_all_files_of_snapshot", side_effect=Exception
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
def test_invalid_get_files_with_diff_permission_from_folder(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    different_files = service.get_files_with_diff_permission_from_folder(
        mock_user_id, mock_snapshot_name
    )
    assert not different_files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxSnapshotDatabase, "get_path_of_file", MockDB.get_path_of_file)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_file_id_of_name", MockDB.get_file_id_of_name
)
@mock.patch.object(
    service,
    "get_sharing_difference_of_two_files",
    mock_get_sharing_difference_of_two_files,
)
def test_valid_get_file_folder_sharing_difference():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "id:FILE_ID15"
    difference = service.get_file_folder_sharing_difference(
        mock_user_id, mock_snapshot_name, mock_file_id
    )
    assert difference


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    service, "get_sharing_difference_of_two_files", side_effect=Exception
)
def test_invalid_get_file_folder_sharing_difference(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILE_ID15"
    difference = service.get_file_folder_sharing_difference(
        mock_user_id, mock_snapshot_name, mock_file_id
    )
    assert not difference


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAnalysis, "get_sharing_differences", MockAnalysis.get_sharing_differences
)
def test_valid_get_sharing_difference_of_two_files():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_base_file_id = "id:FILE_ID15"
    mock_compare_file_id = "id:FILE_ID1"
    difference = service.get_sharing_difference_of_two_files(
        mock_user_id, mock_snapshot_name, mock_base_file_id, mock_compare_file_id
    )
    assert difference


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(DropboxAnalysis, "get_sharing_differences", side_effect=Exception)
def test_invalid_get_sharing_difference_of_two_files(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_base_file_id = "id:FILE_ID15"
    mock_compare_file_id = "id:FILE_ID1"
    difference = service.get_sharing_difference_of_two_files(
        mock_user_id, mock_snapshot_name, mock_base_file_id, mock_compare_file_id
    )
    assert not difference


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAnalysis,
    "compare_two_file_snapshots",
    MockAnalysis.compare_two_file_snapshots,
)
def test_valid_get_difference_of_two_snapshots():
    mock_user_id = "MOCK_USER_ID1"
    mock_base_snapshot_name = "FILE_SNAPSHOT1"
    mock_compare_snapshot_name = "FILE_SNAPSHOT2"
    difference = service.get_difference_of_two_snapshots(
        mock_user_id, mock_base_snapshot_name, mock_compare_snapshot_name
    )
    assert difference


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(DropboxAnalysis, "compare_two_file_snapshots", side_effect=Exception)
def test_invalid_get_difference_of_two_snapshots(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_base_snapshot_name = "FILE_SNAPSHOT1"
    mock_compare_snapshot_name = "FILE_SNAPSHOT2"
    difference = service.get_difference_of_two_snapshots(
        mock_user_id, mock_base_snapshot_name, mock_compare_snapshot_name
    )
    assert not difference


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(
    DropboxAuthDatabase,
    "update_or_push_recent_queries",
    MockDB.update_or_push_recent_queries,
)
@mock.patch.object(
    DropboxQueryBuilder, "get_files_of_query", MockQueryBuilder.get_files_of_query
)
def test_valid_process_query_search():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "drive:MyDrive"
    files = service.process_query_search(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(
    DropboxAuthDatabase,
    "update_or_push_recent_queries",
    MockDB.update_or_push_recent_queries,
)
@mock.patch.object(
    service,
    "get_files_with_diff_permission_from_folder",
    mock_get_files_with_diff_permission_from_folder,
)
def test_valid_is_file_folder_diff_process_query_search():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "is:file_folder_diff and file_ids:[]"
    files = service.process_query_search(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(
    DropboxAuthDatabase,
    "update_or_push_recent_queries",
    MockDB.update_or_push_recent_queries,
)
@mock.patch.object(
    service,
    "get_files_with_diff_permission_from_folder",
    mock_get_files_with_diff_permission_from_folder,
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_file_id_of_name",
    MockDB.get_file_id_of_name,
)
@mock.patch.object(
    DropboxSnapshotDatabase, "get_files_of_file_ids", MockDB.get_files_of_file_ids
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAnalysis, "get_sharing_differences", MockAnalysis.get_sharing_differences
)
def test_valid_is_file_folder_diff_process_query_search_with_file_ids():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = 'is:file_folder_diff and file_ids:["id:FILE_ID15"]'
    files = service.process_query_search(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAuthDatabase,
    "update_or_push_recent_queries",
    MockDB.update_or_push_recent_queries,
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_access_control_requirement",
    MockDB.get_access_control_requirement,
)
@mock.patch.object(
    DropboxQueryBuilder, "get_files_of_query", MockQueryBuilder.get_files_of_query
)
@mock.patch.object(
    DropboxAnalysis,
    "tag_files_and_permissions_with_violation",
    MockAnalysis.tag_files_and_permissions_with_violation,
)
def test_valid_access_control_requirements_process_query_search():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "accessControl:ACR#2"
    files = service.process_query_search(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(DropboxAnalysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    DropboxAuthDatabase,
    "update_or_push_recent_queries",
    MockDB.update_or_push_recent_queries,
)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_access_control_requirement",
    MockDB.get_access_control_requirement,
)
@mock.patch.object(
    DropboxQueryBuilder, "get_files_of_query", MockQueryBuilder.get_files_of_query
)
@mock.patch.object(
    DropboxAnalysis, "tag_files_and_permissions_with_violation", side_effect=Exception
)
def test_invalid_access_control_requirements_process_query_search(
    google_analysis_exception,
):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "accessControl:ACR#4"
    files = service.process_query_search(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert not files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(
    DropboxAuthDatabase, "update_or_push_recent_queries", side_effect=Exception
)
def test_invalid_process_query_search(dropbox_auth_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "drive:MyDrive"
    files = service.process_query_search(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert not files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(
    DropboxQueryBuilder,
    "create_tree_and_validate",
    MockQueryBuilder.create_tree_and_validate,
)
def test_valid_validate_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "drive:MyDrive"
    validated = service.validate_query(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert validated


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(
    DropboxQueryBuilder,
    "create_tree_and_validate",
    MockQueryBuilder.create_tree_and_validate,
)
def test_valid_is_file_folder_diff_validate_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "is:file_folder_diff and file_ids=[]"
    validated = service.validate_query(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert validated


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_access_control_requirement",
    MockDB.get_access_control_requirement,
)
@mock.patch.object(
    DropboxQueryBuilder,
    "create_tree_and_validate",
    MockQueryBuilder.create_tree_and_validate,
)
def test_valid_access_control_requirement_validate_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "accessControl:ACR#4"
    validated = service.validate_query(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert validated


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_access_control_requirement",
    MockDB.get_access_control_requirement,
)
@mock.patch.object(
    DropboxQueryBuilder,
    "create_tree_and_validate",
    MockQueryBuilder.create_tree_and_validate,
)
def test_invalid_access_control_requirement_validate_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "accessControl:ACR#4 and drive:MyDrive"
    validated = service.validate_query(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert (
        validated
        == "Invalid Query: Access Control Requirements cannot be searched with other queries"
    )


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_access_control_requirement",
    MockDB.get_access_control_requirement,
)
@mock.patch.object(
    DropboxQueryBuilder,
    "create_tree_and_validate",
    MockQueryBuilder.create_tree_and_validate,
)
def test_invalid_access_control_requirement_validate_query2():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "accessControl:INVALID_ACR"
    validated = service.validate_query(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert (
        validated
        == "No Such Requirement: There is no access control requirement named :INVALID_ACR"
    )


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxQueryBuilder, "__init__", MockQueryBuilder.__init__)
@mock.patch.object(
    DropboxQueryBuilder,
    "create_tree_and_validate",
    MockQueryBuilder.create_tree_and_validate,
)
def test_invalid_validate_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    mock_query = "is:file_folder_diff and drive:MyDrive"
    validated = service.validate_query(
        mock_user_id, mock_email, mock_snapshot_name, mock_query
    )
    assert (
        validated
        == "Invalid Query: invalid format of file folder sharing difference query"
    )


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_all_members_from_permissions",
    MockDB.get_all_members_from_permissions,
)
def test_valid_get_unique_members_of_file_snapshot():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    unique_members = service.get_unique_members_of_file_snapshot(
        mock_user_id, mock_snapshot_name
    )
    assert unique_members


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
def test_invalid_get_unique_members_of_file_snapshot():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    unique_members = service.get_unique_members_of_file_snapshot(
        mock_user_id, mock_snapshot_name
    )
    assert not unique_members


@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(
    DropboxAuthDatabase,
    "get_recent_queries",
    MockUserDataBase.get_recent_queries,
)
def test_valid_get_recent_queries():
    mock_email = "yooha.bae@stonybrook.edu"
    recent_queries = service.get_recent_queries(mock_email)
    assert recent_queries


@mock.patch.object(DropboxAuthDatabase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(DropboxAuthDatabase, "get_recent_queries", side_effect=Exception)
def test_invalid_get_recent_queries(dropbox_auth_exception):
    mock_email = "yooha.bae@stonybrook.edu"
    recent_queries = service.get_recent_queries(mock_email)
    assert not recent_queries


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "create_access_control_requirement",
    MockDB.create_access_control_requirement,
)
def test_valid_create_access_control_requirement():
    mock_user_id = "MOCK_USER_ID1"
    mock_access_control = {
        "name": "ACR",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": True,
    }
    created = service.create_access_control_requirement(
        mock_user_id, mock_access_control
    )
    assert created


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "create_access_control_requirement", side_effect=Exception
)
def test_invalid_create_access_control_requirement(create_acr_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_access_control = {
        "name": "ACR",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": True,
    }
    created = service.create_access_control_requirement(
        mock_user_id, mock_access_control
    )
    assert not created


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "check_duplicate_access_control_requirement",
    MockDB.check_duplicate_access_control_requirement,
)
def test_valid_duplicate_check_duplicate_access_control_requirement():
    mock_user_id = "MOCK_USER_ID1"
    mock_access_control = {
        "name": "ACR#2",
        "query": "drive:WeByte",
        "AR": [],
        "AW": ["yooha.bae@stonybrook.edu"],
        "DR": [],
        "DW": ["yoolbi.lee@stonybrook.edu"],
        "Grp": False,
    }

    duplicate = service.check_duplicate_access_control_requirement(
        mock_user_id, mock_access_control
    )
    assert duplicate


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "check_duplicate_access_control_requirement",
    MockDB.check_duplicate_access_control_requirement,
)
def test_valid_not_duplicate_check_duplicate_access_control_requirement():
    mock_user_id = "MOCK_USER_ID1"
    mock_access_control = {
        "name": "ACR#2",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": [],
        "DW": ["yoollee@cs.stonybrook.edu"],
        "Grp": False,
    }
    duplicate = service.check_duplicate_access_control_requirement(
        mock_user_id, mock_access_control
    )
    assert not duplicate


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "check_duplicate_access_control_requirement",
    side_effect=Exception,
)
def test_invalid_check_duplicate_access_control_requirement(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_access_control = {
        "name": "ACR#2",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": [],
        "DW": ["yoollee@cs.stonybrook.edu"],
        "Grp": False,
    }
    duplicate = service.check_duplicate_access_control_requirement(
        mock_user_id, mock_access_control
    )
    assert duplicate is None


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_access_control_requirements",
    MockDB.get_access_control_requirements,
)
def test_valid_get_access_control_requirements():
    mock_user_id = "MOCK_USER_ID1"
    access_control_requirements = service.get_access_control_requirements(mock_user_id)
    assert access_control_requirements


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "get_access_control_requirements",
    side_effect=Exception,
)
def test_invalid_get_access_control_requirements(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    access_control_requirements = service.get_access_control_requirements(mock_user_id)
    assert access_control_requirements is None


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase,
    "delete_access_control_requirement",
    MockDB.delete_access_control_requirement,
)
def test_valid_delete_access_control_requirements():
    mock_user_id = "MOCK_USER_ID1"
    mock_access_control_requirement_name = "MOCK_ACR#2"
    deleted = service.delete_access_control_requirement(
        mock_user_id, mock_access_control_requirement_name
    )
    assert deleted


@mock.patch.object(DropboxSnapshotDatabase, "__init__", MockDB.__init__)
@mock.patch.object(
    DropboxSnapshotDatabase, "delete_access_control_requirement", side_effect=Exception
)
def test_invalid_delete_access_control_requirements(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_access_control_requirement_name = "MOCK_ACR#2"
    deleted = service.delete_access_control_requirement(
        mock_user_id, mock_access_control_requirement_name
    )
    assert not deleted
