import re
from .service import SnapshotDataBase
from app.utils.util import BinaryTree, ListOfDictsComparor
import pyparsing as pp


class QueryBuilder:
    def __init__(self, user_id, user_email, snapshot_name):
        self._db = SnapshotDataBase(user_id)
        self.user_email = user_email
        self.snapshot_name = snapshot_name
        self.boolean_operators = None
        self.operators = None
        self.initialize_grammar_factory()
        self.all_files = self._db.get_all_files_of_snapshot(self.snapshot_name)
        self.is_groups = True

    def create_tree_from_query(self, query):
        operator = pp.Regex(":").setName("operator")
        key = pp.Regex(r"([a-zA-Z0-9_\-\.@]+)")
        value = pp.Regex(r"\"([a-zA-Z0-9_\-\.@^$]\/ +]+)\"|([a-zA-Z0-9_\-\.@^$\/]+)")
        condition = pp.Group(key + operator + value)

        expr = pp.infix_notation(
            condition,
            [
                ("-", 1, pp.OpAssoc.RIGHT),
                (pp.one_of("and or"), 2, pp.OpAssoc.RIGHT),
            ],
        )

        parsed_expr = expr.parseString(query).asList()[0]
        tree = self.create_tree_from_parsed_expression(parsed_expr)
        return tree

    def create_tree_from_parsed_expression(self, parsed_expr):
        if parsed_expr is []:
            return
        if ":" in parsed_expr:
            root = parsed_expr
            left = None
            right = None
        elif len(parsed_expr) == 2:
            left = parsed_expr.pop()
            root = parsed_expr.pop()
            right = None
        else:
            left = parsed_expr.pop()
            root = parsed_expr.pop()
            right = parsed_expr.pop()
        tree = BinaryTree(root)
        if left:
            tree.left = self.create_tree_from_parsed_expression(left)
        if right:
            tree.right = self.create_tree_from_parsed_expression(right)
        return tree

    def initialize_grammar_factory(self):
        _and = "and"
        _or = "or"
        _not = "-"
        boolean_operators = [_and, _or, _not]
        operators = [
            "drive",
            "owner",
            # "creator",
            # "from",
            # "to",
            "readable",
            "writable",
            # "sharable",
            "name",
            "inFolder",
            "folder",
            "path",
            "sharing",
        ]
        self.boolean_operators = boolean_operators
        self.operators = operators

    def validate_email(self, email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def validate_drive(self, drive_name):
        if drive_name.lower() == "mydrive":
            return "MyDrive"
        else:
            shared_drives = self._db.get_shared_drives(self.snapshot_name)
            shared_drive_names = [x["name"] for x in shared_drives]
            if drive_name not in shared_drive_names:
                raise ValueError(
                    f"No Such Shared Drive: {drive_name} for the 'drive:' argument"
                )
            return drive_name

    def validate_user(self, operator, user_email):
        if user_email == "me":
            return self.user_email
        else:
            if not self.validate_email(user_email):
                raise ValueError(
                    f"Invalid Email: {user_email} for the '{operator}:' argument"
                )
            return user_email

    def validate_boolean_operator(self, bool_operator):
        if bool_operator not in self.boolean_operators:
            raise ValueError(
                f"Invalid Boolean Operator: {bool_operator} is not one of: and, or, -"
            )

    def validate_operator(self, operator):
        if operator not in self.operators:
            raise ValueError(
                f"Invalid Operator: {operator} is not one of: "
                + ", ".join(self.operators)
            )

    def validate_regex(self, operator, regex_expr):
        try:
            re.compile(regex_expr)
        except Exception:
            raise ValueError(
                f"Invalid Regex Value: {operator}:{regex_expr} is not valid"
            )

    def validate_path(self, path):
        path_pattern = r"^([\/]{1}[a-z0-9.]+)+(\/?){1}$|^([\/]{1})$"
        try:
            re.match(path_pattern, path)
        except Exception:
            raise ValueError(f"Invalid Path Value: {path} is not in the correct format")

    def validate_value(self, operator, value):
        if operator == "drive":
            self.validate_drive(value)
        elif operator in [
            "owner",
            "creator",
            # "from",
            # "to",
            "readable",
            "writable",
            # "sharable",
        ]:
            self.validate_user(operator, value)
        elif operator in ["name", "folder", "inFolder"]:
            self.validate_regex(operator, value)
        elif operator == "path":
            pass
        elif operator == "sharing":
            sharing_options = ["none", "anyone", "individual", "domain"]
            if value not in sharing_options:
                raise ValueError(
                    f"Invalid Sharing Option: {value} is not one of "
                    + ", ".join(sharing_options)
                )

    def validate(self, tree):
        if tree.data is None:
            return
        node = tree.data
        if type(node) == str:
            boolean_operator = node
            self.validate_boolean_operator(boolean_operator)
        elif type(node) == list:
            operator = node[0]
            self.validate_operator(operator)
            value = node[2]
            self.validate_value(operator, value)
        if tree.left is not None:
            self.validate(tree.left)
        if tree.right is not None:
            self.validate(tree.right)

    def get_files_of_query(self, query):
        tree = self.create_tree_from_query(query)
        files = self.get_files_from_tree(tree)
        return files

    def get_files_from_tree(self, tree):
        node = tree.data
        left_files = []
        right_files = []
        if type(node) == list:
            operator = node[0]
            value = node[2]
            return self.get_file_of_operator(operator, value)
        if type(node) == str:
            boolean_operator = node
            if tree.left is not None:
                left_files = self.get_files_from_tree(tree.left)
            if tree.right is not None:
                right_files = self.get_files_from_tree(tree.right)
            if boolean_operator == "and":
                if left_files and right_files:
                    return ListOfDictsComparor.intersection(left_files, right_files)
            elif boolean_operator == "or":
                if left_files and right_files:
                    return ListOfDictsComparor.union(left_files, right_files)
            elif boolean_operator == "-":
                return ListOfDictsComparor.difference(self.all_files, left_files)

    def get_file_of_operator(self, operator, value):
        files = []
        if operator == "drive":
            regex_path = rf"^\/{value}"
            files = self._db.get_files_with_path_regex(self.snapshot_name, regex_path)
        elif operator in ["owner", "readable", "writable"]:
            if operator == "readable":
                operator = "reader"
            elif operator == "writable":
                operator = "writer"
            if self.is_groups:
                # get files including the group emails the email is in
                files = self._db.get_files_with_certain_role_including_groups(
                    self.snapshot_name, operator, value
                )
            else:
                files = self._db.get_files_with_certain_role(
                    self.snapshot_name, operator, value
                )
        elif operator == "name":
            regex_expr = re.compile(value)
            files = self._db.get_files_that_match_file_name_regex(
                self.snapshot_name, regex_expr
            )
        elif operator == "inFolder":
            folder_ids_and_names = self._db.get_folders_with_regex(
                self.snapshot_name, value
            )
            files = []
            for folder in folder_ids_and_names:
                folder_id = folder["id"]
                files = ListOfDictsComparor.union(
                    files,
                    self._db.get_file_under_folder(
                        self.snapshot_name, folder_id=folder_id
                    ),
                )
        elif operator == "folder":
            folder_ids_and_names = self._db.get_folders_with_regex(
                self.snapshot_name, value
            )
            files = []
            for folder in folder_ids_and_names:
                folder_path = rf"^{folder['path']}/{folder['name']}$"
                files = ListOfDictsComparor.union(
                    files,
                    self._db.get_files_with_path_regex(self.snapshot_name, folder_path),
                )
        elif operator == "path":
            regex_path = rf"^{value}"
            files = self._db.get_files_with_path_regex(self.snapshot_name, regex_path)
        elif operator == "sharing":
            if value == "none":
                pass
            elif value == "individual":
                pass
            elif value == "domain":
                pass
        else:
            raise ValueError("Invalid Operator")
        return files

    def create_tree_and_validate(self, query):
        tree = self.create_tree_from_query(query)
        self.validate(tree)
