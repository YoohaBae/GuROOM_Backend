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

    def create_file_snapshot(self, snapshot_name, root_id, data, user_id):
        snapshot = FileSnapshot(
            name=snapshot_name,
            files=data,
            created=datetime.utcnow(),
            search_query=[],
            root_id=root_id,
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

    def get_file_under_folder(
        self, user_id, snapshot_name, offset, limit, folder_id=None
    ):
        pipeline = [
            {"$match": {"name": snapshot_name, "user_id": str(user_id)}},
            {"$limit": 1},
            {
                "$unwind": {
                    "path": "$files",
                    "includeArrayIndex": "file_id",
                    "preserveNullAndEmptyArrays": True,
                }
            },
        ]
        if folder_id:
            file_parent_match = {
                "$match": {"files.parents": {"$in": ["0AKSNHh_CP_ChUk9PVA"]}}
            }
        else:
            file_parent_match = {"$match": {"files.parents": {"$size": 0}}}
        pipeline.append(file_parent_match)
        pipeline.extend([{"$project": {"files": 1}}, {"$unset": "_id"}])
        files = self._db.aggregate_documents(self.collection_name, pipeline)
        return files[offset : (offset + limit)]  # noqa: E203

    def get_root_id(self, user_id, snapshot_name):
        query = {"user_id": str(user_id), "name": snapshot_name}
        return self._db.find_document(self.collection_name, query)["root_id"]

    def delete_file_snapshot(self, user_id, snapshot_name):
        query = {"user_id": str(user_id), "name": snapshot_name}
        self._db.delete_document(self.collection_name, query)

    def edit_file_snapshot_name(self, user_id, snapshot_name, new_snapshot_name):
        query = {"user_id": str(user_id), "name": snapshot_name}
        update = {"$set": {"name": new_snapshot_name}}
        self._db.update_document(self.collection_name, query, update)
