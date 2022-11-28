import mock
from fastapi.testclient import TestClient
from app.micro_apps.snapshot.endpoints.v1.dropbox import AuthJWT
from ...services.dropbox.service import DropboxSnapshotService
from app.main import app
from .mock.mock_authjwt import MockAuthJWT
from .mock.mock_dropbox_service import MockService

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data/dropbox"

client = TestClient(app)


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "check_duplicate_file_snapshot_name", MockService.get_false
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_all_files_and_permissions_from_api",
    MockService.get_all_files_and_permissions_from_api,
)
@mock.patch.object(
    DropboxSnapshotService, "create_file_snapshot", MockService.create_file_snapshot
)
@mock.patch.object(
    DropboxSnapshotService,
    "perform_inherit_direct_permission_analysis",
    MockService.perform_inherit_direct_permission_analysis,
)
def test_valid_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 201


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_none,
)
def test_invalid_user_id_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "check_duplicate_file_snapshot_name", MockService.get_true
)
def test_invalid_duplicate_name_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 400


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "check_duplicate_file_snapshot_name", MockService.get_false
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_none,
)
def test_invalid_user_email_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "check_duplicate_file_snapshot_name", MockService.get_false
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_all_files_and_permissions_from_api",
    MockService.get_two_none,
)
def test_invalid_all_files_permissions_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "check_duplicate_file_snapshot_name", MockService.get_false
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_all_files_and_permissions_from_api",
    MockService.get_all_files_and_permissions_from_api,
)
@mock.patch.object(DropboxSnapshotService, "create_file_snapshot", MockService.get_none)
def test_invalid_create_file_snapshot_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "check_duplicate_file_snapshot_name", MockService.get_false
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_all_files_and_permissions_from_api",
    MockService.get_all_files_and_permissions_from_api,
)
@mock.patch.object(
    DropboxSnapshotService, "create_file_snapshot", MockService.create_file_snapshot
)
@mock.patch.object(
    DropboxSnapshotService,
    "perform_inherit_direct_permission_analysis",
    MockService.get_none,
)
def test_invalid_analysis_take_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.post("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "delete_file_snapshot", MockService.delete_file_snapshot
)
def test_valid_delete_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.delete("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_get_user_id_delete_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.delete("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "delete_file_snapshot", MockService.get_false
)
def test_invalid_delete_file_snapshot():
    body = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.delete("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "edit_file_snapshot_name",
    MockService.edit_file_snapshot_name,
)
def test_valid_edit_file_snapshot_name():
    body = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "new_snapshot_name": "MOCK_NEW_FILE_SNAPSHOT1",
    }
    response = client.put("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
@mock.patch.object(
    DropboxSnapshotService,
    "edit_file_snapshot_name",
    MockService.edit_file_snapshot_name,
)
def test_invalid_get_user_id_edit_file_snapshot_name():
    body = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "new_snapshot_name": "MOCK_NEW_FILE_SNAPSHOT1",
    }
    response = client.put("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "edit_file_snapshot_name", MockService.get_false
)
def test_invalid_edit_file_snapshot_name():
    body = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "new_snapshot_name": "MOCK_NEW_FILE_SNAPSHOT1",
    }
    response = client.put("/apps/snapshot/v1/dropbox/files", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_file_snapshot_names",
    MockService.get_file_snapshot_names,
)
def test_valid_get_file_snapshot_names():
    response = client.get("/apps/snapshot/v1/dropbox/files/names")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_get_file_snapshot_names():
    response = client.get("/apps/snapshot/v1/dropbox/files/names")
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "get_file_snapshot_names", MockService.get_none
)
def test_invalid_get_file_snapshot_names():
    response = client.get("/apps/snapshot/v1/dropbox/files/names")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "get_files_of_folder", MockService.get_files_of_folder
)
@mock.patch.object(
    DropboxSnapshotService,
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
    response = client.get("/apps/snapshot/v1/dropbox/files", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_id_from_access_token", MockService.get_none
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
    response = client.get("/apps/snapshot/v1/dropbox/files", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(DropboxSnapshotService, "get_files_of_folder", MockService.get_none)
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
    response = client.get("/apps/snapshot/v1/dropbox/files", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "get_files_of_folder", MockService.get_files_of_folder
)
@mock.patch.object(
    DropboxSnapshotService, "get_permission_of_files", MockService.get_none
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
    response = client.get("/apps/snapshot/v1/dropbox/files", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_file_folder_sharing_difference",
    MockService.get_file_folder_sharing_difference,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_file_folder_sharing_difference():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "file_id": "MOCK_FILE_ID1"}
    response = client.get(
        "/apps/snapshot/v1/dropbox/files/differences/sharing", params=params
    )
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_file_folder_sharing_difference():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "file_id": "MOCK_FILE_ID1"}
    response = client.get(
        "/apps/snapshot/v1/dropbox/files/differences/sharing", params=params
    )
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "get_file_folder_sharing_difference", MockService.get_none
)
def test_invalid_file_folder_sharing_difference():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "file_id": "MOCK_FILE_ID1"}
    response = client.get(
        "/apps/snapshot/v1/dropbox/files/differences/sharing", params=params
    )
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_difference_of_two_snapshots",
    MockService.get_difference_of_two_snapshots,
)
def test_valid_snapshot_difference():
    params = {
        "base_snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "compare_snapshot_name": "MOCK_FILE_SNAPSHOT2",
    }
    response = client.get("/apps/snapshot/v1/dropbox/files/differences", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_snapshot_difference():
    params = {
        "base_snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "compare_snapshot_name": "MOCK_FILE_SNAPSHOT2",
    }
    response = client.get("/apps/snapshot/v1/dropbox/files/differences", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "get_difference_of_two_snapshots", MockService.get_none
)
def test_invalid_snapshot_difference():
    params = {
        "base_snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "compare_snapshot_name": "MOCK_FILE_SNAPSHOT2",
    }
    response = client.get("/apps/snapshot/v1/dropbox/files/differences", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_recent_queries",
    MockService.get_recent_queries,
)
def test_valid_get_recent_queries():
    response = client.get("/apps/snapshot/v1/dropbox/queries")
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_recent_queries",
    MockService.get_none,
)
def test_invalid_get_recent_queries():
    response = client.get("/apps/snapshot/v1/dropbox/queries")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_email_from_token", MockService.get_none
)
def test_invalid_user_email_get_recent_queries():
    response = client.get("/apps/snapshot/v1/dropbox/queries")
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_unique_members_of_file_snapshot",
    MockService.get_unique_members_of_file_snapshot,
)
def test_valid_get_unique_members_of_file_snapshot():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1"}
    response = client.get("/apps/snapshot/v1/dropbox/files/members", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_unique_members_of_file_snapshot",
    MockService.get_none,
)
def test_invalid_get_unique_members_of_file_snapshot():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "is_groups": False}
    response = client.get("/apps/snapshot/v1/dropbox/files/members", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_get_unique_members_of_file_snapshot():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "is_groups": False}
    response = client.get("/apps/snapshot/v1/dropbox/files/members", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "validate_query",
    MockService.validate_query,
)
@mock.patch.object(
    DropboxSnapshotService,
    "process_query_search",
    MockService.process_query_search,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_permission_of_files",
    MockService.get_permission_of_files,
)
def test_valid_groups_off_search_files():
    params = {
        "snapshot_name": "MOCK_FILE_SNAPSHOT1",
        "query": "groups:off and drive:MyDrive",
    }
    response = client.get("/apps/snapshot/v1/dropbox/files/search", params=params)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService, "get_user_id_from_access_token", MockService.get_none
)
def test_invalid_user_id_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/dropbox/files/search", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "get_user_email_from_token", MockService.get_none
)
def test_invalid_user_email_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/dropbox/files/search", params=params)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "validate_query",
    MockService.validate_query_invalid,
)
def test_invalid_query_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drvie:MyDrive"}
    response = client.get("/apps/snapshot/v1/dropbox/files/search", params=params)
    assert response.status_code == 400


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "validate_query",
    MockService.validate_query,
)
@mock.patch.object(
    DropboxSnapshotService,
    "process_query_search",
    MockService.get_none,
)
def test_invalid_process_query_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/dropbox/files/search", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_email_from_token",
    MockService.get_user_email_from_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "validate_query",
    MockService.validate_query,
)
@mock.patch.object(
    DropboxSnapshotService,
    "process_query_search",
    MockService.process_query_search,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_permission_of_files",
    MockService.get_none,
)
def test_invalid_permissions_search_files():
    params = {"snapshot_name": "MOCK_FILE_SNAPSHOT1", "query": "drive:MyDrive"}
    response = client.get("/apps/snapshot/v1/dropbox/files/search", params=params)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "check_duplicate_access_control_requirement",
    MockService.get_false,
)
@mock.patch.object(
    DropboxSnapshotService, "create_access_control_requirement", MockService.get_true
)
def test_valid_create_access_control_requirements():
    body = {
        "name": "ACR#1",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": True,
    }
    response = client.post("/apps/snapshot/v1/dropbox/access-controls", json=body)
    assert response.status_code == 201


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_none,
)
def test_invalid_user_id_create_access_control_requirements():
    body = {
        "name": "ACR#1",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": True,
    }
    response = client.post("/apps/snapshot/v1/dropbox/access-controls", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "check_duplicate_access_control_requirement",
    MockService.get_true,
)
def test_invalid_is_duplicate_create_access_control_requirements():
    body = {
        "name": "ACR#1",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": True,
    }
    response = client.post("/apps/snapshot/v1/dropbox/access-controls", json=body)
    assert response.status_code == 400


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "check_duplicate_access_control_requirement",
    MockService.get_none,
)
def test_invalid_check_duplicate_create_access_control_requirements():
    body = {
        "name": "ACR#1",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": True,
    }
    response = client.post("/apps/snapshot/v1/dropbox/access-controls", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "check_duplicate_access_control_requirement",
    MockService.get_false,
)
@mock.patch.object(
    DropboxSnapshotService, "create_access_control_requirement", MockService.get_false
)
def test_invalid_create_access_control_requirements():
    body = {
        "name": "ACR#1",
        "query": "drive:MyDrive",
        "AR": [],
        "AW": [],
        "DR": ["yoollee@cs.stonybrook.edu"],
        "DW": [],
        "Grp": True,
    }
    response = client.post("/apps/snapshot/v1/dropbox/access-controls", json=body)
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService,
    "get_access_control_requirements",
    MockService.get_access_control_requirements,
)
def test_valid_get_access_control_requirements():
    response = client.get(
        "/apps/snapshot/v1/dropbox/access-controls",
    )
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_none,
)
def test_invalid_user_id_get_access_control_requirements():
    response = client.get("/apps/snapshot/v1/dropbox/access-controls")
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "get_access_control_requirements", MockService.get_none
)
def test_invalid_get_access_control_requirements():
    response = client.get("/apps/snapshot/v1/dropbox/access-controls")
    assert response.status_code == 500


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "delete_access_control_requirement", MockService.get_true
)
def test_valid_delete_access_control_requirement():
    body = {"name": "ACR#1"}
    response = client.delete("/apps/snapshot/v1/dropbox/access-controls", json=body)
    assert response.status_code == 200


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_none,
)
def test_invalid_user_id_delete_access_control_requirement():
    body = {"name": "ACR#1"}
    response = client.delete("/apps/snapshot/v1/dropbox/access-controls", json=body)
    assert response.status_code == 404


@mock.patch.object(AuthJWT, "__init__", MockAuthJWT.__init__)
@mock.patch.object(AuthJWT, "jwt_required", MockAuthJWT.jwt_required)
@mock.patch.object(AuthJWT, "get_jwt_subject", MockAuthJWT.get_jwt_subject)
@mock.patch.object(
    DropboxSnapshotService,
    "get_user_id_from_access_token",
    MockService.get_user_id_from_access_token,
)
@mock.patch.object(
    DropboxSnapshotService, "delete_access_control_requirement", MockService.get_false
)
def test_invalid_delete_access_control_requirement():
    body = {"name": "ACR#1"}
    response = client.delete("/apps/snapshot/v1/dropbox/access-controls", json=body)
    assert response.status_code == 500
