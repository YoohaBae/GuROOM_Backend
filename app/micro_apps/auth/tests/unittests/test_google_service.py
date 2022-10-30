from app.micro_apps.auth.services.google.service import (
    GoogleAuthService,
    GoogleAuth,
    GoogleAuthDatabase,
)
import mock
from .mock.mock_auth import MockAuth
from .mock.mock_database import MockGoogleAuthDatabase

service = GoogleAuthService()


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "get_authorization_url", MockAuth.get_authorization_url)
def test_valid_get_google_auth_url():
    url = service.get_auth_url()
    assert url


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "get_authorization_url", side_effect=Exception)
def test_invalid_get_google_auth_url(google_auth_exception):
    url = service.get_auth_url()
    assert url is None


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "get_token", MockAuth.get_token)
def test_valid_get_google_token():
    code = "MOCK_CODE1"
    token = service.get_token(code)
    assert token


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "get_token", side_effect=Exception)
def test_invalid_get_google_token(google_auth_exception):
    code = "MOCK_CODE1"
    token = service.get_token(code)
    assert token is None


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "get_user", MockAuth.get_user)
def test_valid_get_google_user():
    access_token = "MOCK_ACCESS_TOKEN1"
    user = service.get_user(access_token)
    assert user


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "get_user", side_effect=Exception)
def test_invalid_get_google_user(google_auth_exception):
    access_token = "MOCK_ACCESS_TOKEN1"
    user = service.get_user(access_token)
    assert user is None


@mock.patch.object(GoogleAuthDatabase, "__init__", MockGoogleAuthDatabase.__init__)
@mock.patch.object(
    GoogleAuthDatabase,
    "check_user_exists",
    MockGoogleAuthDatabase.check_user_exists_when_exists,
)
@mock.patch.object(GoogleAuthDatabase, "save_user", MockGoogleAuthDatabase.save_user)
def test_valid_check_user_existence_when_exists():
    email = "MOCK_EMAIL1"
    exists = service.check_user_existence(email)
    assert exists


@mock.patch.object(GoogleAuthDatabase, "__init__", MockGoogleAuthDatabase.__init__)
@mock.patch.object(
    GoogleAuthDatabase,
    "check_user_exists",
    MockGoogleAuthDatabase.check_user_exists_when_not_exists,
)
@mock.patch.object(GoogleAuthDatabase, "save_user", MockGoogleAuthDatabase.save_user)
def test_valid_check_user_existence_when_not_exists():
    email = "MOCK_EMAIL1"
    exists = service.check_user_existence(email)
    assert not exists


@mock.patch.object(GoogleAuthDatabase, "__init__", MockGoogleAuthDatabase.__init__)
@mock.patch.object(GoogleAuthDatabase, "check_user_exists", side_effect=Exception)
def test_invalid_check_user_existence(mock_db_exception):
    email = "MOCK_EMAIL1"
    exists = service.check_user_existence(email)
    assert exists is None


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "refresh_token", MockAuth.refresh_token)
def test_valid_refresh_google_access_token():
    refresh_token = "MOCK_REFRESH_TOKEN1"
    new_token = service.refresh_access_token(refresh_token)
    assert new_token


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "refresh_token", side_effect=Exception)
def test_invalid_refresh_google_access_token(google_auth_exception):
    refresh_token = "MOCK_REFRESH_TOKEN1"
    new_token = service.refresh_access_token(refresh_token)
    assert new_token is None


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "revoke_token", MockAuth.revoke_token)
def test_valid_revoke_google_token():
    access_token = "MOCK_ACCESS_TOKEN1"
    revoked = service.revoke_token(access_token)
    assert revoked


@mock.patch.object(GoogleAuth, "__init__", MockAuth.__init__)
@mock.patch.object(GoogleAuth, "revoke_token", side_effect=Exception)
def test_invalid_revoke_google_token(google_auth_exception):
    access_token = "MOCK_ACCESS_TOKEN1"
    revoked = service.revoke_token(access_token)
    assert not revoked
