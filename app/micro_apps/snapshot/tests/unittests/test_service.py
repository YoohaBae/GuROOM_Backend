import datetime
import pytest
import mock
from app.micro_apps.snapshot.services import service
from .mock.mock_google_auth import MockGoogleAuth
from .mock.mock_user_database import MockUserDataBase
from .mock.mock_google_drive import MockGoogleDrive
from .mock.mock_database import MockDB
from .mock.mock_analysis import MockAnalysis
from ..data import service_input

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"

mock_access_token = "ACCESS_TOKEN"


def mock_get_sharing_difference_of_two_files(
    user_id, snapshot_name, base_file_id, compare_file_id
):
    return [{"id": "PERMISSIONID1"}], [], [{"id": "PERMISSIONID4"}]


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.UserDataBase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(service.GoogleAuth, "get_user", MockGoogleAuth.get_user)
@mock.patch.object(service.UserDataBase, "get_user", MockUserDataBase.get_user)
def test_valid_get_user_id_from_token():
    user_id = service.get_user_id_from_token(mock_access_token)
    assert user_id == "MOCK_USER_ID1"


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.UserDataBase, "__init__", MockUserDataBase.__init__)
@mock.patch.object(service.GoogleAuth, "get_user", side_effect=Exception)
def test_invalid_get_user_id_from_token(google_auth_exception):
    user_id = service.get_user_id_from_token(mock_access_token)
    assert not user_id


@mock.patch.object(service.GoogleDrive, "__init__", MockGoogleDrive.__init__)
@mock.patch.object(
    service.GoogleDrive, "get_root_file_id", MockGoogleDrive.get_root_file_id
)
def test_valid_get_root_id_from_api():
    root_id = service.get_root_id_from_api(mock_access_token)
    assert root_id == "ROOTID1"


@mock.patch.object(service.GoogleDrive, "__init__", MockGoogleDrive.__init__)
@mock.patch.object(service.GoogleDrive, "get_root_file_id", side_effect=Exception)
def test_invalid_get_root_id_from_api(google_drive_exception):
    root_id = service.get_root_id_from_api(mock_access_token)
    assert not root_id


@mock.patch.object(service.GoogleDrive, "__init__", MockGoogleDrive.__init__)
@mock.patch.object(
    service.GoogleDrive, "get_shared_drives", MockGoogleDrive.get_shared_drives
)
def test_valid_get_all_shared_drives_from_api():
    shared_drives = service.get_all_shared_drives_from_api(mock_access_token)
    assert shared_drives


@mock.patch.object(service.GoogleDrive, "__init__", MockGoogleDrive.__init__)
@mock.patch.object(service.GoogleDrive, "get_shared_drives", side_effect=Exception)
def test_invalid_get_all_shared_drives_from_api(google_drive_exception):
    shared_drives = service.get_all_shared_drives_from_api(mock_access_token)
    assert not shared_drives


@mock.patch.object(service.GoogleDrive, "__init__", MockGoogleDrive.__init__)
@mock.patch.object(service.GoogleDrive, "get_files", MockGoogleDrive.get_files)
def test_valid_get_all_files_from_api():
    files = service.get_all_files_from_api(mock_access_token)
    assert files


@mock.patch.object(service.GoogleDrive, "__init__", MockGoogleDrive.__init__)
@mock.patch.object(service.GoogleDrive, "get_files", side_effect=Exception)
def test_invalid_get_all_files_from_api(google_drive_exception):
    files = service.get_all_files_from_api(mock_access_token)
    assert not files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "create_file_snapshot", MockDB.create_file_snapshot
)
def test_valid_create_file_snapshot():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_files = []
    mock_root_id = "ROOTID1"
    mock_shared_drives = []
    created = service.create_file_snapshot(
        mock_user_id, mock_snapshot_name, mock_files, mock_root_id, mock_shared_drives
    )
    assert created


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "create_file_snapshot", side_effect=Exception
)
def test_invalid_create_file_snapshot(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_files = []
    mock_root_id = "ROOTID1"
    mock_shared_drives = []
    created = service.create_file_snapshot(
        mock_user_id, mock_snapshot_name, mock_files, mock_root_id, mock_shared_drives
    )
    assert not created


@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    service.Analysis,
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


@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    service.Analysis, "calculate_permission_and_path", side_effect=Exception
)
def test_invalid_perform_inherit_direct_permission_analysis(analysis_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    calculated = service.perform_inherit_direct_permission_analysis(
        mock_user_id, mock_snapshot_name
    )
    assert not calculated


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "delete_file_snapshot", MockDB.delete_file_snapshot
)
def test_valid_delete_file_snapshot():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    deleted = service.delete_file_snapshot(mock_user_id, mock_snapshot_name)
    assert deleted


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "delete_file_snapshot", side_effect=Exception
)
def test_invalid_delete_file_snapshot(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    deleted = service.delete_file_snapshot(mock_user_id, mock_snapshot_name)
    assert not deleted


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "edit_file_snapshot_name", MockDB.edit_file_snapshot_name
)
def test_valid_edit_file_snapshot_name():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    new_mock_snapshot_name = "NEW_FILE_SNAPSHOT1"
    edited = service.edit_file_snapshot_name(
        mock_user_id, mock_snapshot_name, new_mock_snapshot_name
    )
    assert edited


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "edit_file_snapshot_name", side_effect=Exception
)
def test_invalid_edit_file_snapshot_name(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    new_mock_snapshot_name = "NEW_FILE_SNAPSHOT1"
    edited = service.edit_file_snapshot_name(
        mock_user_id, mock_snapshot_name, new_mock_snapshot_name
    )
    assert not edited


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_snapshot_names", MockDB.get_file_snapshot_names
)
def test_valid_get_file_snapshot_names():
    mock_user_id = "MOCK_USER_ID1"
    names = service.get_file_snapshot_names(mock_user_id)
    assert names


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(service.SnapshotDataBase, "get_file_snapshot_names", lambda x: [])
def test_valid_get_empty_file_snapshot_names():
    mock_user_id = "MOCK_USER_ID1"
    names = service.get_file_snapshot_names(mock_user_id)
    assert len(names) == 0


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_snapshot_names", side_effect=Exception
)
def test_invalid_get_file_snapshot_names(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    names = service.get_file_snapshot_names(mock_user_id)
    assert not names


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(service.SnapshotDataBase, "get_root_id", MockDB.get_root_id)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", MockDB.get_file_under_folder
)
def test_valid_get_files_of_my_drive():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    files = service.get_files_of_my_drive(mock_user_id, mock_snapshot_name)
    assert files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(service.SnapshotDataBase, "get_root_id", MockDB.get_root_id)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_file_under_folder",
    MockDB.get_empty_file_under_folder,
)
def test_valid_get_empty_files_of_my_drive():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    files = service.get_files_of_my_drive(mock_user_id, mock_snapshot_name)
    assert len(files) == 0


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(service.SnapshotDataBase, "get_root_id", MockDB.get_root_id)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", side_effect=Exception
)
def test_invalid_get_files_of_my_drive(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    files = service.get_files_of_my_drive(mock_user_id, mock_snapshot_name)
    assert not files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", MockDB.get_file_under_folder
)
@mock.patch.object(
    service.SnapshotDataBase, "get_files_with_no_path", MockDB.get_files_with_no_path
)
def test_valid_get_files_of_shared_with_me():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    files = service.get_files_of_shared_with_me(mock_user_id, mock_snapshot_name)
    assert files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", MockDB.get_file_under_folder
)
@mock.patch.object(
    service.SnapshotDataBase, "get_files_with_no_path", MockDB.get_files_with_no_path
)
def test_valid_get_files_of_shared_with_me_with_offset_limit():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_offset = 0
    mock_limit = 1
    files = service.get_files_of_shared_with_me(
        mock_user_id, mock_snapshot_name, mock_offset, mock_limit
    )
    assert len(files) == 1


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", MockDB.get_file_under_folder
)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_files_with_no_path",
    MockDB.get_empty_file_under_folder,
)
def test_valid_get_empty_files_of_shared_with_me():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    files = service.get_files_of_shared_with_me(mock_user_id, mock_snapshot_name)
    assert len(files) == 0


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", MockDB.get_file_under_folder
)
@mock.patch.object(
    service.SnapshotDataBase, "get_files_with_no_path", side_effect=Exception
)
def test_invalid_get_files_of_shared_with_me(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    files = service.get_files_of_shared_with_me(mock_user_id, mock_snapshot_name)
    assert not files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", MockDB.get_file_under_folder
)
def test_valid_get_files_of_shared_drive():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_drive_id = "SHAREDDRIVEID1"
    files = service.get_files_of_shared_drive(
        mock_user_id, mock_snapshot_name, mock_drive_id
    )
    assert files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_file_under_folder",
    MockDB.get_empty_file_under_folder,
)
def test_valid_get_empty_files_of_shared_drive():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_drive_id = "SHAREDDRIVEID1"
    files = service.get_files_of_shared_drive(
        mock_user_id, mock_snapshot_name, mock_drive_id
    )
    assert len(files) == 0


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", side_effect=Exception
)
def test_invalid_get_files_of_shared_drive(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_drive_id = "SHAREDDRIVEID1"
    files = service.get_files_of_shared_drive(
        mock_user_id, mock_snapshot_name, mock_drive_id
    )
    assert not files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", MockDB.get_file_under_folder
)
def test_valid_get_files_of_folder():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_id = "FILEID8"
    files = service.get_files_of_folder(
        mock_user_id, mock_snapshot_name, mock_folder_id
    )
    assert files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_file_under_folder",
    MockDB.get_empty_file_under_folder,
)
def test_valid_get_empty_files_of_folder():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_id = "FILEID8"
    files = service.get_files_of_folder(
        mock_user_id, mock_snapshot_name, mock_folder_id
    )
    assert len(files) == 0


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_file_under_folder", side_effect=Exception
)
def test_invalid_get_files_of_folder(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_id = "FILEID8"
    files = service.get_files_of_folder(
        mock_user_id, mock_snapshot_name, mock_folder_id
    )
    assert not files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
def test_valid_get_permission_of_files():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_files = service_input.mock_file_input
    permissions = service.get_permission_of_files(
        mock_user_id, mock_snapshot_name, mock_files
    )
    assert permissions


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_all_permission_of_file", side_effect=Exception
)
def test_invalid_get_permission_of_files(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_files = service_input.mock_file_input
    permissions = service.get_permission_of_files(
        mock_user_id, mock_snapshot_name, mock_files
    )
    assert not permissions


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(service.SnapshotDataBase, "get_root_id", MockDB.get_root_id)
@mock.patch.object(
    service.SnapshotDataBase, "get_shared_drives", MockDB.get_shared_drives
)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    service.Analysis, "get_sharing_differences", MockAnalysis.get_sharing_differences
)
def test_valid_get_files_with_diff_permission_from_folder():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    different_files = service.get_files_with_diff_permission_from_folder(
        mock_user_id, mock_snapshot_name
    )
    assert different_files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(service.SnapshotDataBase, "get_root_id", MockDB.get_root_id)
@mock.patch.object(
    service.SnapshotDataBase, "get_shared_drives", MockDB.get_shared_drives
)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    service.Analysis,
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


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_all_files_of_snapshot", side_effect=Exception
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
def test_invalid_get_files_with_diff_permission_from_folder(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    different_files = service.get_files_with_diff_permission_from_folder(
        mock_user_id, mock_snapshot_name
    )
    assert not different_files


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(service.SnapshotDataBase, "get_parent_id", MockDB.get_parent_id)
@mock.patch.object(
    service,
    "get_sharing_difference_of_two_files",
    mock_get_sharing_difference_of_two_files,
)
def test_valid_get_file_folder_sharing_difference():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID20"
    difference = service.get_file_folder_sharing_difference(
        mock_user_id, mock_snapshot_name, mock_file_id
    )
    assert difference


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(service.SnapshotDataBase, "get_parent_id", MockDB.get_parent_id)
@mock.patch.object(
    service, "get_sharing_difference_of_two_files", side_effect=Exception
)
def test_invalid_get_file_folder_sharing_difference(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID20"
    difference = service.get_file_folder_sharing_difference(
        mock_user_id, mock_snapshot_name, mock_file_id
    )
    assert not difference


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    service.Analysis, "get_sharing_differences", MockAnalysis.get_sharing_differences
)
def test_valid_get_sharing_difference_of_two_files():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_base_file_id = "FILEID20"
    mock_compare_file_id = "FILEID8"
    difference = service.get_sharing_difference_of_two_files(
        mock_user_id, mock_snapshot_name, mock_base_file_id, mock_compare_file_id
    )
    assert difference


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(service.Analysis, "get_sharing_differences", side_effect=Exception)
def test_invalid_get_sharing_difference_of_two_files(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_base_file_id = "FILEID20"
    mock_compare_file_id = "FILEID8"
    difference = service.get_sharing_difference_of_two_files(
        mock_user_id, mock_snapshot_name, mock_base_file_id, mock_compare_file_id
    )
    assert not difference


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    service.Analysis, "get_sharing_differences", MockAnalysis.get_sharing_differences
)
def test_valid_get_sharing_difference_of_two_files_different_snapshots():
    mock_user_id = "MOCK_USER_ID1"
    mock_base_snapshot_name = "FILE_SNAPSHOT1"
    mock_compare_snapshot_name = "FILE_SNAPSHOT2"
    mock_file_id = "FILEID1"
    difference = service.get_sharing_difference_of_two_files_different_snapshots(
        mock_user_id, mock_base_snapshot_name, mock_compare_snapshot_name, mock_file_id
    )
    assert difference


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_permission_of_file",
    MockDB.get_all_permission_of_file,
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(service.Analysis, "get_sharing_differences", side_effect=Exception)
def test_invalid_get_sharing_difference_of_two_files_different_snapshots(
    snapshot_db_exception,
):
    mock_user_id = "MOCK_USER_ID1"
    mock_base_snapshot_name = "FILE_SNAPSHOT1"
    mock_compare_snapshot_name = "FILE_SNAPSHOT2"
    mock_file_id = "FILEID1"
    difference = service.get_sharing_difference_of_two_files_different_snapshots(
        mock_user_id, mock_base_snapshot_name, mock_compare_snapshot_name, mock_file_id
    )
    assert not difference


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    service.Analysis,
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


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_files_of_snapshot",
    MockDB.get_all_files_of_snapshot,
)
@mock.patch.object(service.Analysis, "__init__", MockAnalysis.__init__)
@mock.patch.object(
    service.Analysis, "compare_two_file_snapshots", side_effect=Exception
)
def test_invalid_get_difference_of_two_snapshots(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_base_snapshot_name = "FILE_SNAPSHOT1"
    mock_compare_snapshot_name = "FILE_SNAPSHOT2"
    difference = service.get_difference_of_two_snapshots(
        mock_user_id, mock_base_snapshot_name, mock_compare_snapshot_name
    )
    assert not difference


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "get_shared_drives", MockDB.get_shared_drives
)
def test_valid_get_shared_drives():
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    shared_drives = service.get_shared_drives(mock_user_id, mock_snapshot_name)
    assert shared_drives


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(service.SnapshotDataBase, "get_shared_drives", side_effect=Exception)
def test_invalid_get_shared_drives(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    shared_drives = service.get_shared_drives(mock_user_id, mock_snapshot_name)
    assert not shared_drives


# @pytest.mark.asyncio
# async def test_valid_scratch_group_memberships_from_file():
#     file = open(absolute_path_to_data + "/Member_List_CS.html")
#     memberships = await service.scratch_group_memberships_from_file(file)
#     with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
#         data = json.load(json_file)
#         memberships_result = data[0]["memberships"]
#     assert memberships == memberships_result


@pytest.mark.asyncio
async def test_invalid_scratch_group_memberships_from_file():
    file = None
    memberships = await service.scratch_group_memberships_from_file(file)
    assert not memberships


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "create_group_memberships_snapshot",
    MockDB.create_group_memberships_snapshot,
)
def test_valid_create_group_snapshot():
    mock_user_id = "MOCK_USER_ID1"
    mock_group_name = "CSE416"
    mock_group_email = "cse416@cs.stonybrook.edu"
    mock_create_time = datetime.datetime.now()
    mock_memberships = []
    created = service.create_group_snapshot(
        mock_user_id,
        mock_group_name,
        mock_group_email,
        mock_create_time,
        mock_memberships,
    )
    assert created


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase, "create_group_memberships_snapshot", side_effect=Exception
)
def test_invalid_create_group_snapshot(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    mock_group_name = "CSE416"
    mock_group_email = "cse416@cs.stonybrook.edu"
    mock_create_time = datetime.datetime.now()
    mock_memberships = []
    created = service.create_group_snapshot(
        mock_user_id,
        mock_group_name,
        mock_group_email,
        mock_create_time,
        mock_memberships,
    )
    assert not created


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_group_membership_snapshots",
    MockDB.get_all_group_membership_snapshots,
)
def test_valid_get_recent_group_membership_snapshots():
    mock_user_id = "MOCK_USER_ID1"
    recent_group_snapshots = service.get_recent_group_membership_snapshots(mock_user_id)
    assert recent_group_snapshots


@mock.patch.object(service.SnapshotDataBase, "__init__", MockDB.__init__)
@mock.patch.object(
    service.SnapshotDataBase,
    "get_all_group_membership_snapshots",
    side_effect=Exception,
)
def test_invalid_get_recent_group_membership_snapshots(snapshot_db_exception):
    mock_user_id = "MOCK_USER_ID1"
    recent_group_snapshots = service.get_recent_group_membership_snapshots(mock_user_id)
    assert not recent_group_snapshots
