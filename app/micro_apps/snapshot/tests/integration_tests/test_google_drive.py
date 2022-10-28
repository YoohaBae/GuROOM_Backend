import mock
import os
import json
from app.micro_apps.auth.services.google.google_auth import GoogleAuth
from app.micro_apps.snapshot.services.google_drive import GoogleDrive

absolute_path_to_auth_data = "./app/micro_apps/auth/tests/data"

with open(absolute_path_to_auth_data + "/environment_variables.json") as json_file:
    environment_variables = json.load(json_file)


@mock.patch.dict(os.environ, environment_variables)
def test_valid_get_root_file_id():
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
    mock_google_auth = GoogleAuth()
    access_token = mock_google_auth.refresh_token(refresh_token)["access_token"]
    mock_google_drive = GoogleDrive()
    root_file_id = mock_google_drive.get_root_file_id(access_token)
    assert root_file_id


def test_invalid_get_root_file_id():
    access_token = "invalid token"
    mock_google_drive = GoogleDrive()
    root_file_id = mock_google_drive.get_root_file_id(access_token)
    assert not root_file_id


@mock.patch.dict(os.environ, environment_variables)
def test_valid_get_files():
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
    mock_google_auth = GoogleAuth()
    access_token = mock_google_auth.refresh_token(refresh_token)["access_token"]
    mock_google_drive = GoogleDrive()
    files, next_page_token = mock_google_drive.get_files(access_token)
    assert files
    if next_page_token:
        next_files, next_page_token = mock_google_drive.get_files(
            access_token, next_page_token
        )
        assert next_files


def test_invalid_get_files():
    access_token = "invalid token"
    mock_google_drive = GoogleDrive()
    files, next_page_token = mock_google_drive.get_files(access_token)
    assert not files
    assert not next_page_token


@mock.patch.dict(os.environ, environment_variables)
def test_valid_get_shared_drives():
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
    mock_google_auth = GoogleAuth()
    access_token = mock_google_auth.refresh_token(refresh_token)["access_token"]
    mock_google_drive = GoogleDrive()
    shared_drives, next_page_token = mock_google_drive.get_shared_drives(access_token)
    assert shared_drives
    if next_page_token:
        next_shared_drives, next_page_token = mock_google_drive.get_shared_drives(
            access_token, next_page_token
        )
        assert next_shared_drives


def test_invalid_get_shared_drives():
    access_token = "invalid token"
    mock_google_drive = GoogleDrive()
    shared_drives, next_page_token = mock_google_drive.get_files(access_token)
    assert not shared_drives
    assert not next_page_token


def test_invalid_get_permission_detail_of_shared_drive_file():
    access_token = "invalid token"
    mock_file_id = "FILEID1"
    mock_permission_id = "PERMISSIONID1"
    mock_google_drive = GoogleDrive()
    permission_detail = mock_google_drive.get_permission_detail_of_shared_drive_file(
        access_token, mock_file_id, mock_permission_id
    )
    assert not permission_detail
