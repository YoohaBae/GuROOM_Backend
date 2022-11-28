import json
import copy
import ast
from datetime import datetime
from app.utils.util import DateTimeEncoder
from app.services.snapshot_service import SnapshotService
from app.micro_apps.auth.services.dropbox.dropbox_auth import DropboxAuth
from app.micro_apps.auth.services.dropbox.database import DropboxAuthDatabase
from app.micro_apps.snapshot.services.dropbox.dropbox_drive import DropboxDrive
from app.micro_apps.snapshot.services.dropbox.analysis import DropboxAnalysis
from app.micro_apps.snapshot.services.dropbox.database import DropboxSnapshotDatabase
from app.micro_apps.snapshot.services.dropbox.query_builder import DropboxQueryBuilder
from app.micro_apps.snapshot.services.models.dropbox.files import Permission, File


class DropboxSnapshotService(SnapshotService):
    def __init__(self):
        super().__init__()

    def get_user_id_from_access_token(self, access_token):
        dropbox_auth = DropboxAuth()
        user_db = DropboxAuthDatabase()

        try:
            user = dropbox_auth.get_user(access_token)
            user_obj = user_db.get_user(user.email)
            user_id = str(user_obj["_id"])
            return user_id
        except Exception as error:
            self.logger.error(error)
            return None

    def get_user_email_from_token(self, access_token):
        dropbox_auth = DropboxAuth()

        try:
            user = dropbox_auth.get_user(access_token)
            return user.email
        except Exception as error:
            self.logger.error(error)
            return None

    def check_duplicate_file_snapshot_name(self, user_id, snapshot_name):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            duplicate = snapshot_db.check_duplicate_file_snapshot_name(snapshot_name)
            return duplicate
        except Exception as error:
            self.logger.error(error)
            return None

    def get_all_files_and_permissions_from_api(self, access_token, user_email):
        dropbox_drive = DropboxDrive()
        try:
            files, shared_folders, next_page_token = dropbox_drive.get_files(
                access_token
            )

            if files and shared_folders:
                # there are more files to be retrieved
                while next_page_token is not None:
                    (
                        new_files,
                        new_shared_folders,
                        next_page_token,
                    ) = dropbox_drive.get_files(access_token, next_page_token)
                    files += new_files
                    shared_folders += new_shared_folders
            elif files is None or shared_folders is None:
                raise ValueError("unable to retrieve files and shared folders")

            # separate file ids and folder ids
            file_ids = [file["id"] for file in files if file["mimeType"] == "file"]
            shared_folder_ids = [folder["driveId"] for folder in shared_folders]

            # get permissions of files
            file_permissions = dropbox_drive.get_permissions_of_files(
                access_token, file_ids
            )
            if file_permissions is None:
                raise ValueError("unable to retrieve file permissions")
            # get permissions of folders and shared folders
            shared_folder_permissions = dropbox_drive.get_permissions_of_shared_folders(
                access_token, shared_folder_ids
            )
            if shared_folder_permissions is None:
                raise ValueError("unable to retrieve folder permissions")

            owner_permission = {}
            for permission in file_permissions:
                if permission["emailAddress"] == user_email:
                    owner_permission = permission
                    break

            # give nested folders their inherited permissions
            nested_folder_permissions = []
            not_shared_folder_permissions = []
            for file in files:
                if file["mimeType"] == "folder":
                    if not file["shared"]:
                        if file["driveId"] is None:
                            new_permission = copy.deepcopy(owner_permission)
                            new_permission["file_id"] = file["id"]
                            not_shared_folder_permissions.append(new_permission)
                    for permission in shared_folder_permissions:
                        # give permission of shared folder to nested folder
                        if permission["driveId"] == file["driveId"]:
                            folder_permission = copy.deepcopy(permission)
                            folder_permission["file_id"] = file["id"]
                            folder_permission["inherited"] = True
                            nested_folder_permissions.append(folder_permission)

            for folder in shared_folders:
                for permission in shared_folder_permissions:
                    if permission["driveId"] == folder["driveId"]:
                        if not permission["file_id"]:
                            permission["file_id"] = folder["id"]
            all_files = [File(**file).dict() for file in files + shared_folders]
            all_permissions = [
                Permission(**permission).dict()
                for permission in file_permissions
                + shared_folder_permissions
                + nested_folder_permissions
                + not_shared_folder_permissions
            ]
            return all_files, all_permissions
        except Exception as error:
            self.logger.error(error)
            return None, None

    def create_file_snapshot(self, user_id, snapshot_name, files, permissions):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            snapshot_db.create_file_snapshot(snapshot_name, files, permissions)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def perform_inherit_direct_permission_analysis(self, user_id, snapshot_name):
        analysis = DropboxAnalysis(user_id)
        try:
            analysis.calculate_permission_and_path(snapshot_name)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def delete_file_snapshot(self, user_id, snapshot_name):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            snapshot_db.delete_file_snapshot(snapshot_name)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def edit_file_snapshot_name(self, user_id, snapshot_name, new_snapshot_name):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            snapshot_db.edit_file_snapshot_name(snapshot_name, new_snapshot_name)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def get_file_snapshot_names(self, user_id):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            data = snapshot_db.get_file_snapshot_names()
            if len(data) == 0:
                return data
            names = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return names
        except Exception as error:
            self.logger.error(error)
            return None

    def get_files_of_folder(
        self, user_id, snapshot_name, path=None, offset=None, limit=None
    ):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            data = snapshot_db.get_file_under_folder(snapshot_name, offset, limit, path)
            if len(data) == 0:
                return []
            files = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return files
        except Exception as error:
            self.logger.error(error)
            return None

    def get_permission_of_files(self, user_id, snapshot_name, files):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            permissions = []
            for file in files:
                permission = snapshot_db.get_all_permission_of_file(
                    snapshot_name, file["id"]
                )
                permissions.extend(permission)
            # group the permissions by the same file ids
            permission_grouped = self.group_permission_by_file_id(permissions)
            for file_id in permission_grouped.keys():
                # separate the permissions by inherit and direct permissions
                inherit, direct = self.separate_permission_to_inherit_and_direct(
                    permission_grouped[file_id]
                )
                permission_grouped[file_id] = {
                    "inherit_permissions": inherit,
                    "direct_permissions": direct,
                }
            return permission_grouped
        except Exception as error:
            self.logger.error(error)
            return None

    def get_files_with_diff_permission_from_folder(self, user_id, snapshot_name):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            all_files = snapshot_db.get_all_files_of_snapshot(snapshot_name)
            different_files = []
            # go through all files of snapshot
            for file in all_files:
                file_id = file["id"]
                file_path = file["path"]
                # if parent doesn't exist or the parent is MyDrive or any shared drive
                if len(file_path.split("/")) == 1:
                    continue
                # get the folder id
                folder_name = file_path.split("/")[-1]
                folder_id = snapshot_db.get_file_id_of_name(snapshot_name, folder_name)
                # get permission of file id
                file_permissions = snapshot_db.get_all_permission_of_file(
                    snapshot_name, file_id
                )
                # get permission of folder id
                folder_permissions = snapshot_db.get_all_permission_of_file(
                    snapshot_name, folder_id
                )
                # no folder with such id
                if folder_permissions is None:
                    continue
                # perform analysis
                analysis = DropboxAnalysis(user_id)
                (
                    base_more_permissions,
                    changes,
                    compare_more_permissions,
                ) = analysis.get_sharing_differences(
                    file_permissions, folder_permissions
                )
                # there is a difference
                if (
                    len(base_more_permissions) != 0
                    or len(changes) != 0
                    or len(compare_more_permissions) != 0
                ):
                    # append to different files
                    different_files.append(file)
            different_files = json.loads(
                json.dumps(different_files, cls=DateTimeEncoder)
            )
            return different_files
        except Exception as error:
            self.logger.error(error)
            return None

    def get_file_folder_sharing_difference(self, user_id, snapshot_name, file_id):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            # get the id of the parent(folder) of file
            folder_path = snapshot_db.get_path_of_file(snapshot_name, file_id)
            folder_name = folder_path.split("/")[-1]
            folder_id = snapshot_db.get_file_id_of_name(snapshot_name, folder_name)

            # compare the two files
            folder_more, changes, file_more = self.get_sharing_difference_of_two_files(
                user_id, snapshot_name, folder_id, file_id
            )
            return folder_more, changes, file_more
        except Exception as error:
            self.logger.error(error)
            return None

    def get_sharing_difference_of_two_files(
        self, user_id, snapshot_name, base_file_id, compare_file_id
    ):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            # get the permissions of the base file
            base_file_permissions = snapshot_db.get_all_permission_of_file(
                snapshot_name, base_file_id
            )
            # get the permissions of the compare file
            compare_file_permissions = snapshot_db.get_all_permission_of_file(
                snapshot_name, compare_file_id
            )
            # perform analysis
            analysis = DropboxAnalysis(user_id)
            (
                base_more_permissions,
                changes,
                compare_more_permissions,
            ) = analysis.get_sharing_differences(
                base_file_permissions, compare_file_permissions
            )
            return base_more_permissions, changes, compare_more_permissions
        except Exception as error:
            self.logger.error(error)
            return None

    def get_difference_of_two_snapshots(
        self, user_id, base_snapshot_name, compare_snapshot_name
    ):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            base_snapshot_files = snapshot_db.get_all_files_of_snapshot(
                base_snapshot_name
            )
            compare_snapshot_files = snapshot_db.get_all_files_of_snapshot(
                compare_snapshot_name
            )
            analysis = DropboxAnalysis(user_id)
            # compare the two file snapshots
            data = analysis.compare_two_file_snapshots(
                base_snapshot_name,
                compare_snapshot_name,
                base_snapshot_files,
                compare_snapshot_files,
            )
            # get the files that have different permissions or files that were newly created
            different_files = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return different_files
        except Exception as error:
            self.logger.error(error)
            return None

    def group_permission_by_file_id(self, permissions):
        permission_grouped = {}
        for permission in permissions:
            permission_grouped.setdefault(permission["file_id"], []).append(permission)
        return permission_grouped

    def separate_permission_to_inherit_and_direct(self, permissions):
        inherit = []
        direct = []
        for permission in permissions:
            if permission["inherited"]:
                inherit.append(permission)
            else:
                direct.append(permission)
        return inherit, direct

    def check_if_files_have_different_permission_from_folder(
        self, user_id, snapshot_name, file_ids
    ):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            all_files = snapshot_db.get_files_of_file_ids(snapshot_name, file_ids)
            # go through all files of snapshot
            for file in all_files:
                file_id = file["id"]
                file_path = file["path"]
                # if parent doesn't exist or the parent is MyDrive or any shared drive
                if len(file_path.split("/")) == 1:
                    continue
                # get the folder id
                folder_name = file_path.split("/")[-1]
                folder_id = snapshot_db.get_file_id_of_name(snapshot_name, folder_name)
                # get permission of file id
                file_permissions = snapshot_db.get_all_permission_of_file(
                    snapshot_name, file_id
                )
                # get permission of folder id
                folder_permissions = snapshot_db.get_all_permission_of_file(
                    snapshot_name, folder_id
                )
                # no folder with such id
                if folder_permissions is None:
                    continue
                # perform analysis
                analysis = DropboxAnalysis(user_id)
                (
                    base_more_permissions,
                    changes,
                    compare_more_permissions,
                ) = analysis.get_sharing_differences(
                    file_permissions, folder_permissions
                )
                # there is a difference
                if (
                    len(base_more_permissions) != 0
                    or len(changes) != 0
                    or len(compare_more_permissions) != 0
                ):
                    # append to different files
                    file["flag"] = True
            return all_files
        except Exception as error:
            self.logger.error(error)
            return None

    def process_query_search(self, user_id, email, snapshot_name, query: str):
        user_db = DropboxAuthDatabase()
        try:
            # retrieve file folder sharing different files
            if "is:file_folder_diff" in query:
                file_ids = ast.literal_eval(
                    query.split(" ")[2].replace("file_ids:", "")
                )
                if len(file_ids) == 0:
                    data = self.get_files_with_diff_permission_from_folder(
                        user_id,
                        snapshot_name,
                    )
                    different_files = json.loads(json.dumps(data, cls=DateTimeEncoder))
                    return different_files
                else:
                    files = self.check_if_files_have_different_permission_from_folder(
                        user_id, snapshot_name, file_ids
                    )
                    files = json.loads(json.dumps(files, cls=DateTimeEncoder))
                    return files
            # query access control requirement files
            elif "accessControl" in query:
                access_control_requirement_name = query.split(":")[1]
                # tagged files and permissions of access control requirement
                data = self.get_files_and_permissions_of_access_control_requirement(
                    user_id, email, snapshot_name, access_control_requirement_name
                )
                if data is None:
                    raise ValueError("unable to retrieve data")
                (
                    files,
                    permissions,
                ) = data
                files = json.loads(json.dumps(files, cls=DateTimeEncoder))
                # group the permissions by the same file ids
                permission_grouped = self.group_permission_by_file_id(permissions)
                for file_id in permission_grouped.keys():
                    # separate the permissions by inherit and direct permissions
                    inherit, direct = self.separate_permission_to_inherit_and_direct(
                        permission_grouped[file_id]
                    )
                    permission_grouped[file_id] = {
                        "inherit_permissions": inherit,
                        "direct_permissions": direct,
                    }
                return files, permission_grouped
            # query other files
            else:
                query_obj = {"search_time": datetime.utcnow(), "query": query}
                user_db.update_or_push_recent_queries(email, query_obj)
                query_builder = DropboxQueryBuilder(user_id, email, snapshot_name)
                data = query_builder.get_files_of_query(query)
                files = json.loads(json.dumps(data, cls=DateTimeEncoder))
                return files
        except Exception as error:
            self.logger.error(error)
            return None

    def validate_query(self, user_id, user_email, snapshot_name, query):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            if "is:file_folder_diff" in query:
                # file folder diff cannot have additional query statements
                if (
                    query.split(" ")[1] != "and"
                    or "file_ids" not in query.split(" ")[2]
                ):
                    raise ValueError(
                        "Invalid Query: invalid format of file folder sharing difference query"
                    )
            elif "accessControl:" in query:
                # access control requirement cannot have additional query statements
                access_control_query = query.split(":")
                if len(access_control_query) >= 3:
                    raise ValueError(
                        "Invalid Query: Access Control Requirements cannot be searched with other queries"
                    )
                # access control requirement
                access_control_requirement = snapshot_db.get_access_control_requirement(
                    access_control_query[1]
                )
                if access_control_requirement is None:
                    raise ValueError(
                        f"No Such Requirement: There is no access control requirement named :{access_control_query[1]}"
                    )
                # Q of access control requirement
                search_query = access_control_requirement["query"]
                query_builder = DropboxQueryBuilder(user_id, user_email, snapshot_name)
                query_builder.create_tree_and_validate(search_query)
            else:
                # validate queries
                query_builder = DropboxQueryBuilder(user_id, user_email, snapshot_name)
                query_builder.create_tree_and_validate(query)
        except Exception as error:
            message = error.args[0]
            return message
        return True

    def get_unique_members_of_file_snapshot(self, user_id, snapshot_name):
        # Used for autocompletion when querying
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            all_members = []
            # get all memberships from the file snapshot
            permission_members = snapshot_db.get_all_members_from_permissions(
                snapshot_name
            )
            all_members.extend(permission_members)
            # get the unique memberships and format them
            unique_group_members = list(
                {member["email"]: member for member in all_members}.values()
            )
            return unique_group_members
        except Exception as error:
            self.logger.error(error)
            return None

    def get_recent_queries(self, email):
        user_db = DropboxAuthDatabase()
        try:
            data = user_db.get_recent_queries(email)
            # sort the recent query by search time
            data.sort(key=lambda x: x["search_time"])
            # get only the 10 recent queries
            data = data[-10:]
            recent_queries = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return recent_queries
        except Exception as error:
            self.logger.error(error)
            return None

    def create_access_control_requirement(self, user_id, access_control):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            snapshot_db.create_access_control_requirement(access_control)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def check_duplicate_access_control_requirement(self, user_id, access_control):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            duplicate = snapshot_db.check_duplicate_access_control_requirement(
                access_control
            )
            return duplicate
        except Exception as error:
            self.logger.error(error)
            return None

    def get_access_control_requirements(self, user_id):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            access_control_requirements = snapshot_db.get_access_control_requirements()
            return access_control_requirements
        except Exception as error:
            self.logger.error(error)
            return None

    def get_files_and_permissions_of_access_control_requirement(
        self, user_id, email, snapshot_name, access_control_requirement_name
    ):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        analysis = DropboxAnalysis(user_id)
        try:
            access_control_requirement = snapshot_db.get_access_control_requirement(
                access_control_requirement_name
            )
            query = access_control_requirement["query"]
            query_builder = DropboxQueryBuilder(user_id, email, snapshot_name)
            # query_builder.is_groups = access_control_requirement["Grp"]
            # file of query
            data = query_builder.get_files_of_query(query)
            files = json.loads(json.dumps(data, cls=DateTimeEncoder))
            # include field violation: bool => whether file has violated the access control requirement
            (
                tagged_files,
                tagged_permissions,
            ) = analysis.tag_files_and_permissions_with_violation(
                snapshot_name, files, access_control_requirement
            )
            return tagged_files, tagged_permissions
        except Exception as error:
            self.logger.error(error)
            return None

    def delete_access_control_requirement(self, user_id, access_control_name):
        snapshot_db = DropboxSnapshotDatabase(user_id)
        try:
            snapshot_db.delete_access_control_requirement(access_control_name)
            return True
        except Exception as error:
            self.logger.error(error)
            return False
