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
        pass

    def check_user_exists(self, email):
        pass

    def get_user(self, email):
        pass

    def get_recent_queries(self, email):
        pass

    def update_or_push_recent_queries(self, email, recent_query_obj):
        pass
