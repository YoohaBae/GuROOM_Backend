from datetime import datetime
from app.services.snapshot_database import SnapshotDatabase
from app.micro_apps.snapshot.services.models.dropbox.dropbox_types import (
    folder_mime_type,
)
from app.micro_apps.snapshot.services.models.google.snapshot import FileSnapshot


class DropboxSnapshotDatabase(SnapshotDatabase):
    def __init__(self, user_id):  # pragma: no cover
        super().__init__(user_id)

    def create_file_snapshot(self, snapshot_name, files, permissions):
        file_snapshot_collection_name = f"{self.user_id}.file_snapshots"
        # create model for file snapshot
        snapshot = FileSnapshot(name=snapshot_name, created=datetime.utcnow())
        # insert file snapshot in database
        self._db.insert_document(file_snapshot_collection_name, snapshot.dict())

        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        self._db.insert_documents(file_collection_name, files)

        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        self._db.insert_documents(permission_collection_name, permissions)

    def get_file_snapshot_names(self):
        file_snapshot_collection_name = f"{self.user_id}.file_snapshots"
        filter_query = {"_id": 0}
        snapshot_names = self._db.find_documents(
            file_snapshot_collection_name, filter_query=filter_query
        )
        return snapshot_names

    def get_file_under_folder(self, snapshot_name, offset=None, limit=None, path=None):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        if path is None:
            path = ""
        query = {"path": path}
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

    def update_permissions(
        self, snapshot_name, folder_path, folder_permission, file_id
    ):
        new_permissions = self.update_inherited_from_permissions(
            snapshot_name, folder_permission, folder_path, file_id
        )
        return new_permissions

    def update_inherited_from_permissions(
        self, snapshot_name, parent_permissions, parent_path, file_id
    ):
        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        for parent_permission in parent_permissions:
            query = {"file_id": file_id, "id": parent_permission["id"]}
            # parent permission was also inherited => get the inherited value
            if parent_permission["inherited"]:
                inherited_from = parent_permission["inherited_from"]
            # parent permission was not inherited
            else:
                inherited_from = parent_path
            update_query = {"$set": {"inherited_from": inherited_from}}
            self._db.update_documents(permission_collection_name, update_query, query)
        query = {"file_id": file_id}
        permissions = self._db.find_documents(
            permission_collection_name, query, {"_id": 0}
        )
        return permissions

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

    # def get_parent_id(self, snapshot_name, file_id):
    #     file_collection_name = f"{self.user_id}.{snapshot_name}.files"
    #     query = {"id": file_id}
    #     filter_query = {"_id": 0, "parents": 1}
    #     parent_id = self._db.find_document(file_collection_name, query, filter_query)[
    #         "parents"
    #     ][0]
    #     return parent_id

    def get_path_of_file(self, snapshot_name, file_id):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"id": file_id}
        filter_query = {"_id": 0, "path": 1}
        path_of_file = self._db.find_document(file_collection_name, query, filter_query)
        if path_of_file is not None:
            return path_of_file["path"]

        if path_of_file is None:
            raise ValueError("path of file cannot be calculated")

    # def update_inherited_and_inherited_from(
    #         self, snapshot_name, file_id, permission_id, inherited, inherited_from
    # ):
    #     permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
    #     query = {"id": permission_id, "file_id": file_id}
    #     update_query = {
    #         "$set": {"inherited": inherited, "inherited_from": inherited_from}
    #     }
    #     self._db.update_document(permission_collection_name, update_query, query)

    def get_all_members_from_permissions(self, snapshot_name):
        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        filter_query = {"_id": 0, "emailAddress": 1, "displayName": 1, "domain": 1}
        raw_members = self._db.find_documents(
            permission_collection_name, filter_query=filter_query
        )
        formatted_members = []
        for member in raw_members:
            if member["displayName"] is None:
                member["displayName"] = member["emailAddress"]
            elif member["emailAddress"] is None and member["domain"]:
                member["emailAddress"] = member["domain"]
            formatted_member = {
                "email": member["emailAddress"],
                "name": member["displayName"],
            }
            formatted_members.append(formatted_member)
        return formatted_members

    def get_files_with_path_regex(self, snapshot_name, path):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"path": {"$regex": path}}
        filter_query = {"_id": 0}
        files = self._db.find_documents(file_collection_name, query, filter_query)
        return files

    def get_files_that_match_file_name_regex(self, snapshot_name, file_name):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"name": {"$regex": file_name}}
        filter_query = {"_id": 0}
        files = self._db.find_documents(file_collection_name, query, filter_query)
        return files

    def get_file_id_of_name(self, snapshot_name, file_name):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"name": file_name}
        filter_query = {"_id": 0}
        files = self._db.find_document(file_collection_name, query, filter_query)
        return files["id"]

    def get_files_with_certain_role(self, snapshot_name, role_name, email):
        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        query = {"role": role_name, "emailAddress": email}
        filter_query = {"_id": 0, "file_id": 1}
        files = self._db.find_documents(permission_collection_name, query, filter_query)
        file_ids = [f["file_id"] for f in files]
        unique_file_ids = [*set(file_ids)]
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"id": {"$in": unique_file_ids}}
        filter_query = {"_id": 0}
        files = self._db.find_documents(file_collection_name, query, filter_query)
        return files

    def get_folders_with_regex(self, snapshot_name, folder_name):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"name": {"$regex": folder_name}, "mimeType": folder_mime_type}
        filter_query = {"_id": 0, "id": 1, "name": 1, "path": 1}
        folders = self._db.find_documents(file_collection_name, query, filter_query)
        return folders

    def get_directly_shared_permissions_file_ids(self, snapshot_name, email):
        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        query = {"emailAddress": email, "inherited": False, "role": {"$ne": "owner"}}
        filter_query = {"_id": 0, "file_id": 1}
        files = self._db.find_documents(permission_collection_name, query, filter_query)
        file_ids = [f["file_id"] for f in files]
        return file_ids

    # def get_files_with_sharing_user(self, snapshot_name, email):
    #     file_collection_name = f"{self.user_id}.{snapshot_name}.files"
    #     query = {"sharingUser.emailAddress": email}
    #     filter_query = {"_id": 0}
    #     files = self._db.find_documents(file_collection_name, query, filter_query)
    #     return files

    def get_files_of_file_ids(self, snapshot_name, file_ids):
        file_collection_name = f"{self.user_id}.{snapshot_name}.files"
        query = {"id": {"$in": file_ids}}
        filter_query = {"_id": 0}
        files = self._db.find_documents(file_collection_name, query, filter_query)
        return files

    def get_file_ids_shared_with_users_from_domain(self, snapshot_name, domain):
        permission_collection_name = f"{self.user_id}.{snapshot_name}.permissions"
        query = {"emailAddress": {"$regex": domain}, "role": {"$ne": "owner"}}
        filter_query = {"_id": 0, "file_id": 1}
        files = self._db.find_documents(permission_collection_name, query, filter_query)
        file_ids = [f["file_id"] for f in files]
        return file_ids

    def get_not_shared_files(self, snapshot_name):
        all_files = self.get_all_files_of_snapshot(snapshot_name)
        not_shared_files = []
        for file in all_files:
            permission = self.get_all_permission_of_file(snapshot_name, file["id"])
            if len(permission) == 0:
                not_shared_files.append(file)
        return not_shared_files

    def create_access_control_requirement(self, access_control):
        access_control_requirement_collection_name = (
            f"{self.user_id}.access_control_requirements"
        )
        self._db.insert_document(
            access_control_requirement_collection_name, access_control.dict()
        )

    def get_access_control_requirements(self):
        access_control_requirement_collection_name = (
            f"{self.user_id}.access_control_requirements"
        )
        query = {}
        filter_query = {"_id": 0}
        access_controls = self._db.find_documents(
            access_control_requirement_collection_name, query, filter_query
        )
        return access_controls

    def check_duplicate_access_control_requirement(self, access_control):
        access_control_requirement_collection_name = (
            f"{self.user_id}.access_control_requirements"
        )
        query = {
            "query": access_control.query,
            "AR": access_control.AR,
            "AW": access_control.AW,
            "DR": access_control.DR,
            "DW": access_control.DW,
            "Grp": access_control.Grp,
        }
        access_control = self._db.find_document(
            access_control_requirement_collection_name, query
        )
        if access_control is None:
            return False
        return True

    def get_access_control_requirement(self, access_control_requirement_name):
        access_control_requirement_collection_name = (
            f"{self.user_id}.access_control_requirements"
        )
        query = {"name": access_control_requirement_name}
        filter_query = {"_id": 0}
        access_control = self._db.find_document(
            access_control_requirement_collection_name, query, filter_query
        )
        return access_control
