import mock
import os
import json
from app.micro_apps.snapshot.services.google_drive import GoogleDrive
from .mock.mock_requests import MockRequests

absolute_path_to_auth_data = "./app/micro_apps/auth/tests/data"

with open(absolute_path_to_auth_data + "/environment_variables.json") as json_file:
    environment_variables = json.load(json_file)


@mock.patch.dict(os.environ, environment_variables)
@mock.patch("requests.get", side_effect=MockRequests.mocked_requests_valid_get_root_id)
def test_valid_get_root_file_id(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_google_drive = GoogleDrive()
    root_file_id = mock_google_drive.get_root_file_id(mock_access_token)
    assert root_file_id


@mock.patch(
    "requests.get", side_effect=MockRequests.mocked_requests_invalid_get_root_id
)
def test_invalid_get_root_file_id(get):
    mock_access_token = "INVALID_TOKEN"
    mock_google_drive = GoogleDrive()
    root_file_id = mock_google_drive.get_root_file_id(mock_access_token)
    assert not root_file_id


@mock.patch.dict(os.environ, environment_variables)
@mock.patch("requests.get", side_effect=MockRequests.mocked_requests_valid_get_files)
def test_valid_get_files(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_google_drive = GoogleDrive()
    files, next_page_token = mock_google_drive.get_files(mock_access_token)
    assert files
    assert not next_page_token


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.get", side_effect=MockRequests.mocked_requests_valid_get_files_next_page
)
def test_valid_get_files_next_page(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_next_page_token = "NEXT_PAGE_TOKEN"
    mock_google_drive = GoogleDrive()
    files, next_page_token = mock_google_drive.get_files(
        mock_access_token, mock_next_page_token
    )
    assert files
    assert next_page_token


@mock.patch("requests.get", side_effect=MockRequests.mocked_requests_invalid_get_files)
def test_invalid_get_files(get):
    access_token = "invalid token"
    mock_google_drive = GoogleDrive()
    files, next_page_token = mock_google_drive.get_files(access_token)
    assert not files
    assert not next_page_token


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.get", side_effect=MockRequests.mocked_requests_valid_get_shared_drives
)
def test_valid_get_shared_drives(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_google_drive = GoogleDrive()
    shared_drives, next_page_token = mock_google_drive.get_shared_drives(
        mock_access_token
    )
    assert shared_drives
    assert not next_page_token


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.get",
    side_effect=MockRequests.mocked_requests_valid_get_shared_drives_next_page,
)
def test_valid_get_shared_drives_next_page(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_next_page_token = "NEXT_PAGE_TOKEN"
    mock_google_drive = GoogleDrive()
    shared_drives, next_page_token = mock_google_drive.get_shared_drives(
        mock_access_token, mock_next_page_token
    )
    assert shared_drives
    assert next_page_token


@mock.patch(
    "requests.get", side_effect=MockRequests.mocked_requests_invalid_get_shared_drives
)
def test_invalid_get_shared_drives(get):
    access_token = "invalid token"
    mock_google_drive = GoogleDrive()
    shared_drives, next_page_token = mock_google_drive.get_shared_drives(access_token)
    assert not shared_drives
    assert not next_page_token


@mock.patch.dict(os.environ, environment_variables)
@mock.patch(
    "requests.get",
    side_effect=MockRequests.mocked_requests_valid_get_permission_detail_of_shared_drive_file,
)
def test_valid_get_permission_detail_of_shared_drive_file(get):
    mock_access_token = "ACCESS_TOKEN"
    mock_file_id = "FILEID1"
    mock_permission_id = "PERMISSIONID1"
    mock_google_drive = GoogleDrive()
    permission_detail = mock_google_drive.get_permission_detail_of_shared_drive_file(
        mock_access_token, mock_file_id, mock_permission_id
    )
    assert permission_detail


@mock.patch(
    "requests.get",
    side_effect=MockRequests.mocked_requests_invalid_get_permission_detail_of_shared_drive_file,
)
def test_invalid_get_permission_detail_of_shared_drive_file(get):
    mock_access_token = "INVALID_TOKEN"
    mock_file_id = "FILEID1"
    mock_permission_id = "PERMISSIONID1"
    mock_google_drive = GoogleDrive()
    permission_detail = mock_google_drive.get_permission_detail_of_shared_drive_file(
        mock_access_token, mock_file_id, mock_permission_id
    )
    assert not permission_detail
