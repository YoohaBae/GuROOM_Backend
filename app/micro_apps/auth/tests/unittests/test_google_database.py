import mock
from app.micro_apps.auth.services.google.database import GoogleAuthDatabase
from app.micro_apps.auth.tests.unittests.mock.mock_mongodb import MockMongoDB

absolute_path_to_data = "./app/micro_apps/auth/tests/data"


def new_init(self):
    db_name = None
    url = None
    self._db = MockMongoDB(url, db_name)
    self.collection_name = "auth"


@mock.patch.object(GoogleAuthDatabase, "__init__", new_init)
def test_save_user():
    mock_database = GoogleAuthDatabase()
    mock_email = "yoobae@cs.stonybrook.edu"
    mock_database.save_user(mock_email)


@mock.patch.object(GoogleAuthDatabase, "__init__", new_init)
def test_check_user_exists_when_exists():
    mock_database = GoogleAuthDatabase()
    mock_email = "yoobae@cs.stonybrook.edu"
    exists = mock_database.check_user_exists(mock_email)
    assert exists


@mock.patch.object(GoogleAuthDatabase, "__init__", new_init)
def test_check_user_exists_when_not_exists():
    mock_database = GoogleAuthDatabase()
    mock_email = "yoollee@cs.stonybrook.edu"
    exists = mock_database.check_user_exists(mock_email)
    assert not exists


@mock.patch.object(GoogleAuthDatabase, "__init__", new_init)
def test_get_user():
    mock_database = GoogleAuthDatabase()
    mock_email = "yoobae@cs.stonybrook.edu"
    user_result = {
        "email": "yoobae@cs.stonybrook.edu",
        "recent_queries": [],
        "type": "google",
    }
    user = mock_database.get_user(mock_email)
    assert user_result == user
