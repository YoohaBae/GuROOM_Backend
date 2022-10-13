import os
from datetime import datetime
import copy
from app.services.mongodb import MongoDB
from .models.snapshot import FileSnapshot
from .models.files import File, Permission


class DataBase:
    def __init__(self, user_id: str):
        url = os.getenv("MONGO_URL")
        db_name = os.getenv("MONGO_DB_NAME")
        self._db = MongoDB(url, db_name)
        self.user_id = user_id

    def create_file_snapshot(self, snapshot_name, data, root_id):
        file_snapshot_collection_name = f"{self.user_id}.file_snapshots"
        snapshot = FileSnapshot(
            name=snapshot_name, created=datetime.utcnow(), root_id=root_id
        )
        self._db.insert_document(file_snapshot_collection_name, snapshot.dict())

        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        files = copy.deepcopy(data)
        files = [File(**file).dict() for file in files]
        self._db.insert_documents(file_collection_name, files)

        for file in data:
            file_id = file["id"]
            permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
            if "permissions" in file:
                permissions = []
                for permission in file["permissions"]:
                    permission["file_id"] = file_id
                    permissions.append(Permission(**permission).dict())
                self._db.insert_documents(permission_collection_name, permissions)

    def get_root_id(self, snapshot_name):
        file_snapshot_collection_name = f"{self.user_id}.file_snapshots"
        query = {"name": snapshot_name}
        filter_query = {"root_id": 1, "_id": 0}
        return self._db.find_document(
            file_snapshot_collection_name, query, filter_query
        )["root_id"]

    def get_file_snapshot_names(self):
        file_snapshot_collection_name = f"{self.user_id}.file_snapshots"
        filter_query = {"_id": 0}
        snapshot_names = self._db.find_documents(
            file_snapshot_collection_name, filter_query=filter_query
        )
        return snapshot_names

    def get_file_under_folder(
        self, snapshot_name, offset=None, limit=None, folder_id=None
    ):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"

        if folder_id:
            query = {"parents": {"$in": [folder_id]}}
        else:
            query = {"parents": {"$size": 0}}

        filter_query = {"_id": 0}
        files = self._db.find_documents(file_collection_name, query, filter_query)
        if offset is not None and limit is not None:
            return files[offset : (offset + limit)]  # noqa: E203
        return files

    def edit_file_snapshot_name(self, snapshot_name, new_snapshot_name):
        # change name in user_id.file_snapshots
        file_snapshot_collection_name = f"{self.user_id}.file_snapshots"
        query = {"name": snapshot_name}
        update_query = {"$set": {"name": new_snapshot_name}}
        self._db.update_document(file_snapshot_collection_name, update_query, query)

        # fix name of all collections under snapshot_name
        starts_with = f"{self.user_id}.{snapshot_name}"
        self.edit_all_collections_starting_with(starts_with, new_snapshot_name)

    def edit_all_collections_starting_with(self, query, new_snapshot_name):
        collections = self._db.get_collection_names()
        for collection in collections:
            if collection.startswith(query):
                # replace the second part of <>.<>
                collection_list = collection.split(".")
                collection_list[1] = new_snapshot_name
                new_collection_name = ".".join(collection_list)
                self._db.rename_collection(collection, new_collection_name)

    def delete_file_snapshot(self, snapshot_name):
        # delete file snapshot from user_id.file_snapshots
        file_snapshot_collection_name = f"{self.user_id}.file_snapshots"
        query = {"name": snapshot_name}
        self._db.delete_document(file_snapshot_collection_name, query)

        # delete files and permissions with snapshot_name
        starts_with = f"{self.user_id}.{snapshot_name}"
        self.delete_all_collections_starting_with(starts_with)

    def delete_all_collections_starting_with(self, query):
        collections = self._db.get_collection_names()
        for collection in collections:
            if collection.startswith(query):
                self._db.drop_collection(collection)

    def update_path_and_permissions(
        self, snapshot_name, folder_path, folder_permission, file_id
    ):
        new_path = self.update_path(snapshot_name, folder_path, file_id)
        new_permissions = self.update_permissions_to_inherit_direct(
            snapshot_name, folder_permission, folder_path, file_id
        )
        return new_path, new_permissions

    def update_permissions_to_inherit_direct(
        self, snapshot_name, parent_permissions, parent_path, file_id
    ):
        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        for parent_permission in parent_permissions:
            query = {"file_id": file_id, "id": parent_permission["id"]}
            if parent_permission["inherited"]:
                inherited_from = parent_permission["inherited_from"]
            else:
                inherited_from = parent_path
            update_query = {
                "$set": {"inherited": True, "inherited_from": inherited_from}
            }
            self._db.update_documents(permission_collection_name, update_query, query)
        query = {"file_id": file_id}
        permissions = self._db.find_documents(
            permission_collection_name, query, {"_id": 0}
        )
        return permissions

    def update_path(self, snapshot_name, folder_path, file_id):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        file_name = self.get_file_name(snapshot_name, file_id)
        new_path = folder_path + "/" + file_name
        query = {"id": file_id}
        update_query = {"$set": {"path": folder_path}}
        self._db.update_document(file_collection_name, update_query, query)
        return new_path

    def get_file_name(self, snapshot_name, file_id):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"id": file_id}
        filter_query = {"name": 1}
        file_name = self._db.find_document(file_collection_name, query, filter_query)
        return file_name["name"]

    def get_all_permission_of_file(self, snapshot_name, file_id):
        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        query = {"file_id": file_id}
        filter_query = {"_id": 0}
        permissions = self._db.find_documents(
            permission_collection_name, query, filter_query
        )
        return permissions

    def get_files_with_no_path(self, snapshot_name):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"path": None}
        filter_query = {"_id": 0}
        files = self._db.find_documents(file_collection_name, query, filter_query)
        return files

    def get_all_permission_of_snapshot(self, snapshot_name):
        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        filter_query = {"_id": 0}
        permissions = self._db.find_documents(
            permission_collection_name, filter_query=filter_query
        )
        return permissions

    def get_all_files_of_snapshot(self, snapshot_name):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        filter_query = {"_id": 0}
        files = self._db.find_documents(file_collection_name, filter_query=filter_query)
        return files
