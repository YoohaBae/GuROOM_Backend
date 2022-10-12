import os
from datetime import datetime
from app.services.mongodb import MongoDB
from .models.snapshot import FileSnapshot


class DataBase:
    def __init__(self):
        url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB_NAME")
        self._db = MongoDB(url, db_name)
        self.collection_name = "file_snapshot"
        self.user_profile_collection = "user_profile"

    def create_file_snapshot(self, snapshot_name, data, user_id):
        snapshot = FileSnapshot(
            name=snapshot_name,
            files=data,
            created=datetime.utcnow(),
            search_query=[],
            user_id=str(user_id),
        )
        self._db.insert_document(self.collection_name, snapshot.dict())

    def get_file_snapshot_names(self, user_id):
        query = {"user_id": str(user_id)}
        filter_query = {"name": 1, "created": 1, "_id": 0}
        snapshot_names = self._db.find_documents(
            self.collection_name, query, filter_query
        )
        return snapshot_names

    def get_file_under_folder(self, user_id, offset, limit, folder_id=None):
        query = {"files": {"$elemMatch": {}}}
        print(user_id)
        print(query)
        print(offset)
        print(limit)
        print(folder_id)

    def delete_file_snapshot(self, user_id, snapshot_name):
        query = {"user_id": str(user_id), "name": snapshot_name}
        self._db.delete_document(self.collection_name, query)

    def edit_file_snapshot_name(self, user_id, snapshot_name, new_snapshot_name):
        query = {"user_id": str(user_id), "name": snapshot_name}
        update = {"$set": {"name": new_snapshot_name}}
        self._db.update_document(self.collection_name, query, update)
