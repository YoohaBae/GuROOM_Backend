import json
import ast
from bs4 import BeautifulSoup
from datetime import datetime
from app.utils.util import DateTimeEncoder
from app.services.snapshot_service import SnapshotService
from app.micro_apps.auth.services.google.google_auth import GoogleAuth
from app.micro_apps.auth.services.google.database import GoogleAuthDatabase
from app.micro_apps.snapshot.services.google.google_drive import GoogleDrive
from app.micro_apps.snapshot.services.google.analysis import GoogleAnalysis
from app.micro_apps.snapshot.services.google.database import GoogleSnapshotDatabase
from app.micro_apps.snapshot.services.google.query_builder import GoogleQueryBuilder


class GoogleSnapshotService(SnapshotService):
    def __init__(self):
        super().__init__()

    def get_user_id_from_access_token(self, access_token):
        google_auth = GoogleAuth()
        user_db = GoogleAuthDatabase()

        try:
            user = google_auth.get_user(access_token)
            user_obj = user_db.get_user(user.email)
            user_id = str(user_obj["_id"])
            return user_id
        except Exception as error:
            self.logger.error(error)
            return None

    def get_user_email_from_token(self, access_token):
        google_auth = GoogleAuth()

        try:
            user = google_auth.get_user(access_token)
            return user.email
        except Exception as error:
            self.logger.error(error)
            return None

    def check_duplicate_file_snapshot_name(self, user_id, snapshot_name):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            duplicate = snapshot_db.check_duplicate_file_snapshot_name(snapshot_name)
            return duplicate
        except Exception as error:
            self.logger.error(error)
            return None

    def get_root_id_from_api(self, access_token):
        google_drive = GoogleDrive()
        try:
            # get the id of MyDrive
            root_id = google_drive.get_root_file_id(access_token)
            return root_id
        except Exception as error:
            self.logger.error(error)
            return None

    def get_all_shared_drives_from_api(self, access_token):
        google_drive = GoogleDrive()
        try:
            drives, next_page_token = google_drive.get_shared_drives(access_token)

            if drives:
                # there are more shared drives to be retrieved
                while next_page_token is not None:
                    new_drives, next_page_token = google_drive.get_shared_drives(
                        access_token, next_page_token
                    )
                    drives += new_drives
            return drives
        except Exception as error:
            self.logger.error(error)
            return None

    def get_all_files_from_api(self, access_token):
        google_drive = GoogleDrive()
        try:
            files, next_page_token = google_drive.get_files(access_token)

            if files:
                # there are more files to be retrieved
                while next_page_token is not None:
                    new_files, next_page_token = google_drive.get_files(
                        access_token, next_page_token
                    )
                    files += new_files
            for file in files:
                shared_drive_permissions_for_file = []
                # separate result into file and permission
                if (
                    "driveId" in file
                    and file["driveId"] is not None
                    and "permissionIds" in file
                    and "permissionIds" != []
                ):
                    permission_ids = file["permissionIds"]
                    for pid in permission_ids:
                        # shared drive permissions must be retrieved separately by a different api request
                        permission = (
                            google_drive.get_permission_detail_of_shared_drive_file(
                                access_token, file["id"], pid
                            )
                        )
                        shared_drive_permissions_for_file.append(permission)
                    file["permissions"] = shared_drive_permissions_for_file
            return files
        except Exception as error:
            self.logger.error(error)
            return None

    def create_file_snapshot(
        self, user_id, snapshot_name, files, root_id, shared_drives
    ):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            snapshot_db.create_file_snapshot(
                snapshot_name, files, root_id, shared_drives
            )
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def perform_inherit_direct_permission_analysis(self, user_id, snapshot_name):
        analysis = GoogleAnalysis(user_id)
        try:
            analysis.calculate_permission_and_path(snapshot_name)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def delete_file_snapshot(self, user_id, snapshot_name):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            snapshot_db.delete_file_snapshot(snapshot_name)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def edit_file_snapshot_name(self, user_id, snapshot_name, new_snapshot_name):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            snapshot_db.edit_file_snapshot_name(snapshot_name, new_snapshot_name)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def get_file_snapshot_names(self, user_id):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            data = snapshot_db.get_file_snapshot_names()
            if len(data) == 0:
                return data
            names = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return names
        except Exception as error:
            self.logger.error(error)
            return None

    def get_files_of_my_drive(self, user_id, snapshot_name, offset=None, limit=None):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            # get the id of MyDrive
            folder_id = snapshot_db.get_root_id(snapshot_name)
            # get files under MyDrive
            data = snapshot_db.get_file_under_folder(
                snapshot_name, offset, limit, folder_id
            )
            if len(data) == 0:
                return []
            files = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return files
        except Exception as error:
            self.logger.error(error)
            return None

    def get_files_of_shared_with_me(
        self, user_id, snapshot_name, offset=None, limit=None
    ):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            # get all files with no parent attribute
            no_parent = snapshot_db.get_file_under_folder(snapshot_name)
            # get all files that do not have a path attribute -> has a parent but that parent is not in snapshot
            no_path = snapshot_db.get_files_with_no_path(snapshot_name)
            yes_path = []
            # set the files with no path as shared with me
            for no_path_file in no_path:
                no_path_file["path"] = "/SharedWithMe"
                yes_path.append(no_path_file)
            data = yes_path + no_parent
            # slice data
            if offset is not None and limit is not None:
                data = data[offset : (offset + limit)]  # noqa: E203
            if len(data) == 0:
                return []
            files = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return files
        except Exception as error:
            self.logger.error(error)
            return None

    def get_files_of_shared_drive(
        self, user_id, snapshot_name, drive_id, offset=None, limit=None
    ):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            data = snapshot_db.get_file_under_folder(
                snapshot_name, offset, limit, drive_id
            )
            if len(data) == 0:
                return []
            files = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return files
        except Exception as error:
            self.logger.error(error)
            return None

    def get_files_of_folder(
        self, user_id, snapshot_name, folder_id, offset=None, limit=None
    ):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            data = snapshot_db.get_file_under_folder(
                snapshot_name, offset, limit, folder_id
            )
            if len(data) == 0:
                return []
            files = json.loads(json.dumps(data, cls=DateTimeEncoder))
            return files
        except Exception as error:
            self.logger.error(error)
            return None

    def get_permission_of_files(self, user_id, snapshot_name, files):
        snapshot_db = GoogleSnapshotDatabase(user_id)
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

    def check_if_files_have_different_permission_from_folder(
        self, user_id, snapshot_name, file_ids
    ):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            all_files = snapshot_db.get_files_of_file_ids(snapshot_name, file_ids)

            root_id = snapshot_db.get_root_id(snapshot_name)
            shared_drives = snapshot_db.get_shared_drives(snapshot_name)
            shared_drive_ids = [x["id"] for x in shared_drives]
            # go through all files of snapshot
            for file in all_files:
                file_id = file["id"]
                parents = file["parents"]
                # if parent doesn't exist or the parent is MyDrive or any shared drive
                if (
                    len(parents) == 0
                    or parents[0] == root_id
                    or parents[0] in shared_drive_ids
                ):
                    continue
                # get the folder id
                folder_id = parents[0]
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
                analysis = GoogleAnalysis(user_id)
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

    def get_files_with_diff_permission_from_folder(self, user_id, snapshot_name):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            all_files = snapshot_db.get_all_files_of_snapshot(snapshot_name)
            different_files = []
            root_id = snapshot_db.get_root_id(snapshot_name)
            shared_drives = snapshot_db.get_shared_drives(snapshot_name)
            shared_drive_ids = [x["id"] for x in shared_drives]
            # go through all files of snapshot
            for file in all_files:
                file_id = file["id"]
                parents = file["parents"]
                # if parent doesn't exist or the parent is MyDrive or any shared drive
                if (
                    len(parents) == 0
                    or parents[0] == root_id
                    or parents[0] in shared_drive_ids
                ):
                    continue
                # get the folder id
                folder_id = parents[0]
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
                analysis = GoogleAnalysis(user_id)
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
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            # get the id of the parent(folder) of file
            folder_id = snapshot_db.get_parent_id(snapshot_name, file_id)
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
        snapshot_db = GoogleSnapshotDatabase(user_id)
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
            analysis = GoogleAnalysis(user_id)
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
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            base_snapshot_files = snapshot_db.get_all_files_of_snapshot(
                base_snapshot_name
            )
            compare_snapshot_files = snapshot_db.get_all_files_of_snapshot(
                compare_snapshot_name
            )
            analysis = GoogleAnalysis(user_id)
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

    def get_shared_drives(self, user_id, snapshot_name):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            shared_drives = snapshot_db.get_shared_drives(snapshot_name)
            return shared_drives
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

    async def scratch_group_memberships_from_file(self, file):
        try:
            # class for membership row div
            MEMBERSHIP_ROW_CLASS = "cXEmmc B9Uude hFgAsc J6Lkdb"
            # class for membership name div
            MEMBERSHIP_NAME_CLASS = "LnLepd"
            # class for membership email div
            MEMBERSHIP_EMAIL_CLASS = "p480bb Sq3iG"
            # class for membership role div
            MEMBERSHIP_ROLE_CLASS = "y7VPke"
            # class for membership join date div
            MEMBERSHIP_JOIN_DATE_CLASS = "y7VPke"
            memberships = []
            await file.seek(0)
            html = await file.read()
            # BeautifulSoup: An html parser that goes through the html file.
            # Can retrieve certain elements based on tags, classes, and ids.
            soup = BeautifulSoup(html, "html.parser")
            # find all membership rows
            membership_html_rows = soup.find_all("div", {"class": MEMBERSHIP_ROW_CLASS})
            for membership_html in membership_html_rows:
                membership_html_member = membership_html.find_all(
                    "span", {"class": "eois5"}
                )
                # email doesn't exist -> external groups
                if len(membership_html_member) == 3:
                    [
                        membership_html_name,
                        membership_html_role,
                        membership_html_join_date,
                    ] = membership_html_member
                    name = membership_html_name.find(
                        "div", {"class": MEMBERSHIP_NAME_CLASS}
                    ).contents[0]
                    role = membership_html_role.find(
                        "div", {"class": MEMBERSHIP_ROLE_CLASS}
                    ).contents[0]
                    join_date = membership_html_join_date.find(
                        "div", {"class": MEMBERSHIP_JOIN_DATE_CLASS}
                    ).contents[0]
                    if "@" in name:
                        email = name
                        membership = {
                            "member": name,
                            "email": email,
                            "role": role,
                            "join_date": join_date,
                        }
                        memberships.append(membership)
                # emails exist -> internal groups
                else:
                    [
                        membership_html_name,
                        membership_html_email,
                        membership_html_role,
                        membership_html_join_date,
                    ] = membership_html_member
                    name = membership_html_name.find(
                        "div", {"class": MEMBERSHIP_NAME_CLASS}
                    ).contents[0]
                    email = membership_html_email.find(
                        "a", {"class": MEMBERSHIP_EMAIL_CLASS}
                    ).contents[0]
                    role = membership_html_role.find(
                        "div", {"class": MEMBERSHIP_ROLE_CLASS}
                    ).contents[0]
                    join_date = membership_html_join_date.find(
                        "div", {"class": MEMBERSHIP_JOIN_DATE_CLASS}
                    ).contents[0]
                    membership = {
                        "member": name,
                        "email": email,
                        "role": role,
                        "join_date": join_date,
                    }
                    memberships.append(membership)
            return memberships
        except Exception as error:
            self.logger.error(error)
            return None

    def create_group_snapshot(
        self, user_id, group_name, group_email, create_time, memberships
    ):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            snapshot_db.create_group_memberships_snapshot(
                group_name, group_email, create_time, memberships
            )
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def get_recent_group_membership_snapshots(self, user_id):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            recent_groups = snapshot_db.get_recent_group_membership_snapshots()
            json_result_groups = json.loads(
                json.dumps(recent_groups, cls=DateTimeEncoder)
            )
            return json_result_groups
        except Exception as error:
            self.logger.error(error)
            return False

    def process_query_search(
        self, user_id, email, snapshot_name, query: str, is_groups=True
    ):
        user_db = GoogleAuthDatabase()
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
                query_builder = GoogleQueryBuilder(user_id, email, snapshot_name)
                query_builder.is_groups = is_groups
                data = query_builder.get_files_of_query(query)
                files = json.loads(json.dumps(data, cls=DateTimeEncoder))
                return files
        except Exception as error:
            self.logger.error(error)
            return None

    def validate_query(self, user_id, user_email, snapshot_name, query):
        snapshot_db = GoogleSnapshotDatabase(user_id)
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
                query_builder = GoogleQueryBuilder(user_id, user_email, snapshot_name)
                query_builder.create_tree_and_validate(search_query)
            else:
                # validate queries
                query_builder = GoogleQueryBuilder(user_id, user_email, snapshot_name)
                query_builder.create_tree_and_validate(query)
        except Exception as error:
            message = error.args[0]
            return message
        return True

    def get_unique_members_of_file_snapshot(self, user_id, snapshot_name, is_groups):
        # Used for autocompletion when querying
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            all_members = []
            # if groups toggle button was set to True get all group memberships
            # from all recent group membership snapshots
            if is_groups:
                recent_group_membership_snapshots = (
                    self.get_recent_group_membership_snapshots(user_id)
                )
                for group in recent_group_membership_snapshots:
                    all_members.extend(group["memberships"])
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
        user_db = GoogleAuthDatabase()
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
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            snapshot_db.create_access_control_requirement(access_control)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def check_duplicate_access_control_requirement(self, user_id, access_control):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            duplicate = snapshot_db.check_duplicate_access_control_requirement(
                access_control
            )
            return duplicate
        except Exception as error:
            self.logger.error(error)
            return None

    def get_access_control_requirements(self, user_id):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            access_control_requirements = snapshot_db.get_access_control_requirements()
            return access_control_requirements
        except Exception as error:
            self.logger.error(error)
            return None

    def get_files_and_permissions_of_access_control_requirement(
        self, user_id, email, snapshot_name, access_control_requirement_name
    ):
        snapshot_db = GoogleSnapshotDatabase(user_id)
        analysis = GoogleAnalysis(user_id)
        try:
            access_control_requirement = snapshot_db.get_access_control_requirement(
                access_control_requirement_name
            )
            # query of access control requirement
            query = access_control_requirement["query"]
            query_builder = GoogleQueryBuilder(user_id, email, snapshot_name)
            query_builder.is_groups = access_control_requirement["Grp"]
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
        snapshot_db = GoogleSnapshotDatabase(user_id)
        try:
            snapshot_db.delete_access_control_requirement(access_control_name)
            return True
        except Exception as error:
            self.logger.error(error)
            return False
