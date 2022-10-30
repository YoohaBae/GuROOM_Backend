import mock
import os
import json
from app.micro_apps.auth.services.google.google_auth import GoogleAuth
from .mock.mock_requests import MockRequests

absolute_path_to_data = "./app/micro_apps/auth/tests/data"

with open(absolute_path_to_data + "/environment_variables.json") as json_file:
    environment_variables = json.load(json_file)


@mock.patch.dict(os.environ, environment_variables)
def test_get_authorization_url():
    mock_google_auth = GoogleAuth()
    url = mock_google_auth.get_authorization_url()
    assert url


@mock.patch.dict(os.environ, environment_variables)
@mock.patch("requests.post", side_effect=MockRequests.mocked_requests_valid_get_token)
def test_valid_get_token(post):
    mock_code = "CODE"
    mock_google_auth = GoogleAuth()
    retrieved = mock_google_auth.get_token(mock_code)
    assert retrieved


@mock.patch("requests.post", side_effect=MockRequests.mocked_requests_invalid_get_token)
def test_invalid_get_token(post):
    mock_code = "CODE"
    mock_google_auth = GoogleAuth()
    retrieved = mock_google_auth.get_token(mock_code)
    assert not retrieved


@mock.patch(
    "requests.post", side_effect=MockRequests.mocked_requests_valid_revoke_token
)
def test_valid_revoke_token(post):
    mock_token = "ACCESS_TOKEN"
    mock_google_auth = GoogleAuth()
    revoked = mock_google_auth.revoke_token(mock_token)
    assert revoked


@mock.patch(
    "requests.post", side_effect=MockRequests.mocked_requests_invalid_revoke_token
)
def test_invalid_revoke_token(post):
    mock_token = "INVALID_ACCESS_TOKEN"
    mock_google_auth = GoogleAuth()
    revoked = mock_google_auth.revoke_token(mock_token)
    assert not revoked


@mock.patch(
    "requests.post", side_effect=MockRequests.mocked_requests_valid_refresh_token
)
def test_valid_refresh_token(post):
    mock_token = "ACCESS_TOKEN"
    mock_google_auth = GoogleAuth()
    refreshed = mock_google_auth.refresh_token(mock_token)
    assert refreshed


@mock.patch(
    "requests.post", side_effect=MockRequests.mocked_requests_invalid_refresh_token
)
def test_invalid_refresh_token(post):
    mock_token = "INVALID_ACCESS_TOKEN"
    mock_google_auth = GoogleAuth()
    refreshed = mock_google_auth.refresh_token(mock_token)
    assert not refreshed


@mock.patch(
    "requests.get", side_effect=MockRequests.mocked_requests_valid_google_get_user
)
def test_valid_get_user(get):
    mock_token = "ACCESS_TOKEN"
    mock_google_auth = GoogleAuth()
    user = mock_google_auth.get_user(mock_token)
    assert user


@mock.patch("requests.get", side_effect=MockRequests.mocked_requests_invalid_get_user)
def test_invalid_get_user(get):
    mock_token = "INVALID_ACCESS_TOKEN"
    mock_google_auth = GoogleAuth()
    user = mock_google_auth.get_user(mock_token)
    assert not user
