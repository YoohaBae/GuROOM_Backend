import os
from datetime import datetime
from app.services.mongodb import MongoDB
from .models.snapshot import FileSnapshot


class DataBase:
    def __init__(self, user_id: str):
        url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB_NAME")
        self._db = MongoDB(url, db_name)
        self.collection_name = "file_snapshot"
        self.user_id = user_id

    def create_file_snapshot(self, snapshot_name, root_id, data):
        snapshot = FileSnapshot(
            name=snapshot_name,
            files=data,
            created=datetime.utcnow(),
            search_query=[],
            root_id=root_id,
            user_id=self.user_id,
        )
        self._db.insert_document(self.collection_name, snapshot.dict())

    def get_file_snapshot_names(self):
        query = {"user_id": self.user_id}
        filter_query = {"name": 1, "created": 1, "_id": 0}
        snapshot_names = self._db.find_documents(
            self.collection_name, query, filter_query
        )
        return snapshot_names

    def get_file_under_folder(
        self, snapshot_name, offset=None, limit=None, folder_id=None
    ):
        pipeline = [
            {"$match": {"name": snapshot_name, "user_id": self.user_id}},
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
            file_parent_match = {"$match": {"files.parents": {"$in": [folder_id]}}}
        else:
            file_parent_match = {"$match": {"files.parents": {"$size": 0}}}
        pipeline.append(file_parent_match)
        pipeline.extend([{"$project": {"files": 1}}, {"$unset": "_id"}])
        files = self._db.aggregate_documents(self.collection_name, pipeline)
        if offset and limit:
            return files[offset : (offset + limit)]  # noqa: E203
        return files

    def get_root_id(self, snapshot_name):
        query = {"user_id": self.user_id, "name": snapshot_name}
        return self._db.find_document(self.collection_name, query)["root_id"]

    def delete_file_snapshot(self, snapshot_name):
        query = {"user_id": self.user_id, "name": snapshot_name}
        self._db.delete_document(self.collection_name, query)

    def edit_file_snapshot_name(self, snapshot_name, new_snapshot_name):
        query = {"user_id": self.user_id, "name": snapshot_name}
        update = {"$set": {"name": new_snapshot_name}}
        self._db.update_document(self.collection_name, query, update)

    def get_file_permission_and_name(self, snapshot_name, file_id):
        pipeline = [
            {"$match": {"name": snapshot_name, "user_id": self.user_id}},
            {"$limit": 1},
            {
                "$unwind": {
                    "path": "$files",
                    "includeArrayIndex": "file_id",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {"$match": {"files.id": file_id}},
            {"$project": {"files.name": 1, "files.permissions": 1}},
            {"$limit": 1},
            {"$unset": "_id"},
        ]
        files = self._db.aggregate_documents(self.collection_name, pipeline)
        return files

    def update_inherited_permission_and_path(
        self, snapshot_name, file_id, parent_path, parent_permissions
    ):
        files = self.get_snapshot(snapshot_name)["files"]
        new_path, new_permissions = None, None
        for file in files:
            if file["id"] == file_id:
                new_path = parent_path + "/" + file["name"]
                new_permissions = self.calculate_inherit_permissions(
                    file["permissions"], parent_permissions, parent_path
                )
                file["path"] = new_path
                file["permissions"] = new_permissions

        query = {"name": snapshot_name, "user_id": self.user_id}
        update = {"$set": {"files": files}}
        self._db.update_document(self.collection_name, query, update)
        return new_path, new_permissions

    def get_snapshot(self, snapshot_name):
        query = {"name": snapshot_name, "user_id": self.user_id}
        snapshot = self._db.find_document(self.collection_name, query)
        return snapshot

    def calculate_inherit_permissions(
        self, permissions, parent_permissions, parent_path
    ):
        for parent_permission in parent_permissions:
            index = next(
                (
                    index
                    for (index, permission) in enumerate(permissions)
                    if permission["id"] == parent_permission["id"]
                )
            )
            if index:
                permissions[index]["inherited"] = True
                if "inherited" in parent_permission:
                    permissions[index]["inherited_from"] = parent_permission[
                        "inherited_from"
                    ]
                permissions[index]["inherited_from"] = parent_path
        return permissions
