import mock
import json
from app.micro_apps.snapshot.tests.unittests.mock.mock_dropbox_database import MockDB
from app.micro_apps.snapshot.services.dropbox.analysis import DropboxAnalysis
from app.micro_apps.snapshot.tests.data.dropbox.analysis_result import (
    sharing_changes_result,
    compare_snapshot_result,
)

mock_user_id = "MOCK_USER_ID1"
absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"


def new_init(self, user_id):
    self._snapshot_db = MockDB(user_id)
    self.user_id = user_id
    self.base_path = ""


@mock.patch.object(DropboxAnalysis, "__init__", new_init)
@mock.patch.object(DropboxAnalysis, "dfs", return_value=None)
def test_calculate_permission_and_path(mock_dfs):
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_DropboxAnalysis = DropboxAnalysis(mock_user_id)
    mock_DropboxAnalysis.calculate_permission_and_path(mock_snapshot_name)


@mock.patch.object(DropboxAnalysis, "__init__", new_init)
def test_dfs_for_my_drive():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_DropboxAnalysis = DropboxAnalysis(mock_user_id)
    visited = []
    curr_folder_path = "/WeByte"
    curr_permission = []
    file_id = "id:FILE_ID13"
    mock_DropboxAnalysis.dfs(
        visited, curr_folder_path, curr_permission, mock_snapshot_name, file_id
    )


@mock.patch.object(DropboxAnalysis, "__init__", new_init)
def test_get_sharing_differences():
    mock_DropboxAnalysis = DropboxAnalysis(mock_user_id)
    mock_base_permission_file_id = "id:FILE_ID15"
    mock_compare_permission_file_id = "id:FILE_ID13"
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
    ) = mock_DropboxAnalysis.get_sharing_differences(
        mock_base_permissions, mock_compare_permissions
    )
    base_permissions_more_ids = [p["id"] for p in base_permissions_more]
    compare_permissions_more_ids = [p["id"] for p in compare_permissions_more]
    assert base_permissions_more_ids == [
        "dbid:PERMISSIONID25",
        "dbid:PERMISSIONID26",
        "dbid:PERMISSIONID27",
        "dbid:PERMISSIONID28",
    ]
    assert sharing_changes == sharing_changes_result
    assert compare_permissions_more_ids == [
        "dbid:PERMISSIONID20",
        "dbid:PERMISSIONID21",
        "dbid:PERMISSIONID22",
    ]


@mock.patch.object(DropboxAnalysis, "__init__", new_init)
def test_compare_two_file_snapshots():
    mock_DropboxAnalysis = DropboxAnalysis(mock_user_id)
    mock_base_snapshot_name = "FILE_SNAPSHOT1"
    mock_compare_snapshot_name = "FILE_SNAPSHOT2"
    with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
        mock_base_snapshot_files = json.load(json_file)
    with open(absolute_path_to_data + "/snapshot2_files.json") as json_file:
        mock_compare_snapshot_files = json.load(json_file)
    different_files = mock_DropboxAnalysis.compare_two_file_snapshots(
        mock_base_snapshot_name,
        mock_compare_snapshot_name,
        mock_base_snapshot_files,
        mock_compare_snapshot_files,
    )
    assert different_files == compare_snapshot_result


@mock.patch.object(DropboxAnalysis, "__init__", new_init)
def test_tag_files_and_permissions_with_violation():
    mock_DropboxAnalysis = DropboxAnalysis(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
        mock_files = json.load(json_file)
    with open(absolute_path_to_data + "/access_control_requirement.json") as json_file:
        data = json.load(json_file)
        mock_access_control_requirement = data[0]
    (
        violated_files,
        violated_permissions,
    ) = mock_DropboxAnalysis.tag_files_and_permissions_with_violation(
        mock_snapshot_name, mock_files, mock_access_control_requirement
    )
    violated_file_ids = [f["id"] for f in violated_files]
    violated_permission_ids = [p["id"] for p in violated_permissions]
    assert violated_file_ids == [
        "id:FILE_ID7",
        "id:FILE_ID9",
        "id:FILE_ID10",
        "id:FILE_ID11",
        "id:FILE_ID12",
        "id:FILE_ID13",
        "id:FILE_ID14",
        "id:FILE_ID15",
    ]
    assert violated_permission_ids == [
        "dbid:PERMISSIONID5",
        "dbid:PERMISSIONID6",
        "dbid:PERMISSIONID8",
        "dbid:PERMISSIONID9",
        "dbid:PERMISSIONID10",
        "dbid:PERMISSIONID11",
        "dbid:PERMISSIONID12",
        "dbid:PERMISSIONID13",
        "dbid:PERMISSIONID14",
        "dbid:PERMISSIONID15",
        "dbid:PERMISSIONID16",
        "dbid:PERMISSIONID17",
        "dbid:PERMISSIONID18",
        "dbid:PERMISSIONID19",
        "dbid:PERMISSIONID20",
        "dbid:PERMISSIONID21",
        "dbid:PERMISSIONID22",
        "dbid:PERMISSIONID23",
        "dbid:PERMISSIONID24",
        "dbid:PERMISSIONID25",
        "dbid:PERMISSIONID26",
        "dbid:PERMISSIONID27",
        "dbid:PERMISSIONID28",
    ]


@mock.patch.object(DropboxAnalysis, "__init__", new_init)
def test_tag_files_and_permissions_with_violation2():
    mock_DropboxAnalysis = DropboxAnalysis(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
        mock_files = json.load(json_file)
    with open(absolute_path_to_data + "/access_control_requirement.json") as json_file:
        data = json.load(json_file)
        mock_access_control_requirement = data[1]
    (
        violated_files,
        violated_permissions,
    ) = mock_DropboxAnalysis.tag_files_and_permissions_with_violation(
        mock_snapshot_name, mock_files, mock_access_control_requirement
    )
    violated_file_ids = [f["id"] for f in violated_files]
    violated_permission_ids = [p["id"] for p in violated_permissions]
    assert violated_file_ids == [
        "id:FILE_ID5",
        "id:FILE_ID7",
        "id:FILE_ID9",
        "id:FILE_ID10",
        "id:FILE_ID11",
        "id:FILE_ID12",
        "id:FILE_ID13",
        "id:FILE_ID14",
        "id:FILE_ID15",
    ]
    assert violated_permission_ids == [
        "dbid:PERMISSIONID2",
        "dbid:PERMISSIONID3",
        "dbid:PERMISSIONID5",
        "dbid:PERMISSIONID6",
        "dbid:PERMISSIONID8",
        "dbid:PERMISSIONID9",
        "dbid:PERMISSIONID10",
        "dbid:PERMISSIONID11",
        "dbid:PERMISSIONID12",
        "dbid:PERMISSIONID13",
        "dbid:PERMISSIONID14",
        "dbid:PERMISSIONID15",
        "dbid:PERMISSIONID16",
        "dbid:PERMISSIONID17",
        "dbid:PERMISSIONID18",
        "dbid:PERMISSIONID19",
        "dbid:PERMISSIONID20",
        "dbid:PERMISSIONID21",
        "dbid:PERMISSIONID22",
        "dbid:PERMISSIONID23",
        "dbid:PERMISSIONID24",
        "dbid:PERMISSIONID25",
        "dbid:PERMISSIONID26",
        "dbid:PERMISSIONID27",
        "dbid:PERMISSIONID28",
    ]
