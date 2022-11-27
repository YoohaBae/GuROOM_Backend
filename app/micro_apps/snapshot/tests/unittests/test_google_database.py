import mock
import json
from datetime import datetime
from app.micro_apps.snapshot.endpoints.models.access_control import AccessControlBody
from app.micro_apps.snapshot.services.google.analysis import GoogleSnapshotDatabase
from app.micro_apps.snapshot.tests.unittests.mock.mock_google_mongodb import MockMongoDB
from app.micro_apps.snapshot.tests.data.google.database_result import DataBaseResult

mock_user_id = "MOCK_USER_ID1"
absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/google"


def new_init(self, user_id):
    db_name = None
    url = None
    self._db = MockMongoDB(url, db_name)
    self.user_id = user_id


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_create_file_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    with open(absolute_path_to_data + "/snapshot1_raw_files.json") as json_file:
        mock_data = json.load(json_file)
    mock_root_id = "ROOTID1"
    mock_shared_drives = []
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_GoogleSnapshotDatabase.create_file_snapshot(
        mock_snapshot_name, mock_data, mock_root_id, mock_shared_drives
    )


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_root_id():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    root_id = mock_GoogleSnapshotDatabase.get_root_id(mock_snapshot_name)
    assert root_id == "ROOTID1"


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_file_snapshot_names():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    file_snapshot_names = mock_GoogleSnapshotDatabase.get_file_snapshot_names()
    assert file_snapshot_names == DataBaseResult.file_snapshot_names_result


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_file_with_no_folder_with_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    files = mock_GoogleSnapshotDatabase.get_file_under_folder(mock_snapshot_name, 0, 2)
    file_ids = [f["id"] for f in files]
    assert len(files) <= 2
    assert file_ids == ["FILEID1", "FILEID15"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_file_with_no_folder_without_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    files = mock_GoogleSnapshotDatabase.get_file_under_folder(mock_snapshot_name)
    file_ids = [f["id"] for f in files]
    assert file_ids == [
        "FILEID1",
        "FILEID15",
        "FILEID16",
        "FILEID17",
        "FILEID18",
        "FILEID3",
    ]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_file_under_certain_folder_with_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_id = "FILEID1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    files = mock_GoogleSnapshotDatabase.get_file_under_folder(
        mock_snapshot_name, 0, 2, mock_folder_id
    )
    file_ids = [f["id"] for f in files]
    assert len(files) <= 2
    assert file_ids == ["FILEID4"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_file_under_certain_folder_without_offset():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_id = "FILEID1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    files = mock_GoogleSnapshotDatabase.get_file_under_folder(
        mock_snapshot_name, folder_id=mock_folder_id
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID4"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_edit_file_snapshot_name():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_changed_snapshot_name = "CHANGE_FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_GoogleSnapshotDatabase.edit_file_snapshot_name(
        mock_snapshot_name, mock_changed_snapshot_name
    )


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_delete_file_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_GoogleSnapshotDatabase.delete_file_snapshot(mock_snapshot_name)


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_update_path_and_permissions():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_path = "/MyDrive"
    folder_permission = []
    file_id = "FILEID5"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_GoogleSnapshotDatabase.update_path_and_permissions(
        mock_snapshot_name, mock_folder_path, folder_permission, file_id
    )


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
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
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_GoogleSnapshotDatabase.update_path_and_permissions(
        mock_snapshot_name, mock_folder_path, folder_permission, file_id
    )


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_all_permission_of_file():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    permissions = mock_GoogleSnapshotDatabase.get_all_permission_of_file(
        mock_snapshot_name, mock_file_id
    )
    permission_ids = [p["id"] for p in permissions]
    assert permission_ids == ["PERMISSIONID1", "PERMISSIONID2", "PERMISSIONID3"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_files_with_no_path():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    files = mock_GoogleSnapshotDatabase.get_files_with_no_path(mock_snapshot_name)
    file_ids = [f["id"] for f in files]
    assert file_ids == [
        "FILEID1",
        "FILEID15",
        "FILEID16",
        "FILEID17",
        "FILEID18",
        "FILEID3",
    ]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_all_permission_of_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    with open(absolute_path_to_data + "/snapshot1_permissions.json") as json_file:
        all_permissions_of_snapshot_result = json.load(json_file)
    permissions = mock_GoogleSnapshotDatabase.get_all_permission_of_snapshot(
        mock_snapshot_name
    )
    assert all_permissions_of_snapshot_result == permissions


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_all_files_of_snapshot():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    with open(absolute_path_to_data + "/snapshot1_files.json") as json_file:
        all_files_of_snapshot_result = json.load(json_file)
    files = mock_GoogleSnapshotDatabase.get_all_files_of_snapshot(mock_snapshot_name)
    assert all_files_of_snapshot_result == files


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_parent_id():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID20"
    parent_id_result = "FILEID8"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    parent_id = mock_GoogleSnapshotDatabase.get_parent_id(
        mock_snapshot_name, mock_file_id
    )
    assert parent_id_result == parent_id


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_shared_drives():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    shared_drives_result = [
        {"id": "SHAREDDRIVEID1", "name": "SUNY"},
        {"id": "SHAREDDRIVEID2", "name": "WeByte"},
    ]
    shared_drives = mock_GoogleSnapshotDatabase.get_shared_drives(mock_snapshot_name)
    assert shared_drives_result == shared_drives


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_path_of_file():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID5"
    path_result = "/MyDrive"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    path = mock_GoogleSnapshotDatabase.get_path_of_file(
        mock_snapshot_name, mock_file_id
    )
    assert path_result == path


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_path_of_shared_drives():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "SHAREDDRIVEID1"
    shared_drive_path_result = "/SUNY"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    shared_drive_path = mock_GoogleSnapshotDatabase.get_path_of_file(
        mock_snapshot_name, mock_file_id
    )
    assert shared_drive_path_result == shared_drive_path


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_update_inherited_and_inherited_from():
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_id = "FILEID4"
    mock_permission_id = "PERMISSIONID1"
    mock_inherited = True
    mock_inherited_from = "/Hi_Folder"
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_GoogleSnapshotDatabase.update_inherited_and_inherited_from(
        mock_snapshot_name,
        mock_file_id,
        mock_permission_id,
        mock_inherited,
        mock_inherited_from,
    )


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_create_group_memberships_snapshot():
    mock_group_name = "CSE416"
    mock_group_email = "cse416@cs.stonybrook.edu"
    mock_create_time = datetime.now()
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
        data = json.load(json_file)
        mock_memberships = data[0]["memberships"]
    mock_GoogleSnapshotDatabase.create_group_memberships_snapshot(
        mock_group_name, mock_group_email, mock_create_time, mock_memberships
    )


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_all_group_membership_snapshots():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    with open(absolute_path_to_data + "/group_snapshots.json") as json_file:
        data = json.load(json_file)
        group_membership_snapshots_result = data
    group_membership_snapshots = (
        mock_GoogleSnapshotDatabase.get_all_group_membership_snapshots()
    )
    assert group_membership_snapshots_result == group_membership_snapshots


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_all_members_from_permissions():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"

    all_members = mock_GoogleSnapshotDatabase.get_all_members_from_permissions(
        mock_snapshot_name
    )
    assert DataBaseResult.all_members_from_permissions_result == all_members


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_files_with_path_regex():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_path = "/FOLDER_1"
    files = mock_GoogleSnapshotDatabase.get_files_with_path_regex(
        mock_snapshot_name, mock_path
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID19", "FILEID11", "FILEID12"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_files_that_match_file_name_regex():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_name = "Hi_Folder"
    files = mock_GoogleSnapshotDatabase.get_files_that_match_file_name_regex(
        mock_snapshot_name, mock_file_name
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID1"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_files_with_certain_role():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_role_name = "writer"
    mock_email = "yoobae@cs.stonybrook.edu"
    files = mock_GoogleSnapshotDatabase.get_files_with_certain_role(
        mock_snapshot_name, mock_role_name, mock_email
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID1", "FILEID16", "FILEID17", "FILEID3", "FILEID4"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_group_emails_of_user_email():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_email = "yoobae@cs.stonybrook.edu"
    group_emails = mock_GoogleSnapshotDatabase.get_group_emails_of_user_email(
        mock_email
    )
    assert group_emails == ["cse300@gmail.com"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_files_with_certain_role_including_groups():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_role_name = "writer"
    mock_email = "yoobae@cs.stonybrook.edu"
    files = mock_GoogleSnapshotDatabase.get_files_with_certain_role_including_groups(
        mock_snapshot_name, mock_role_name, mock_email
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == [
        "FILEID1",
        "FILEID16",
        "FILEID17",
        "FILEID3",
        "FILEID4",
        "FILEID5",
    ]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_folders_with_regex():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_folder_name = "Hi_Folder"
    folders = mock_GoogleSnapshotDatabase.get_folders_with_regex(
        mock_snapshot_name, mock_folder_name
    )
    folder_ids = [f["id"] for f in folders]
    assert folder_ids == ["FILEID1"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_directly_shared_permissions_file_ids():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yoobae@cs.stonybrook.edu"
    file_ids = mock_GoogleSnapshotDatabase.get_directly_shared_permissions_file_ids(
        mock_snapshot_name, mock_email
    )
    assert file_ids == [
        "FILEID1",
        "FILEID2",
        "FILEID6",
        "FILEID7",
        "FILEID8",
        "FILEID14",
        "FILEID16",
        "FILEID17",
        "FILEID3",
        "FILEID4",
    ]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_files_with_sharing_user():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_email = "yoollee@cs.stonybrook.edu"
    files = mock_GoogleSnapshotDatabase.get_files_with_sharing_user(
        mock_snapshot_name, mock_email
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID1", "FILEID3"]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_files_of_file_ids():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_file_ids = ["FILEID1", "FILEID2"]
    files = mock_GoogleSnapshotDatabase.get_files_of_file_ids(
        mock_snapshot_name, mock_file_ids
    )
    file_ids = [f["id"] for f in files]
    assert file_ids == mock_file_ids


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_file_ids_shared_with_users_from_domain():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_domain = "@cs.stonybrook.edu"
    file_ids = mock_GoogleSnapshotDatabase.get_file_ids_shared_with_users_from_domain(
        mock_snapshot_name, mock_domain
    )
    unique_file_ids = [*set(file_ids)]
    unique_file_ids.sort()
    assert unique_file_ids == [
        "FILEID1",
        "FILEID14",
        "FILEID16",
        "FILEID17",
        "FILEID2",
        "FILEID3",
        "FILEID4",
        "FILEID6",
        "FILEID7",
        "FILEID8",
    ]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_not_shared_files():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    files = mock_GoogleSnapshotDatabase.get_not_shared_files(mock_snapshot_name)
    file_ids = [f["id"] for f in files]
    assert file_ids == [
        "FILEID2",
        "FILEID6",
        "FILEID7",
        "FILEID8",
        "FILEID14",
        "FILEID19",
        "FILEID20",
        "FILEID9",
        "FILEID10",
        "FILEID11",
        "FILEID12",
    ]


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_file_ids_shared_with_anyone():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_snapshot_name = "FILE_SNAPSHOT1"
    file_ids = mock_GoogleSnapshotDatabase.get_file_ids_shared_with_anyone(
        mock_snapshot_name
    )
    assert file_ids == []


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_create_access_control_requirement():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_access_control = {
        "name": "ACR#1",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": True,
    }
    mock_access_control = AccessControlBody(**mock_access_control)
    mock_GoogleSnapshotDatabase.create_access_control_requirement(mock_access_control)


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_access_control_requirements():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    access_control_requirements = (
        mock_GoogleSnapshotDatabase.get_access_control_requirements()
    )
    assert access_control_requirements == DataBaseResult.all_access_control_requirements


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_duplicate_check_access_control_requirements():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_access_control = {
        "name": "ACR#1",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": ["cse416@cs.stonybrook.edu"],
        "DR": [],
        "DW": ["yoollee@cs.stonybrook.edu"],
        "Grp": True,
    }
    mock_access_control = AccessControlBody(**mock_access_control)
    access_control_requirements = (
        mock_GoogleSnapshotDatabase.check_duplicate_access_control_requirement(
            mock_access_control
        )
    )
    assert access_control_requirements


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_not_duplicate_check_access_control_requirements():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
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
        mock_GoogleSnapshotDatabase.check_duplicate_access_control_requirement(
            mock_access_control
        )
    )
    assert not access_control_requirements


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_get_access_control_requirement():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_acr_name = "ACR#1"
    access_control_requirement = (
        mock_GoogleSnapshotDatabase.get_access_control_requirement(mock_acr_name)
    )
    assert access_control_requirement["name"] == "ACR#1"


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_invalid_get_access_control_requirement():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_acr_name = "ACR#10"
    access_control_requirement = (
        mock_GoogleSnapshotDatabase.get_access_control_requirement(mock_acr_name)
    )
    assert not access_control_requirement


@mock.patch.object(GoogleSnapshotDatabase, "__init__", new_init)
def test_delete_access_control_requirement():
    mock_GoogleSnapshotDatabase = GoogleSnapshotDatabase(mock_user_id)
    mock_acr_name = "ACR#1"
    mock_GoogleSnapshotDatabase.delete_access_control_requirement(mock_acr_name)
