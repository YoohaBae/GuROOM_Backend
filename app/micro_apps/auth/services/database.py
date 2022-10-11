import os
from app.services.mongodb import MongoDB


class DataBase:
    def __init__(self):
        url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB_NAME")
        self._db = MongoDB(url, db_name)
        self.collection_name = "auth"
        self.user_profile_collection_name = "user_profile"

    def save_user(self, email):
        user = {"email": email}
        self._db.insert_document(self.collection_name, user)

    def check_user_exists(self, email):
        query = {"email": email}
        data = self._db.find_document(self.collection_name, query)
        if data:
            return True
        return False

    def get_user(self, email):
        query = {"email": email}
        data = self._db.find_document(self.collection_name, query)
        return data
