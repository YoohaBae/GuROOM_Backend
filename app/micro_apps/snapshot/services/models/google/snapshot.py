from pydantic import BaseModel
from typing import List
from datetime import datetime


class SharedDrive(BaseModel):
    id: str
    name: str


class FileSnapshot(BaseModel):
    name: str
    created: datetime
    root_id: str = None
    shared_drives: List[SharedDrive] = []


class Membership(BaseModel):
    member: str
    email: str
    role: str
    join_date: str


class GroupMembershipsSnapshot(BaseModel):
    group_name: str
    group_email: str
    create_time: datetime
    memberships: List[Membership]
