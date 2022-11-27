import mock
import pytest
from fastapi.testclient import TestClient
from app.micro_apps.snapshot.endpoints.v1.google import AuthJWT
from ...services.google.service import GoogleSnapshotService
from app.main import app
from .mock.mock_authjwt import MockAuthJWT
from .mock.mock_google_service import MockService

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/google"

client = TestClient(app)


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_root_id_from_api", MockService.get_root_id_from_api
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_all_shared_drives_from_api",
    MockService.get_all_shared_drives_from_api,
)
@mock.patch.object(
    GoogleSnapshotService, "get_all_files_from_api", MockService.get_all_files_from_api
)
@mock.patch.object(
    GoogleSnapshotService, "create_file_snapshot", MockService.create_file_snapshot
)
@mock.patch.object(
    GoogleSnapshotService,
    "perform_inherit_direct_permission_analysis",
    MockService.perform_inherit_direct_permission_analysis,
)
def test_valid_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 201


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(GoogleSnapshotService, "get_root_id_from_api", MockService.get_none)
def test_invalid_root_id_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_root_id_from_api", MockService.get_root_id_from_api
)
@mock.patch.object(
    GoogleSnapshotService, "get_all_shared_drives_from_api", MockService.get_none
)
@mock.patch.object(
    GoogleSnapshotService, "get_all_files_from_api", MockService.get_all_files_from_api
)
@mock.patch.object(
    GoogleSnapshotService, "create_file_snapshot", MockService.create_file_snapshot
)
@mock.patch.object(
    GoogleSnapshotService,
    "perform_inherit_direct_permission_analysis",
    MockService.perform_inherit_direct_permission_analysis,
)
def test_invalid_all_shared_drives_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_root_id_from_api", MockService.get_root_id_from_api
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_all_shared_drives_from_api",
    MockService.get_all_shared_drives_from_api,
)
@mock.patch.object(
    GoogleSnapshotService, "get_all_files_from_api", MockService.get_none
)
@mock.patch.object(
    GoogleSnapshotService, "create_file_snapshot", MockService.create_file_snapshot
)
@mock.patch.object(
    GoogleSnapshotService,
    "perform_inherit_direct_permission_analysis",
    MockService.perform_inherit_direct_permission_analysis,
)
def test_invalid_all_files_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_root_id_from_api", MockService.get_root_id_from_api
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_all_shared_drives_from_api",
    MockService.get_all_shared_drives_from_api,
)
@mock.patch.object(
    GoogleSnapshotService, "get_all_files_from_api", MockService.get_all_files_from_api
)
@mock.patch.object(GoogleSnapshotService, "create_file_snapshot", MockService.get_false)
@mock.patch.object(
    GoogleSnapshotService,
    "perform_inherit_direct_permission_analysis",
    MockService.perform_inherit_direct_permission_analysis,
)
def test_invalid_create_file_snapshot_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_root_id_from_api", MockService.get_root_id_from_api
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_all_shared_drives_from_api",
    MockService.get_all_shared_drives_from_api,
)
@mock.patch.object(
    GoogleSnapshotService, "get_all_files_from_api", MockService.get_all_files_from_api
)
@mock.patch.object(
    GoogleSnapshotService, "create_file_snapshot", MockService.create_file_snapshot
)
@mock.patch.object(
    GoogleSnapshotService,
    "perform_inherit_direct_permission_analysis",
    MockService.get_false,
)
def test_invalid_analysis_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "delete_file_snapshot", MockService.delete_file_snapshot
)
def test_valid_delete_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.delete("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_get_user_id_delete_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.delete("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(GoogleSnapshotService, "delete_file_snapshot", MockService.get_false)
def test_invalid_delete_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.delete("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "edit_file_snapshot_name",
    MockService.edit_file_snapshot_name,
)
def test_valid_edit_file_snapshot_name():
    body = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "new_snapshot_name": "MOCK_NEW_FILE_SNAPSHOT1",
    }
    response = client.put("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
@mock.patch.object(
    GoogleSnapshotService,
    "edit_file_snapshot_name",
    MockService.edit_file_snapshot_name,
)
def test_invalid_get_user_id_edit_file_snapshot_name():
    body = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "new_snapshot_name": "MOCK_NEW_FILE_SNAPSHOT1",
    }
    response = client.put("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "edit_file_snapshot_name", MockService.get_false
)
def test_invalid_edit_file_snapshot_name():
    body = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "new_snapshot_name": "MOCK_NEW_FILE_SNAPSHOT1",
    }
    response = client.put("/apps/snapshot/v1/google/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_file_snapshot_names",
    MockService.get_file_snapshot_names,
)
def test_valid_get_file_snapshot_names():
    response = client.get("/apps/snapshot/v1/google/files/names")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_get_file_snapshot_names():
    response = client.get("/apps/snapshot/v1/google/files/names")
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_file_snapshot_names", MockService.get_none
)
def test_invalid_get_file_snapshot_names():
    response = client.get("/apps/snapshot/v1/google/files/names")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_shared_drives", MockService.get_shared_drives
)
def test_valid_get_shared_drives():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.get("/apps/snapshot/v1/google/files/drives", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_get_shared_drives():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.get("/apps/snapshot/v1/google/files/drives", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(GoogleSnapshotService, "get_shared_drives", MockService.get_none)
def test_invalid_get_shared_drives():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.get("/apps/snapshot/v1/google/files/drives", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_files_of_my_drive", MockService.get_files_of_my_drive
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_get_my_drive_file_snapshot():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "offset": None,
        "limit": None,
        "my_drive": True,
        "shared_with_me": False,
        "shared_drive": False,
        "folder_id": None,
    }
    response = client.get("/apps/snapshot/v1/google/files", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_files_of_shared_with_me",
    MockService.get_files_of_shared_with_me,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_get_shared_with_me_file_snapshot():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "offset": None,
        "limit": None,
        "my_drive": False,
        "shared_with_me": True,
        "shared_drive": False,
        "folder_id": None,
    }
    response = client.get("/apps/snapshot/v1/google/files", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_files_of_shared_drive",
    MockService.get_files_of_shared_drive,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_get_shared_drive_file_snapshot():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "offset": None,
        "limit": None,
        "my_drive": False,
        "shared_with_me": False,
        "shared_drive": True,
        "folder_id": "MOCK_SHARED_DRIVE1",
    }
    response = client.get("/apps/snapshot/v1/google/files", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_files_of_folder", MockService.get_files_of_folder
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_get_under_folder_file_snapshot():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "offset": None,
        "limit": None,
        "my_drive": False,
        "shared_with_me": False,
        "shared_drive": False,
        "folder_id": "MOCK_FOLDER_ID1",
    }
    response = client.get("/apps/snapshot/v1/google/files", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_get_file_snapshot():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "offset": None,
        "limit": None,
        "my_drive": True,
        "shared_with_me": False,
        "shared_drive": False,
        "folder_id": None,
    }
    response = client.get("/apps/snapshot/v1/google/files", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(GoogleSnapshotService, "get_files_of_folder", MockService.get_none)
def test_invalid_files_get_file_snapshot():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "offset": None,
        "limit": None,
        "my_drive": False,
        "shared_with_me": False,
        "shared_drive": False,
        "folder_id": "MOCK_FOLDER_ID1",
    }
    response = client.get("/apps/snapshot/v1/google/files", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_files_of_folder", MockService.get_files_of_folder
)
@mock.patch.object(
    GoogleSnapshotService, "get_permission_of_files", MockService.get_none
)
def test_invalid_permissions_get_file_snapshot():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "offset": None,
        "limit": None,
        "my_drive": False,
        "shared_with_me": False,
        "shared_drive": False,
        "folder_id": "MOCK_FOLDER_ID1",
    }
    response = client.get("/apps/snapshot/v1/google/files", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_file_folder_sharing_difference",
    MockService.get_file_folder_sharing_difference,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_file_folder_sharing_difference():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "file_id": "MOCK_FILE_ID1"}
    response = client.get(
        "/apps/snapshot/v1/google/files/differences/sharing", params=params
    )
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_file_folder_sharing_difference():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "file_id": "MOCK_FILE_ID1"}
    response = client.get(
        "/apps/snapshot/v1/google/files/differences/sharing", params=params
    )
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_file_folder_sharing_difference", MockService.get_none
)
def test_invalid_file_folder_sharing_difference():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "file_id": "MOCK_FILE_ID1"}
    response = client.get(
        "/apps/snapshot/v1/google/files/differences/sharing", params=params
    )
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_difference_of_two_snapshots",
    MockService.get_difference_of_two_snapshots,
)
def test_valid_snapshot_difference():
    params = {
        "base_snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "compare_snapshot_name": "MOCK_FILE_SNAPSHOT2",
    }
    response = client.get("/apps/snapshot/v1/google/files/differences", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_snapshot_difference():
    params = {
        "base_snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "compare_snapshot_name": "MOCK_FILE_SNAPSHOT2",
    }
    response = client.get("/apps/snapshot/v1/google/files/differences", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_difference_of_two_snapshots", MockService.get_none
)
def test_invalid_snapshot_difference():
    params = {
        "base_snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "compare_snapshot_name": "MOCK_FILE_SNAPSHOT2",
    }
    response = client.get("/apps/snapshot/v1/google/files/differences", params=params)
    assert response.status_code == 500


@pytest.mark.asyncio
@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "scratch_group_memberships_from_file",
    MockService.scratch_group_memberships_from_file,
)
@mock.patch.object(
    GoogleSnapshotService, "create_group_snapshot", MockService.create_group_snapshot
)
async def test_valid_create_group_membership_snapshot():
    with open(absolute_path_to_data + "/member_list.html") as file:
        body = {
            "group_name": "cse416",
            "group_email": "cse416s@cs.stonybrook.edu",
            "create_time": 1666240112000,
        }
        response = client.post(
            "/apps/snapshot/v1/google/groups",
            data=body,
            files={"file": ("member_list.html", file, "text/html")},
        )
        assert response.status_code == 201


@pytest.mark.asyncio
@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
async def test_invalid_user_id_create_group_membership_snapshot():
    with open(absolute_path_to_data + "/member_list.html") as file:
        body = {
            "group_name": "cse416",
            "group_email": "cse416s@cs.stonybrook.edu",
            "create_time": 1666240112000,
        }
        response = client.post(
            "/apps/snapshot/v1/google/groups",
            data=body,
            files={"file": ("member_list.html", file, "text/html")},
        )
        assert response.status_code == 404


@pytest.mark.asyncio
@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "scratch_group_memberships_from_file",
    MockService.get_invalid_scratch_group_memberships_from_file,
)
async def test_invalid_memberships_create_group_membership_snapshot():
    with open(absolute_path_to_data + "/member_list.html") as file:
        body = {
            "group_name": "cse416",
            "group_email": "cse416@cs.stonybrook.edu",
            "create_time": 1666240112000,
        }
        response = client.post(
            "/apps/snapshot/v1/google/groups",
            data=body,
            files={"file": ("member_list.html", file, "text/html")},
        )
        assert response.status_code == 400


@pytest.mark.asyncio
@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "scratch_group_memberships_from_file",
    MockService.scratch_group_memberships_from_file,
)
@mock.patch.object(
    GoogleSnapshotService, "create_group_snapshot", MockService.get_false
)
async def test_invalid_create_group_membership_snapshot():
    with open(absolute_path_to_data + "/member_list.html") as file:
        body = {
            "group_name": "cse416",
            "group_email": "cse416s@cs.stonybrook.edu",
            "create_time": 1666240112000,
        }
        response = client.post(
            "/apps/snapshot/v1/google/groups",
            data=body,
            files={"file": ("member_list.html", file, "text/html")},
        )
        assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_recent_group_membership_snapshots",
    MockService.get_recent_group_membership_snapshots,
)
def test_valid_get_group_membership_snapshots():
    response = client.get("/apps/snapshot/v1/google/groups")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_get_group_membership_snapshots():
    response = client.get("/apps/snapshot/v1/google/groups")
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_recent_group_membership_snapshots", MockService.get_none
)
def test_invalid_get_group_membership_snapshots():
    response = client.get("/apps/snapshot/v1/google/groups")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_recent_queries",
    MockService.get_recent_queries,
)
def test_valid_get_recent_queries():
    response = client.get("/apps/snapshot/v1/google/queries")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_recent_queries",
    MockService.get_none,
)
def test_invalid_get_recent_queries():
    response = client.get("/apps/snapshot/v1/google/queries")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_email_from_token", MockService.get_none
)
def test_invalid_user_email_get_recent_queries():
    response = client.get("/apps/snapshot/v1/google/queries")
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_unique_members_of_file_snapshot",
    MockService.get_unique_members_of_file_snapshot,
)
def test_valid_get_unique_members_of_file_snapshot():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "is_groups": False}
    response = client.get("/apps/snapshot/v1/google/files/members", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_unique_members_of_file_snapshot",
    MockService.get_none,
)
def test_invalid_get_unique_members_of_file_snapshot():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "is_groups": False}
    response = client.get("/apps/snapshot/v1/google/files/members", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_get_unique_members_of_file_snapshot():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "is_groups": False}
    response = client.get("/apps/snapshot/v1/google/files/members", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "validate_query",
    MockService.validate_query,
)
@mock.patch.object(
    GoogleSnapshotService,
    "process_query_search",
    MockService.process_query_search,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_groups_off_search_files():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "query": "groups:off and drive:MyDrive",
    }
    response = client.get("/apps/snapshot/v1/google/files/search", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "validate_query",
    MockService.validate_query,
)
@mock.patch.object(
    GoogleSnapshotService,
    "process_query_search",
    MockService.process_query_search,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_groups_on_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/google/files/search", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/google/files/search", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService, "get_user_email_from_token", MockService.get_none
)
def test_invalid_user_email_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/google/files/search", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "validate_query",
    MockService.validate_query_invalid,
)
def test_invalid_query_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drvie:MyDrive"}
    response = client.get("/apps/snapshot/v1/google/files/search", params=params)
    assert response.status_code == 400


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "validate_query",
    MockService.validate_query,
)
@mock.patch.object(
    GoogleSnapshotService,
    "process_query_search",
    MockService.get_none,
)
def test_invalid_process_query_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/google/files/search", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    GoogleSnapshotService,
    "validate_query",
    MockService.validate_query,
)
@mock.patch.object(
    GoogleSnapshotService,
    "process_query_search",
    MockService.process_query_search,
)
@mock.patch.object(
    GoogleSnapshotService,
    "get_permission_of_files",
    MockService.get_none,
)
def test_invalid_permissions_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/google/files/search", params=params)
    assert response.status_code == 500
