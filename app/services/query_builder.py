class QueryBuilder:
    def __init__(self, snapshot_db, user_email, snapshot_name):
        self._snapshot_db = snapshot_db
        self.is_groups = True
        self.user_email = user_email
        self.snapshot_name = snapshot_name
        self.boolean_operators = None
        self.operators = None
        self.initialize_grammar_factory()
        self.all_files = self._snapshot_db.get_all_files_of_snapshot(self.snapshot_name)
        self.is_groups = True

    def create_tree_from_query(self, query):
        raise NotImplementedError("Must be implemented by child class")

    def create_tree_from_parsed_expression(self, parsed_expr):
        raise NotImplementedError("Must be implemented by child class")

    def initialize_grammar_factory(self):
        raise NotImplementedError("Must be implemented by child class")

    def validate_email(self, email):
        raise NotImplementedError("Must be implemented by child class")

    def validate_drive(self, drive_name):
        raise NotImplementedError("Must be implemented by child class")

    def validate_user(self, user_email):
        raise NotImplementedError("Must be implemented by child class")

    def validate_boolean_operator(self, bool_operator):
        raise NotImplementedError("Must be implemented by child class")

    def validate_operator(self, operator):
        raise NotImplementedError("Must be implemented by child class")

    def validate_regex(self, operator, regex_expr):
        raise NotImplementedError("Must be implemented by child class")

    def validate_path(self, path):
        raise NotImplementedError("Must be implemented by child class")

    def validate_value(self, operator, value):
        raise NotImplementedError("Must be implemented by child class")

    def validate(self, tree):
        raise NotImplementedError("Must be implemented by child class")

    def get_files_of_query(self, query):
        raise NotImplementedError("Must be implemented by child class")

    def get_files_from_tree(self, tree):
        raise NotImplementedError("Must be implemented by child class")

    def get_file_of_operator(self, operator, value):
        raise NotImplementedError("Must be implemented by child class")

    def create_tree_and_validate(self, query):
        raise NotImplementedError("Must be implemented by child class")
