import mock
from app.micro_apps.auth.services import service
from .mock.mock_google_auth import MockGoogleAuth
from .mock.mock_database import MockDataBase


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(
    service.GoogleAuth, "get_authorization_url", MockGoogleAuth.get_authorization_url
)
def test_valid_get_google_auth_url():
    url = service.get_google_auth_url()
    assert url


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "get_authorization_url", side_effect=Exception)
def test_invalid_get_google_auth_url(google_auth_exception):
    url = service.get_google_auth_url()
    assert url is None


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "get_token", MockGoogleAuth.get_token)
def test_valid_get_google_token():
    code = "MOCK_CODE1"
    token = service.get_google_token(code)
    assert token


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "get_token", side_effect=Exception)
def test_invalid_get_google_token(google_auth_exception):
    code = "MOCK_CODE1"
    token = service.get_google_token(code)
    assert token is None


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "get_user", MockGoogleAuth.get_user)
def test_valid_get_google_user():
    access_token = "MOCK_ACCESS_TOKEN1"
    user = service.get_google_user(access_token)
    assert user


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "get_user", side_effect=Exception)
def test_invalid_get_google_user(google_auth_exception):
    access_token = "MOCK_ACCESS_TOKEN1"
    user = service.get_google_user(access_token)
    assert user is None


@mock.patch.object(service.DataBase, "__init__", MockDataBase.__init__)
@mock.patch.object(
    service.DataBase, "check_user_exists", MockDataBase.check_user_exists_when_exists
)
@mock.patch.object(service.DataBase, "save_user", MockDataBase.save_user)
def test_valid_check_user_existence_when_exists():
    email = "MOCK_EMAIL1"
    exists = service.check_user_existence(email)
    assert exists


@mock.patch.object(service.DataBase, "__init__", MockDataBase.__init__)
@mock.patch.object(
    service.DataBase,
    "check_user_exists",
    MockDataBase.check_user_exists_when_not_exists,
)
@mock.patch.object(service.DataBase, "save_user", MockDataBase.save_user)
def test_valid_check_user_existence_when_not_exists():
    email = "MOCK_EMAIL1"
    exists = service.check_user_existence(email)
    assert not exists


@mock.patch.object(service.DataBase, "__init__", MockDataBase.__init__)
@mock.patch.object(service.DataBase, "check_user_exists", side_effect=Exception)
def test_invalid_check_user_existence(mock_db_exception):
    email = "MOCK_EMAIL1"
    exists = service.check_user_existence(email)
    assert exists is None


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "refresh_token", MockGoogleAuth.refresh_token)
def test_valid_refresh_google_access_token():
    refresh_token = "MOCK_REFRESH_TOKEN1"
    new_token = service.refresh_google_access_token(refresh_token)
    assert new_token


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "refresh_token", side_effect=Exception)
def test_invalid_refresh_google_access_token(google_auth_exception):
    refresh_token = "MOCK_REFRESH_TOKEN1"
    new_token = service.refresh_google_access_token(refresh_token)
    assert new_token is None


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "revoke_token", MockGoogleAuth.revoke_token)
def test_valid_revoke_google_token():
    access_token = "MOCK_ACCESS_TOKEN1"
    revoked = service.revoke_google_token(access_token)
    assert revoked


@mock.patch.object(service.GoogleAuth, "__init__", MockGoogleAuth.__init__)
@mock.patch.object(service.GoogleAuth, "revoke_token", side_effect=Exception)
def test_invalid_revoke_google_token(google_auth_exception):
    access_token = "MOCK_ACCESS_TOKEN1"
    revoked = service.revoke_google_token(access_token)
    assert not revoked
