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
        snapshot = FileSnapshot(name=snapshot_name, files=data, created=datetime.utcnow(), search_query=[],
                                user_id=str(user_id))
        self._db.insert_document(self.collection_name, snapshot.dict())

    def get_file_snapshots(self, user_id, snapshot_name=None, name_only=False):
        query, filter_query = {}, {'_id': 0, 'user_id': 0}
        if snapshot_name:
            query = {"name": snapshot_name, "user_id": str(user_id)}
        if name_only:
            filter_query = {'name': 1, '_id': 0}
        print(filter_query)
        snapshot = self._db.find_documents(self.collection_name, query, filter_query)
        return snapshot
