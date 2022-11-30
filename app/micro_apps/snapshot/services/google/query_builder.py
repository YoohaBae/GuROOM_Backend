import re
import pyparsing as pp
from app.services.query_builder import QueryBuilder
from app.utils.util import BinaryTree, ListOfDictsComparor
from .service import GoogleSnapshotDatabase


class GoogleQueryBuilder(QueryBuilder):
    def __init__(self, user_id, user_email, snapshot_name):
        super().__init__(GoogleSnapshotDatabase(user_id), user_email, snapshot_name)
        self.is_groups = True

    def create_tree_from_query(self, query):
        # pp -> pyparsing package that creates infix notation based on strings
        operator = pp.Regex(":").setName("operator")
        key = pp.Regex(r"([a-zA-Z0-9_\-\.@]+)")
        value = pp.Regex(r"\"([a-zA-Z0-9_\-\.@^$]\/ +]+)\"|([a-zA-Z0-9_\-\.@^$\/]+)")
        condition = pp.Group(key + operator + value)
        # creates infix notation based on the above rules
        expr = pp.infix_notation(
            condition,
            [
                ("-", 1, pp.OpAssoc.RIGHT),
                (pp.one_of("and or"), 2, pp.OpAssoc.RIGHT),
            ],
        )
        # get the string of the infix notation
        parsed_expr = expr.parseString(query).asList()[0]
        # create tree from the infix notation
        tree = self.create_tree_from_parsed_expression(parsed_expr)
        return tree

    def create_tree_from_parsed_expression(self, parsed_expr):
        if parsed_expr is []:
            return
        # simple search query
        if ":" in parsed_expr:
            root = parsed_expr
            left = None
            right = None
        # - operator
        elif len(parsed_expr) == 2:
            left = parsed_expr.pop()
            root = parsed_expr.pop()
            right = None
        # and or operator
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
            "from",
            "to",
            "readable",
            "writable",
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
            shared_drives = self._snapshot_db.get_shared_drives(self.snapshot_name)
            # check if drive exists in shared drives
            shared_drive_names = [x["name"] for x in shared_drives]
            if drive_name not in shared_drive_names:
                raise ValueError(
                    f"No Such Shared Drive: {drive_name} for the 'drive:' argument"
                )
            return drive_name

    def validate_user(self, user_email):
        # user email is me
        if user_email == "me":
            # replace it with user email
            return self.user_email
        else:
            # validate email format
            if not self.validate_email(user_email):
                # get domain from user email
                domain = re.search(r"@[\w.]+", self.user_email).group()
                # create new email by attaching domain of account user email to end
                user_email = user_email + domain
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
        path_pattern = r"^([\/]{1}[a-zA-Z0-9.][^\\]+)+(\/?){1}$|^([\/]{1})$"
        try:
            if re.match(path_pattern, path):
                pass
            else:
                raise ValueError(
                    f"Invalid Path Value: {path} is not in the correct format"
                )
        except Exception:
            raise ValueError(f"Invalid Path Value: {path} is not in the correct format")

    def validate_value(self, operator, value):
        # drive is the operator
        if operator == "drive":
            self.validate_drive(value)
        # operator is one of the following
        elif operator in [
            "owner",
            "creator",
            "from",
            "to",
            "readable",
            "writable",
            # "sharable",
        ]:
            self.validate_user(value)
        elif operator in ["name", "folder", "inFolder"]:
            self.validate_regex(operator, value)
        elif operator == "path":
            self.validate_path(value)
        elif operator == "sharing":
            sharing_options = ["none", "anyone", "domain"]
            if value not in sharing_options:
                raise ValueError(
                    f"Invalid Sharing Option: {value} is not one of "
                    + ", ".join(sharing_options)
                )

    def validate(self, tree):
        if tree.data is None:
            return
        node = tree.data
        # validate boolean operator
        if type(node) == str:
            boolean_operator = node
            self.validate_boolean_operator(boolean_operator)
        # validate tree
        elif type(node) == list:
            operator = node[0]
            self.validate_operator(operator)
            value = node[2]
            self.validate_value(operator, value)
        # if left node of tree exists, validate left node
        if tree.left is not None:
            self.validate(tree.left)
        # if right node of tree exists, validate right node
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
        # node is simple query
        if type(node) == list:
            operator = node[0]
            value = node[2]
            return self.get_file_of_operator(operator, value)
        # node is boolean operator
        if type(node) == str:
            boolean_operator = node
            if tree.left is not None:
                left_files = self.get_files_from_tree(tree.left)
            if tree.right is not None:
                right_files = self.get_files_from_tree(tree.right)
            if boolean_operator == "and":
                # get intersection
                if left_files is not None and right_files is not None:
                    return ListOfDictsComparor.intersection(left_files, right_files)
            elif boolean_operator == "or":
                # get union
                if left_files is not None and right_files is not None:
                    return ListOfDictsComparor.union(left_files, right_files)
            elif boolean_operator == "-":
                # get difference
                return ListOfDictsComparor.difference(self.all_files, left_files)

    def get_file_of_operator(self, operator, value):
        files = []
        # file of drive operator
        if operator == "drive":
            regex_path = rf"^/{value}"
            files = self._snapshot_db.get_files_with_path_regex(
                self.snapshot_name, regex_path
            )
        # file of roles operator
        elif operator in ["owner", "readable", "writable"]:
            if operator == "readable":
                operator = "reader"
            elif operator == "writable":
                operator = "writer"
            email = self.validate_user(value)
            if self.is_groups:
                # get files including the group emails the email is in
                files = self._snapshot_db.get_files_with_certain_role_including_groups(
                    self.snapshot_name, operator, email
                )
                if files is None:
                    raise ValueError("file data is invalid")
            else:
                files = self._snapshot_db.get_files_with_certain_role(
                    self.snapshot_name, operator, email
                )
                if files is None:
                    raise ValueError("file data is invalid")
        # file of from operator
        elif operator == "from":
            email = self.validate_user(value)
            files = self._snapshot_db.get_files_with_sharing_user(
                self.snapshot_name, email
            )
        # file of to operator
        elif operator == "to":
            email = self.validate_user(value)
            file_ids = self._snapshot_db.get_directly_shared_permissions_file_ids(
                self.snapshot_name, email
            )
            unique_file_ids = [*set(file_ids)]
            files = self._snapshot_db.get_files_of_file_ids(
                self.snapshot_name, unique_file_ids
            )
        # file of file name operator
        elif operator == "name":
            regex_expr = value
            files = self._snapshot_db.get_files_that_match_file_name_regex(
                self.snapshot_name, regex_expr
            )
        # file that are in folder
        elif operator == "inFolder":
            folder_ids_and_names = self._snapshot_db.get_folders_with_regex(
                self.snapshot_name, value
            )
            files = []
            # for all folders => get all files that are only directly under that folder
            for folder in folder_ids_and_names:
                folder_id = folder["id"]
                files = ListOfDictsComparor.union(
                    files,
                    self._snapshot_db.get_file_under_folder(
                        self.snapshot_name, folder_id=folder_id
                    ),
                )
        # file that are under folder
        elif operator == "folder":
            folder_ids_and_names = self._snapshot_db.get_folders_with_regex(
                self.snapshot_name, value
            )
            files = []
            for folder in folder_ids_and_names:
                # get all folders and files under that folder recursively by using path regex
                folder_path = rf"^{folder['path']}/{folder['name']}$"
                files = ListOfDictsComparor.union(
                    files,
                    self._snapshot_db.get_files_with_path_regex(
                        self.snapshot_name, folder_path
                    ),
                )
        # file of path operator
        elif operator == "path":
            regex_path = rf"^{value}"
            files = self._snapshot_db.get_files_with_path_regex(
                self.snapshot_name, regex_path
            )
        # file of sharing operator
        elif operator == "sharing":
            if value == "none":
                files = self._snapshot_db.get_not_shared_files(self.snapshot_name)
            elif value == "anyone":
                file_ids = self._snapshot_db.get_file_ids_shared_with_anyone(
                    self.snapshot_name
                )
                unique_file_ids = [*set(file_ids)]
                files = self._snapshot_db.get_files_of_file_ids(
                    self.snapshot_name, unique_file_ids
                )
            elif value == "domain":
                # domain of user email
                domain = re.search(r"@[\w.]+", self.user_email).group()
                file_ids = self._snapshot_db.get_file_ids_shared_with_users_from_domain(
                    self.snapshot_name, domain
                )
                unique_file_ids = [*set(file_ids)]
                files = self._snapshot_db.get_files_of_file_ids(
                    self.snapshot_name, unique_file_ids
                )
        else:
            raise ValueError("Invalid Operator")
        return files

    def create_tree_and_validate(self, query):
        tree = self.create_tree_from_query(query)
        self.validate(tree)
