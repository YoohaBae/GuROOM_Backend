import os
import mock
from fastapi.testclient import TestClient
from app.micro_apps.auth.endpoints.v1.google import AuthJWT, service
from app.main import app
from .mock.mock_authjwt import MockAuthJWT
from .mock.mock_service import MockService

client = TestClient(app)


@mock.patch.object(service, "get_google_auth_url", MockService.get_google_auth_url)
def test_valid_create_google_auth():
    response = client.get("/apps/auth/v1/google/authorize")
    assert response.status_code == 200


@mock.patch.object(service, "get_google_auth_url", MockService.get_none)
def test_invalid_create_google_auth():
    response = client.get("/apps/auth/v1/google/authorize")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "create_access_token", MockAuthJWT.create_access_token)
@mock.patch.object(AuthJWT, "create_refresh_token", MockAuthJWT.create_refresh_token)
@mock.patch.object(AuthJWT, "set_access_cookies", MockAuthJWT.set_access_cookies)
@mock.patch.object(AuthJWT, "set_refresh_cookies", MockAuthJWT.set_refresh_cookies)
@mock.patch.object(service, "get_google_token", MockService.get_google_token)
def test_valid_login():
    body = {
        "code": "MOCK_CODE1"
    }
    response = client.post("/apps/auth/v1/google/login", json=body)
    assert response.status_code == 201


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "create_access_token", MockAuthJWT.create_access_token)
@mock.patch.object(AuthJWT, "create_refresh_token", MockAuthJWT.create_refresh_token)
@mock.patch.object(AuthJWT, "set_access_cookies", MockAuthJWT.set_access_cookies)
@mock.patch.object(AuthJWT, "set_refresh_cookies", MockAuthJWT.set_refresh_cookies)
@mock.patch.object(service, "get_google_token", MockService.get_none)
def test_invalid_login():
    body = {
        "code": "MOCK_CODE1"
    }
    response = client.post("/apps/auth/v1/google/login", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(service, "get_google_user", MockService.get_google_user)
@mock.patch.object(service, "check_user_existence", MockService.user_not_exist)
def test_valid_get_first_time_user():
    response = client.get("/apps/auth/v1/google/user")
    assert response.status_code == 201


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(service, "get_google_user", MockService.get_google_user)
@mock.patch.object(service, "check_user_existence", MockService.user_exists)
def test_valid_get_existing_user():
    response = client.get("/apps/auth/v1/google/user")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(service, "get_google_user", MockService.get_google_user)
@mock.patch.object(service, "check_user_existence", MockService.get_none)
def test_invalid_get_user():
    response = client.get("/apps/auth/v1/google/user")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(service, "get_google_user", MockService.get_none)
def test_invalid_get_user_from_google():
    response = client.get("/apps/auth/v1/google/user")
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_refresh_token_required", MockAuthJWT.jwt_refresh_token_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(AuthJWT, "unset_access_cookies", MockAuthJWT.unset_access_cookies)
@mock.patch.object(AuthJWT, "create_access_token", MockAuthJWT.create_access_token)
@mock.patch.object(service, "refresh_google_access_token", MockService.refresh_google_access_token)
def test_valid_refresh_token():
    response = client.post("/apps/auth/v1/google/refresh")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_refresh_token_required", MockAuthJWT.jwt_refresh_token_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(AuthJWT, "unset_access_cookies", MockAuthJWT.unset_access_cookies)
@mock.patch.object(AuthJWT, "create_access_token", MockAuthJWT.create_access_token)
@mock.patch.object(service, "refresh_google_access_token", MockService.get_none)
def test_invalid_refresh_token():
    response = client.post("/apps/auth/v1/google/refresh")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "unset_jwt_cookies", MockAuthJWT.unset_jwt_cookies)
def test_logout():
    response = client.delete("/apps/auth/v1/google/logout")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "unset_jwt_cookies", MockAuthJWT.unset_jwt_cookies)
@mock.patch.object(service, "revoke_google_token", MockService.revoke_google_token)
def test_valid_revoke_token():
    response = client.delete("/apps/auth/v1/google/revoke")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "unset_jwt_cookies", MockAuthJWT.unset_jwt_cookies)
@mock.patch.object(service, "revoke_google_token", MockService.get_none)
def test_invalid_revoke_token():
    response = client.delete("/apps/auth/v1/google/revoke")
    assert response.status_code == 500
