import mock
import json
from app.micro_apps.snapshot.endpoints.models.access_control import AccessControlBody
from app.micro_apps.snapshot.services.dropbox.analysis import DropboxSnapshotDatabase
from app.micro_apps.snapshot.tests.unittests.mock.mock_dropbox_mongodb import (
    MockMongoDB,
)
from app.micro_apps.snapshot.tests.data.dropbox.database_result import DataBaseResult

mock_user_id = "MOCK_USER_ID1"
absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"


def new_init(self, user_id):
    db_name = None
    url = None
    self._db = MockMongoDB(url, db_name)
    self.user_id = user_id


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_check_duplicate_file_snapshot_name():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    duplicate = mock_DropboxSnapshotDatabase.check_duplicate_file_snapshot_name(
        mock_snapshot_name
    )
    assert duplicate


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_create_file_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
        mock_files = json.load(json_file)
    with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
        mock_permissions = json.load(json_file)
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_DropboxSnapshotDatabase.create_file_snapshot(
        mock_snapshot_name, mock_files, mock_permissions
    )


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_file_snapshot_names():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    file_snapshot_names = mock_DropboxSnapshotDatabase.get_file_snapshot_names()
    assert file_snapshot_names == DataBaseResult.file_snapshot_names_result


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_file_with_no_folder_with_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    files = mock_DropboxSnapshotDatabase.get_file_under_folder(mock_snapshot_name, 0, 2)
    file_ids = [f["id"] for f in files]
    assert len(files) <= 2
    assert file_ids == ["id:FILE_ID1", "id:FILE_ID2"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_file_with_no_folder_without_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    files = mock_DropboxSnapshotDatabase.get_file_under_folder(mock_snapshot_name)
    file_ids = [f["id"] for f in files]
    assert file_ids == [
        "id:FILE_ID1",
        "id:FILE_ID2",
        "id:FILE_ID4",
        "id:FILE_ID5",
        "id:FILE_ID6",
        "id:FILE_ID8",
        "id:FILE_ID13",
        "id:FILE_ID14",
    ]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_file_under_certain_folder_with_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_path = "/WeByte"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    files = mock_DropboxSnapshotDatabase.get_file_under_folder(
        mock_snapshot_name, 0, 1, path=mock_path
    )
    file_ids = [f["id"] for f in files]
    assert len(files) <= 1
    assert file_ids == ["id:FILE_ID9"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_file_under_certain_folder_without_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_path = "/WeByte"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    files = mock_DropboxSnapshotDatabase.get_file_under_folder(
        mock_snapshot_name, path=mock_path
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["id:FILE_ID9", "id:FILE_ID15"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_edit_file_snapshot_name():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_changed_snapshot_name = "CHANGE_FILE_SNAPSHOT1"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_DropboxSnapshotDatabase.edit_file_snapshot_name(
        mock_snapshot_name, mock_changed_snapshot_name
    )


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_delete_file_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_DropboxSnapshotDatabase.delete_file_snapshot(mock_snapshot_name)


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_update_path_and_permissions():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "id:FILE_ID15"
    mock_parent_permissions = []
    mock_parent_path = "/WeByte"
    with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
        data = json.load(json_file)
        for permission in data:
            if permission["file_id"] == mock_file_id:
                mock_parent_permissions.append(permission)
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_DropboxSnapshotDatabase.update_permissions(
        mock_snapshot_name, mock_parent_path, mock_parent_permissions, mock_file_id
    )


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_file_name():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "id:FILE_ID1"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    file_name = mock_DropboxSnapshotDatabase.get_file_name(
        mock_snapshot_name, mock_file_id
    )
    assert file_name == "FOLDER_1"


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_all_permission_of_file():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "id:FILE_ID1"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    permissions = mock_DropboxSnapshotDatabase.get_all_permission_of_file(
        mock_snapshot_name, mock_file_id
    )
    permission_ids = [p["id"] for p in permissions]
    assert permission_ids == ["dbid:PERMISSIONID29"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_all_files_of_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
        all_files_of_snapshot_result = json.load(json_file)
    files = mock_DropboxSnapshotDatabase.get_all_files_of_snapshot(mock_snapshot_name)
    assert all_files_of_snapshot_result == files


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_path_of_file():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "id:FILE_ID12"
    path_result = "/CSE 416"
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    path = mock_DropboxSnapshotDatabase.get_path_of_file(
        mock_snapshot_name, mock_file_id
    )
    assert path_result == path


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_update_inherited_from():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "id:FILE_ID15"
    mock_parent_permissions = []
    mock_parent_path = "/WeByte"
    with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
        data = json.load(json_file)
        for permission in data:
            if permission["file_id"] == mock_file_id:
                mock_parent_permissions.append(permission)
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_DropboxSnapshotDatabase.update_inherited_from_permissions(
        mock_snapshot_name, mock_parent_permissions, mock_parent_path, mock_file_id
    )


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_all_members_from_permissions():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"

    all_members = mock_DropboxSnapshotDatabase.get_all_members_from_permissions(
        mock_snapshot_name
    )
    assert DataBaseResult.all_members_from_permissions_result == all_members


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_files_with_path_regex():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_path = "/WeByte"
    files = mock_DropboxSnapshotDatabase.get_files_with_path_regex(
        mock_snapshot_name, mock_path
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["id:FILE_ID9", "id:FILE_ID10", "id:FILE_ID15"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_files_that_match_file_name_regex():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_name = "Get Started with Dropbox Paper"
    files = mock_DropboxSnapshotDatabase.get_files_that_match_file_name_regex(
        mock_snapshot_name, mock_file_name
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["id:FILE_ID4"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_file_id_of_name():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_name = "FOLDER_1"
    file_id = mock_DropboxSnapshotDatabase.get_file_id_of_name(
        mock_snapshot_name, mock_file_name
    )
    assert file_id == "id:FILE_ID1"


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_files_with_certain_role():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_role_name = "writer"
    mock_email = "yooha.bae@stonybrook.edu"
    files = mock_DropboxSnapshotDatabase.get_files_with_certain_role(
        mock_snapshot_name, mock_role_name, mock_email
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["id:FILE_ID11", "id:FILE_ID12", "id:FILE_ID14"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_folders_with_regex():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_name = "folder"
    folders = mock_DropboxSnapshotDatabase.get_folders_with_regex(
        mock_snapshot_name, mock_folder_name
    )
    folder_ids = [f["id"] for f in folders]
    assert folder_ids == ["id:FILE_ID15"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_directly_shared_permissions_file_ids():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yooha.bae@stonybrook.edu"
    file_ids = mock_DropboxSnapshotDatabase.get_directly_shared_permissions_file_ids(
        mock_snapshot_name, mock_email
    )
    assert file_ids == ["id:FILE_ID14"]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_files_of_file_ids():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_ids = ["id:FILE_ID1", "id:FILE_ID2"]
    files = mock_DropboxSnapshotDatabase.get_files_of_file_ids(
        mock_snapshot_name, mock_file_ids
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == mock_file_ids


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_file_ids_shared_with_users_from_domain():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_domain = "@stonybrook.edu"
    file_ids = mock_DropboxSnapshotDatabase.get_file_ids_shared_with_users_from_domain(
        mock_snapshot_name, mock_domain
    )
    unique_file_ids = [*set(file_ids)]
    unique_file_ids.sort()
    assert unique_file_ids == [
        "id:FILE_ID10",
        "id:FILE_ID11",
        "id:FILE_ID12",
        "id:FILE_ID13",
        "id:FILE_ID14",
        "id:FILE_ID15",
        "id:FILE_ID5",
        "id:FILE_ID7",
        "id:FILE_ID9",
    ]


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_not_shared_files():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    files = mock_DropboxSnapshotDatabase.get_not_shared_files(mock_snapshot_name)
    file_ids = [f["id"] for f in files]
    assert file_ids == []


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_create_access_control_requirement():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_access_control = {
        "name": "ACR#1",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": False,
    }
    mock_access_control = AccessControlBody(**mock_access_control)
    mock_DropboxSnapshotDatabase.create_access_control_requirement(mock_access_control)


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_access_control_requirements():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    access_control_requirements = (
        mock_DropboxSnapshotDatabase.get_access_control_requirements()
    )
    assert access_control_requirements == DataBaseResult.all_access_control_requirements


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_duplicate_check_access_control_requirements():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_access_control = {
        "name": "ACR#2",
        "query": "drive:WeByte",
        "AR": [],
        "AW": ["yooha.bae@stonybrook.edu"],
        "DR": [],
        "DW": ["yoolbi.lee@stonybrook.edu"],
        "Grp": False,
    }
    mock_access_control = AccessControlBody(**mock_access_control)
    access_control_requirements = (
        mock_DropboxSnapshotDatabase.check_duplicate_access_control_requirement(
            mock_access_control
        )
    )
    assert access_control_requirements


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_not_duplicate_check_access_control_requirements():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_access_control = {
        "name": "ACR#5",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["haeunpark@cs.stonybrook.edu"],
        "DW": [],
        "Grp": False,
    }
    mock_access_control = AccessControlBody(**mock_access_control)
    access_control_requirements = (
        mock_DropboxSnapshotDatabase.check_duplicate_access_control_requirement(
            mock_access_control
        )
    )
    assert not access_control_requirements


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_get_access_control_requirement():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_acr_name = "ACR#2"
    access_control_requirement = (
        mock_DropboxSnapshotDatabase.get_access_control_requirement(mock_acr_name)
    )
    assert access_control_requirement["name"] == "ACR#2"


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_invalid_get_access_control_requirement():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_acr_name = "ACR#10"
    access_control_requirement = (
        mock_DropboxSnapshotDatabase.get_access_control_requirement(mock_acr_name)
    )
    assert not access_control_requirement


@mock.patch.object(DropboxSnapshotDatabase, "__init__", new_init)
def test_delete_access_control_requirement():
    mock_DropboxSnapshotDatabase = DropboxSnapshotDatabase(mock_user_id)
    mock_acr_name = "ACR#1"
    mock_DropboxSnapshotDatabase.delete_access_control_requirement(mock_acr_name)
