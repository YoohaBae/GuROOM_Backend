import mock
import json
from datetime import datetime
from app.micro_apps.snapshot.services.analysis import DataBase
from app.micro_apps.snapshot.tests.unittests.mock.mock_mongodb import MockMongoDB
from app.micro_apps.snapshot.tests.data.database_result import DataBaseResult

mock_user_id = "MOCK_USER_ID1"
absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"


def new_init(self, user_id):
    db_name = None
    url = None
    self._db = MockMongoDB(url, db_name)
    self.user_id = user_id


@mock.patch.object(DataBase, "__init__", new_init)
def test_create_file_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    with open(absolute_path_to_data + "/snapshot1_raw_files.json") as json_file:
        mock_data = json.load(json_file)
    mock_root_id = "ROOTID1"
    mock_shared_drives = []
    mock_database = DataBase(mock_user_id)
    mock_database.create_file_snapshot(
        mock_snapshot_name, mock_data, mock_root_id, mock_shared_drives
    )


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_root_id():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    root_id = mock_database.get_root_id(mock_snapshot_name)
    assert root_id == "ROOTID1"


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_file_snapshot_names():
    mock_database = DataBase(mock_user_id)
    file_snapshot_names = mock_database.get_file_snapshot_names()
    assert file_snapshot_names == DataBaseResult.file_snapshot_names_result


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_file_with_no_folder_with_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    files = mock_database.get_file_under_folder(mock_snapshot_name, 0, 2)
    assert len(files) <= 2
    assert DataBaseResult.file_with_no_folder_with_offset_result == files


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_file_with_no_folder_without_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    files = mock_database.get_file_under_folder(mock_snapshot_name)
    assert DataBaseResult.file_with_no_folder_without_offset_result == files


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_file_under_certain_folder_with_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_id = "FILEID1"
    mock_database = DataBase(mock_user_id)
    files = mock_database.get_file_under_folder(
        mock_snapshot_name, 0, 2, mock_folder_id
    )
    assert len(files) <= 2
    assert DataBaseResult.file_with_folder_with_offset_result == files


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_file_under_certain_folder_without_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_id = "FILEID1"
    mock_database = DataBase(mock_user_id)
    files = mock_database.get_file_under_folder(
        mock_snapshot_name, folder_id=mock_folder_id
    )
    assert DataBaseResult.file_with_folder_without_offset_result == files


@mock.patch.object(DataBase, "__init__", new_init)
def test_edit_file_snapshot_name():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_changed_snapshot_name = "CHANGE_FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    mock_database.edit_file_snapshot_name(
        mock_snapshot_name, mock_changed_snapshot_name
    )


@mock.patch.object(DataBase, "__init__", new_init)
def test_delete_file_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    mock_database.delete_file_snapshot(mock_snapshot_name)


@mock.patch.object(DataBase, "__init__", new_init)
def test_update_path_and_permissions():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_path = "/MyDrive"
    folder_permission = []
    file_id = "FILEID5"
    mock_database = DataBase(mock_user_id)
    mock_database.update_path_and_permissions(
        mock_snapshot_name, mock_folder_path, folder_permission, file_id
    )


@mock.patch.object(DataBase, "__init__", new_init)
def test_update_permissions_to_inherit_direct():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_path = "/MyDrive/FILEID6"
    file_id = "FILEID19"
    folder_permission = []
    with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
        data = json.load(json_file)
        for permission in data:
            if permission["file_id"] == "FILEID6":
                folder_permission.append(permission)
    mock_database = DataBase(mock_user_id)
    mock_database.update_path_and_permissions(
        mock_snapshot_name, mock_folder_path, folder_permission, file_id
    )


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_all_permission_of_file():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID1"
    mock_database = DataBase(mock_user_id)
    permissions = mock_database.get_all_permission_of_file(
        mock_snapshot_name, mock_file_id
    )
    assert DataBaseResult.get_all_permission_of_file_result == permissions


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_files_with_no_path():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    files = mock_database.get_files_with_no_path(mock_snapshot_name)
    assert DataBaseResult.files_with_no_path_result == files


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_all_permission_of_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    permissions = mock_database.get_all_permission_of_snapshot(mock_snapshot_name)
    assert DataBaseResult.all_permissions_of_snapshot_result == permissions


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_all_files_of_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    files = mock_database.get_all_files_of_snapshot(mock_snapshot_name)
    assert DataBaseResult.all_files_of_snapshot_result == files


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_parent_id():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID20"
    parent_id_result = "FILEID8"
    mock_database = DataBase(mock_user_id)
    parent_id = mock_database.get_parent_id(mock_snapshot_name, mock_file_id)
    assert parent_id_result == parent_id


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_shared_drives():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_database = DataBase(mock_user_id)
    shared_drives = mock_database.get_shared_drives(mock_snapshot_name)
    assert DataBaseResult.shared_drives_result == shared_drives


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_path_of_file():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID5"
    path_result = "/MyDrive"
    mock_database = DataBase(mock_user_id)
    path = mock_database.get_path_of_file(mock_snapshot_name, mock_file_id)
    assert path_result == path


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_path_of_shared_drives():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "SHAREDDRIVEID1"
    shared_drive_path_result = "/SUNY"
    mock_database = DataBase(mock_user_id)
    shared_drive_path = mock_database.get_path_of_file(mock_snapshot_name, mock_file_id)
    assert shared_drive_path_result == shared_drive_path


@mock.patch.object(DataBase, "__init__", new_init)
def test_update_inherited_and_inherited_from():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID4"
    mock_permission_id = "PERMISSIONID1"
    mock_inherited = True
    mock_inherited_from = "/Hi_Folder"
    mock_database = DataBase(mock_user_id)
    mock_database.update_inherited_and_inherited_from(
        mock_snapshot_name,
        mock_file_id,
        mock_permission_id,
        mock_inherited,
        mock_inherited_from,
    )


@mock.patch.object(DataBase, "__init__", new_init)
def test_create_group_memberships_snapshot():
    mock_group_name = "CSE416"
    mock_group_email = "cse416@cs.stonybrook.edu"
    mock_create_time = datetime.now()
    mock_database = DataBase(mock_user_id)
    with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
        data = json.load(json_file)
        mock_memberships = data[0]["memberships"]
    mock_database.create_group_memberships_snapshot(
        mock_group_name, mock_group_email, mock_create_time, mock_memberships
    )


@mock.patch.object(DataBase, "__init__", new_init)
def test_get_all_group_membership_snapshots():
    mock_database = DataBase(mock_user_id)
    with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
        data = json.load(json_file)
        group_membership_snapshots_result = data
    group_membership_snapshots = mock_database.get_all_group_membership_snapshots()
    print(group_membership_snapshots)
    assert group_membership_snapshots_result == group_membership_snapshots
