import os
from app.services.mongodb import MongoDB


class DataBase:
    def __init__(self):  # pragma: no cover
        url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB_NAME")
        self._db = MongoDB(url, db_name)
        self.collection_name = "auth"

    def save_user(self, email):
        user = {"email": email, "recent_queries": []}
        self._db.insert_document(self.collection_name, user)

    def check_user_exists(self, email):
        query = {"email": email}
        data = self._db.find_document(self.collection_name, query)
        if data is not None and data != {}:
            return True
        return False

    def get_user(self, email):
        query = {"email": email}
        filter_query = {"recent_queries": 0}
        data = self._db.find_document(self.collection_name, query, filter_query=filter_query)
        return data

    def get_recent_queries(self, email):
        query = {"email": email}
        filter_query = {"recent_queries": 1}
        data = self._db.find_document(self.collection_name, query, filter_query=filter_query)
        return data["recent_queries"]

    def update_recent_queries(self, email, recent_query):
        # TODO: if same query exist in previous array pop that element and push to most recent query
        query = {"email": email, "recent_queries": {"$ne": recent_query}}
        update_query = {"$push": {"recent_queries": recent_query}}
        self._db.update_document(self.collection_name, update_query, query)
