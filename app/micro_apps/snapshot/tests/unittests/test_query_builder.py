import mock
import pytest
from .mock.mock_database import MockDB
from app.micro_apps.snapshot.services.google.query_builder import GoogleQueryBuilder

absolute_path_to_data = "./app/micro_apps/snapshot/tests/data"

mock_access_token = "ACCESS_TOKEN"


def new_init(self, user_id, user_email, snapshot_name):
    self._snapshot_db = MockDB(user_id)
    self.user_email = user_email
    self.snapshot_name = snapshot_name
    self.boolean_operators = None
    self.operators = None
    self.initialize_grammar_factory()
    self.all_files = self._snapshot_db.get_all_files_of_snapshot(self.snapshot_name)
    self.is_groups = True


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_create_tree_from_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "drive:MyDrive and (from:yoobae@cs.stonybrook.edu or name:HI_FOLDER)"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    tree = mock_query_builder.create_tree_from_query(mock_query)
    assert tree.data == "and"
    assert tree.left.data == "or"
    assert tree.left.left.data == ["name", ":", "HI_FOLDER"]
    assert tree.left.right.data == ["from", ":", "yoobae@cs.stonybrook.edu"]
    assert tree.right.data == ["drive", ":", "MyDrive"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_create_tree_from_query2():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "drive:MyDrive and -name:HI_FOLDER"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    tree = mock_query_builder.create_tree_from_query(mock_query)
    assert tree.data == "and"
    assert tree.left.data == "-"
    assert tree.left.left.data == ["name", ":", "HI_FOLDER"]
    assert tree.right.data == ["drive", ":", "MyDrive"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_email():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_email = "yoobae@cs.stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    valid = mock_query_builder.validate_email(mock_email)
    assert valid


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_validate_email():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_email = "yoobae.com"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    valid = mock_query_builder.validate_email(mock_email)
    assert not valid


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_drive_my_drive():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_drive_name = "mydrive"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    valid = mock_query_builder.validate_drive(mock_drive_name)
    assert valid


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_drive():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_drive_name = "WeByte"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    valid = mock_query_builder.validate_drive(mock_drive_name)
    assert valid


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_validate_drive():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "FILE_SNAPSHOT1"
    mock_drive_name = "INVALID"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    with pytest.raises(ValueError):
        mock_query_builder.validate_drive(mock_drive_name)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_user():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_email = "yoobae@cs.stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    new_email = mock_query_builder.validate_user(mock_email)
    assert new_email == mock_email


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_user_me():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_email = "me"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    new_email = mock_query_builder.validate_user(mock_email)
    assert new_email == mock_user_email


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_validate_user():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_email = "yoobae"
    mock_fixed_email = "yoobae@cs.stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    new_email = mock_query_builder.validate_user(mock_email)
    assert new_email == mock_fixed_email


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_boolean_operator():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_boolean_operator = "and"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_boolean_operator(mock_boolean_operator)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_validate_boolean_operator():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_boolean_operator = "not"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    with pytest.raises(ValueError):
        mock_query_builder.validate_boolean_operator(mock_boolean_operator)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_operator():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "from"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_operator(mock_operator)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_validate_operator():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "here"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    with pytest.raises(ValueError):
        mock_query_builder.validate_operator(mock_operator)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_regex():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "from"
    mock_regex_expr = "^HI_FOLDER$"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_regex(mock_operator, mock_regex_expr)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_validate_regex():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "from"
    mock_regex_expr = "["
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    with pytest.raises(ValueError):
        mock_query_builder.validate_regex(mock_operator, mock_regex_expr)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_path():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_path = "/hi"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_path(mock_path)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_validate_path():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_path = "h//d3///"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    with pytest.raises(ValueError):
        mock_query_builder.validate_path(mock_path)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_value_drive():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "drive"
    mock_value = "mydrive"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_value(mock_operator, mock_value)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_value_user():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "from"
    mock_value = "yooha.bae@stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_value(mock_operator, mock_value)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_value_regex():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "name"
    mock_value = "HI_FOLDER"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_value(mock_operator, mock_value)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_value_path():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "path"
    mock_value = "/HI"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_value(mock_operator, mock_value)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_validate_value_sharing():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "sharing"
    mock_value = "none"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.validate_value(mock_operator, mock_value)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_validate_value():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_operator = "sharing"
    mock_value = "invalid"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    with pytest.raises(ValueError):
        mock_query_builder.validate_value(mock_operator, mock_value)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_create_tree_and_validate():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "drive:MyDrive and -name:HI_FOLDER"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    mock_query_builder.create_tree_and_validate(mock_query)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_drive_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "drive:WeByte"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID6", "FILEID7", "FILEID19"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_owner_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "owner:yoollee@cs.stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID1", "FILEID3", "FILEID4"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_from_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "from:yoollee@cs.stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID1", "FILEID3"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_to_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "to:yoollee@cs.stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID16", "FILEID17"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_readable_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "readable:piplup2k@gmail.com"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID6"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_writable_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "writable:yoollee@cs.stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID16"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_name_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "name:^Hi"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID1", "FILEID4"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_infolder_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "inFolder:FOLDER_1"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID11", "FILEID12", "FILEID19"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_folder_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "folder:FOLDER_1"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID11", "FILEID12", "FILEID19"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_path_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "path:/WeByte/FOLDER_1"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID19"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_sharing_none_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "sharing:none"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == [
        "FILEID2",
        "FILEID6",
        "FILEID7",
        "FILEID8",
        "FILEID14",
        "FILEID19",
        "FILEID20",
        "FILEID9",
        "FILEID10",
        "FILEID11",
        "FILEID12",
    ]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_sharing_anyone_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "sharing:anyone"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == []


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_sharing_domain_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "sharing:domain"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == [
        "FILEID1",
        "FILEID2",
        "FILEID6",
        "FILEID7",
        "FILEID8",
        "FILEID14",
        "FILEID16",
        "FILEID17",
        "FILEID3",
        "FILEID4",
    ]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_invalid_operator_get_files_of_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "invalid:off and sharing:none"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    with pytest.raises(ValueError):
        mock_query_builder.get_files_of_query(mock_query)


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_and_not_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "drive:MyDrive and -name:HI_FOLDER"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID5"]


@mock.patch.object(GoogleQueryBuilder, "__init__", new_init)
def test_valid_get_files_of_or_query():
    mock_user_id = "MOCK_USER_ID1"
    mock_user_email = "yoobae@cs.stonybrook.edu"
    mock_snapshot_name = "MOCK_FILE_SNAPSHOT1"
    mock_query = "drive:MyDrive or owner:yoobae@cs.stonybrook.edu"
    mock_query_builder = GoogleQueryBuilder(mock_user_id, mock_user_email, mock_snapshot_name)
    files = mock_query_builder.get_files_of_query(mock_query)
    file_ids = [f["id"] for f in files]
    assert file_ids == ["FILEID5"]
