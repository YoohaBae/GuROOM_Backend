import mock
import os
import json
from app.micro_apps.auth.services.google_auth import GoogleAuth

absolute_path_to_data = "./app/micro_apps/auth/tests/data"

with open(absolute_path_to_data + "/environment_variables.json") as json_file:
    environment_variables = json.load(json_file)


@mock.patch.dict(os.environ, environment_variables)
def test_get_authorization_url():
    mock_google_auth = GoogleAuth()
    url = mock_google_auth.get_authorization_url()
    assert url


@mock.patch.dict(os.environ, environment_variables)
def test_invalid_get_token():
    mock_code = "invalid code"
    mock_google_auth = GoogleAuth()
    retrieved = mock_google_auth.get_token(mock_code)
    assert not retrieved


@mock.patch.dict(os.environ, environment_variables)
def test_invalid_revoke_token():
    mock_token = "invalid token"
    mock_google_auth = GoogleAuth()
    revoked = mock_google_auth.revoke_token(mock_token)
    assert not revoked


@mock.patch.dict(os.environ, environment_variables)
def test_invalid_refresh_token():
    mock_token = "invalid token"
    mock_google_auth = GoogleAuth()
    refreshed = mock_google_auth.refresh_token(mock_token)
    assert not refreshed


@mock.patch.dict(os.environ, environment_variables)
def test_invalid_get_user():
    mock_token = "invalid token"
    mock_google_auth = GoogleAuth()
    retrieved = mock_google_auth.get_user(mock_token)
    assert not retrieved


@mock.patch.dict(os.environ, environment_variables)
def test_valid_get_user():
    refresh_token = os.getenv("REFRESH_TOKEN")
    mock_google_auth = GoogleAuth()
    access_token = mock_google_auth.refresh_token(refresh_token)["access_token"]
    retrieved = mock_google_auth.get_user(access_token)
    assert retrieved
