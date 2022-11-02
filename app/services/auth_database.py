import os
import logging
from app.services.mongodb import MongoDB


class AuthDatabase:
    def __init__(self):
        format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=format)
        self.logger = logging.getLogger()
        url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB_NAME")
        self._db = MongoDB(url, db_name)
        self.collection_name = "auth"

    def save_user(self, email):
        """
        operation: save user to database
        :param email: email of user
        :return: None
        """
        raise NotImplementedError("Must be implemented by child class")

    def check_user_exists(self, email):
        """
        operation: check if user exists by finding user
        :param email: user email
        :return: True -> user exists, False -> user does not exist
        """
        raise NotImplementedError("Must be implemented by child class")

    def get_user(self, email):
        """
        operation: get user information
        :param email: user email
        :return: user with no recent queries
        """
        raise NotImplementedError("Must be implemented by child class")

    def get_recent_queries(self, email):
        """
        operation: retrieves recent queries of a user
        :param email: user email
        :return: list of recent queries
        """
        raise NotImplementedError("Must be implemented by child class")

    def update_or_push_recent_queries(self, email, recent_query_obj):
        """
        operation: Check if query exists -> if it exists: update search_time to now
                                        -> if not exists: append to recent_queries
        :param email:
        :param recent_query_obj: (query, search_time)
        :return: None
        """
        raise NotImplementedError("Must be implemented by child class")
