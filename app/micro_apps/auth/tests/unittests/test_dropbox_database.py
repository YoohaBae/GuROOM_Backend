import mock
from app.micro_apps.auth.services.dropbox.database import DropboxAuthDatabase
from app.micro_apps.auth.tests.unittests.mock.mock_mongodb import MockMongoDB

absolute_path_to_data = "./app/micro_apps/auth/tests/data"


def new_init(self):
    db_name = None
    url = None
    self._db = MockMongoDB(url, db_name, "dropbox")
    self.collection_name = "auth"


@mock.patch.object(DropboxAuthDatabase, "__init__", new_init)
def test_save_user():
    mock_database = DropboxAuthDatabase()
    mock_email = "yoobae@cs.stonybrook.edu"
    mock_database.save_user(mock_email)


@mock.patch.object(DropboxAuthDatabase, "__init__", new_init)
def test_check_user_exists_when_exists():
    mock_database = DropboxAuthDatabase()
    mock_email = "yoobae@cs.stonybrook.edu"
    exists = mock_database.check_user_exists(mock_email)
    assert exists


@mock.patch.object(DropboxAuthDatabase, "__init__", new_init)
def test_check_user_exists_when_not_exists():
    mock_database = DropboxAuthDatabase()
    mock_email = "yoollee@cs.stonybrook.edu"
    exists = mock_database.check_user_exists(mock_email)
    assert not exists


@mock.patch.object(DropboxAuthDatabase, "__init__", new_init)
def test_get_user():
    mock_database = DropboxAuthDatabase()
    mock_email = "yoobae@cs.stonybrook.edu"
    user_result = {
        "_id": "MOCK_USER_ID3",
        "email": "yoobae@cs.stonybrook.edu",
        "recent_queries": [
            {
                "query": "from: yooha.bae@stonybrook.edu",
                "search_time": "2022-10-28T01:50:35.403+00:00",
            }
        ],
        "type": "dropbox",
    }
    user = mock_database.get_user(mock_email)
    assert user_result == user


@mock.patch.object(DropboxAuthDatabase, "__init__", new_init)
def test_get_recent_queries():
    mock_database = DropboxAuthDatabase()
    mock_email = "yoobae@cs.stonybrook.edu"
    recent_queries = mock_database.get_recent_queries(mock_email)
    recent_queries_result = [
        {
            "query": "from: yooha.bae@stonybrook.edu",
            "search_time": "2022-10-28T01:50:35.403+00:00",
        }
    ]
    assert recent_queries_result == recent_queries


@mock.patch.object(DropboxAuthDatabase, "__init__", new_init)
def test_existing_update_or_push_recent_queries():
    mock_database = DropboxAuthDatabase()
    mock_email = "yoobae@cs.stonybrook.edu"
    mock_recent_query_obj = {
        "query": "drive:MyDrive",
        "datetime": "2022-10-29T01:50:35.403+00:00",
    }
    mock_database.update_or_push_recent_queries(mock_email, mock_recent_query_obj)


@mock.patch.object(DropboxAuthDatabase, "__init__", new_init)
def test_new_update_or_push_recent_queries():
    mock_database = DropboxAuthDatabase()
    mock_email = "new@cs.stonybrook.edu"
    mock_recent_query_obj = {
        "query": "drive:MyDrive",
        "datetime": "2022-10-29T01:50:35.403+00:00",
    }
    mock_database.update_or_push_recent_queries(mock_email, mock_recent_query_obj)
