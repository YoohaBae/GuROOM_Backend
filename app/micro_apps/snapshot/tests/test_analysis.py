import mock
import json
from .mock.mockDatabase import MockDB
from ..services.analysis import Analysis
from .data.analysis_result import (
    base_permissions_more_result,
    sharing_changes_result,
    compare_permissions_more_result,
    compare_snapshot_result,
)

mock_user_id = "3243568dalewklgfhjfhsdjkl32ljk"
absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


def new_init(self, user_id):
    self.db = MockDB(user_id)
    self.user_id = user_id
    self.shared_with_me_drive_path = "/SharedWithMe"
    self.my_drive_path = "/MyDrive"


@mock.patch.object(Analysis, "__init__", new_init)
@mock.patch.object(Analysis, "dfs", return_value=None)
@mock.patch.object(Analysis, "dfs_shared", return_value=None)
@mock.patch.object(Analysis, "update_inherited_shared", return_value=None)
def test_calculate_permission_and_path(
    mock_dfs, mock_dfs_shared, mock_update_inherited_shared
):
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_analysis = Analysis(mock_user_id)
    mock_analysis.calculate_permission_and_path(mock_snapshot_name)


@mock.patch.object(Analysis, "__init__", new_init)
def test_update_inherited_shared():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_analysis = Analysis(mock_user_id)
    mock_analysis.update_inherited_shared(mock_snapshot_name)


@mock.patch.object(Analysis, "__init__", new_init)
def test_dfs_for_my_drive():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_analysis = Analysis(mock_user_id)
    visited = []
    curr_folder_path = "/MyDrive"
    curr_permission = []
    file_id = mock_analysis.db.get_root_id(mock_snapshot_name)
    mock_analysis.dfs(
        visited, curr_folder_path, curr_permission, mock_snapshot_name, file_id
    )


@mock.patch.object(Analysis, "__init__", new_init)
def test_dfs_shared():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_analysis = Analysis(mock_user_id)
    visited = []
    sample_shared_drive = {}
    with open(absolute_path_to_data + "/file_snapshots.json") as json_file:
        data = json.load(json_file)
        for file_snapshot in data:
            if file_snapshot["name"] == mock_snapshot_name:
                sample_shared_drive = file_snapshot["shared_drives"][0]
    curr_folder_path = "/" + sample_shared_drive["name"]
    folder_id = sample_shared_drive["id"]
    mock_analysis.dfs_shared(visited, curr_folder_path, mock_snapshot_name, folder_id)


@mock.patch.object(Analysis, "__init__", new_init)
def test_get_sharing_differences():
    mock_analysis = Analysis(mock_user_id)
    mock_base_permission_file_id = "FILEID4"
    mock_compare_permission_file_id = "FILEID5"
    mock_base_permissions = []
    mock_compare_permissions = []
    with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
        data = json.load(json_file)
        for permission in data:
            if permission["file_id"] == mock_base_permission_file_id:
                mock_base_permissions.append(permission)
            elif permission["file_id"] == mock_compare_permission_file_id:
                mock_compare_permissions.append(permission)
    (
        base_permissions_more,
        sharing_changes,
        compare_permissions_more,
    ) = mock_analysis.get_sharing_differences(
        mock_base_permissions, mock_compare_permissions
    )
    assert base_permissions_more == base_permissions_more_result
    assert sharing_changes == sharing_changes_result
    assert compare_permissions_more == compare_permissions_more_result


# TODO: create FILE_SNAPSHOT2 data
@mock.patch.object(Analysis, "__init__", new_init)
def test_compare_two_file_snapshots():
    mock_analysis = Analysis(mock_user_id)
    mock_base_snapshot_name = "FILE_SNAPSHOT1"
    mock_compare_snapshot_name = "FILE_SNAPSHOT2"
    with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
        mock_base_snapshot_files = json.load(json_file)
    with open(absolute_path_to_data + "/snapshot2_files.json") as json_file:
        mock_compare_snapshot_files = json.load(json_file)
    different_files = mock_analysis.compare_two_file_snapshots(
        mock_base_snapshot_name,
        mock_compare_snapshot_name,
        mock_base_snapshot_files,
        mock_compare_snapshot_files,
    )
    assert different_files == compare_snapshot_result
