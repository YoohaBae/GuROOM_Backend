import datetime
from app.services.auth_database import AuthDatabase


class GoogleAuthDatabase(AuthDatabase):
    def __init__(self):  # pragma: no cover
        super().__init__()

    def save_user(self, email):
        # save user email with type google and empty recent queries
        user = {"type": "google", "email": email, "recent_queries": []}
        self._db.insert_document(self.collection_name, user)

    def check_user_exists(self, email):
        query = {"email": email, "type": "google"}
        data = self._db.find_document(self.collection_name, query)
        if data is not None and data != {}:
            return True
        return False

    def get_user(self, email):
        query = {"email": email, "type": "google"}
        filter_query = {"recent_queries": 0}
        data = self._db.find_document(
            self.collection_name, query, filter_query=filter_query
        )
        return data

    def get_recent_queries(self, email):
        query = {"email": email, "type": "google"}
        filter_query = {"recent_queries": 1}
        data = self._db.find_document(
            self.collection_name, query, filter_query=filter_query
        )
        return data["recent_queries"]

    def update_or_push_recent_queries(self, email, recent_query_obj):
        query = {
            "email": email,
            "type": "google",
            "recent_queries": {"$elemMatch": {"query": recent_query_obj["query"]}},
        }
        exists = self._db.find_document(self.collection_name, query)
        if exists is not None and exists != {}:
            # update datetime of existing query
            query = {
                "email": email,
                "type": "google",
                "recent_queries.query": recent_query_obj["query"],
            }
            update_query = {
                "$set": {"recent_queries.$.search_time": datetime.datetime.utcnow()}
            }
        else:
            # push new recent query
            query = {"email": email, "type": "google"}
            update_query = {"$push": {"recent_queries": recent_query_obj}}
        self._db.update_document(self.collection_name, update_query, query)
