import mock
import os
import json
from app.micro_apps.snapshot.services.dropbox.dropbox_drive import DropboxDrive
from .mock.mock_dropbox_requests import MockRequests

absolute_path_to_auth_data = "./app/micro_apps/auth/tests/data"

with open(absolute_path_to_auth_data + "/environment_variables.json") as json_file:
    environment_variables = json.load(json_file)


@mock.patch.dict(os.environ, environment_variables)
@mock.patch("requests.post", side_effect=MockRequests.mocked_requests_valid_get_files)
def test_valid_get_files(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_dropbox_drive = DropboxDrive()
    files, folders, next_page_token = mock_dropbox_drive.get_files(mock_access_token)
    assert files is not None
    assert folders is not None
    assert next_page_token is None


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.post", side_effect=MockRequests.mocked_requests_valid_get_files_next_page
)
def test_valid_get_files_next_page(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_next_page_token = "NEXT_PAGE_TOKEN"
    mock_dropbox_drive = DropboxDrive()
    files, folders, next_page_token = mock_dropbox_drive.get_files(
        mock_access_token, mock_next_page_token
    )
    assert files is not None
    assert folders is not None
    assert next_page_token is None


@mock.patch("requests.post", side_effect=MockRequests.mocked_requests_invalid_get_files)
def test_invalid_get_files(get):
    access_token = "invalid token"
    mock_dropbox_drive = DropboxDrive()
    files, folders, next_page_token = mock_dropbox_drive.get_files(access_token)
    assert files is None
    assert folders is None
    assert next_page_token is None


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.post",
    side_effect=MockRequests.mocked_requests_valid_get_permissions_of_file,
)
def test_valid_get_permissions_of_files(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_file_ids = ["id:FILE_ID1"]
    mock_dropbox_drive = DropboxDrive()
    files_permissions = mock_dropbox_drive.get_permissions_of_files(
        mock_access_token, mock_file_ids
    )
    assert files_permissions is not None


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.post",
    side_effect=MockRequests.mocked_requests_invalid_get_permissions_of_file,
)
def test_invalid_get_permissions_of_files(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_file_ids = ["id:FILE_ID1"]
    mock_dropbox_drive = DropboxDrive()
    files_permissions = mock_dropbox_drive.get_permissions_of_files(
        mock_access_token, mock_file_ids
    )
    assert files_permissions is None


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.post",
    side_effect=MockRequests.mocked_requests_invalid_role_get_permissions_of_file,
)
def test_invalid_role_get_permissions_of_files(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_file_ids = ["id:FILE_ID1"]
    mock_dropbox_drive = DropboxDrive()
    files_permissions = mock_dropbox_drive.get_permissions_of_files(
        mock_access_token, mock_file_ids
    )
    assert files_permissions is None


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.post",
    side_effect=MockRequests.mocked_requests_valid_get_permissions_of_shared_folder,
)
def test_valid_get_permissions_of_shared_folders(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_folder_ids = ["SHARED_FOLDER_ID1"]
    mock_dropbox_drive = DropboxDrive()
    files_permissions = mock_dropbox_drive.get_permissions_of_shared_folders(
        mock_access_token, mock_folder_ids
    )
    assert files_permissions is not None


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.post",
    side_effect=MockRequests.mocked_requests_invalid_get_permissions_of_shared_folder,
)
def test_invalid_get_permissions_of_shared_folders(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_folder_ids = ["SHARED_FOLDER_ID1"]
    mock_dropbox_drive = DropboxDrive()
    files_permissions = mock_dropbox_drive.get_permissions_of_shared_folders(
        mock_access_token, mock_folder_ids
    )
    assert files_permissions is None


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.post",
    side_effect=MockRequests.mocked_requests_invalid_role_get_permissions_of_shared_folders,
)
def test_invalid_role_get_permissions_of_shared_folders(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_folder_ids = ["SHARED_FOLDER_ID1"]
    mock_dropbox_drive = DropboxDrive()
    files_permissions = mock_dropbox_drive.get_permissions_of_shared_folders(
        mock_access_token, mock_folder_ids
    )
    assert files_permissions is None
