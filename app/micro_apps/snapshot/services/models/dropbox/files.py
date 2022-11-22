from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SharingUser(BaseModel):
    kind: str
    displayName: str
    me: bool
    permissionId: str
    emailAddress: Optional[str]


class Owner(BaseModel):
    kind: Optional[str]
    displayName: Optional[str]
    me: Optional[bool]
    permissionId: Optional[str]
    emailAddress: Optional[str]


class RestrictUser(BaseModel):
    kind: str
    displayName: str
    me: bool
    permissionId: str
    emailAddress: str


class PermissionDetail(BaseModel):
    permissionType: str
    role: str
    inheritedFrom: Optional[str]
    inherited: bool


class Permission(BaseModel):
    id: Optional[str]
    type: Optional[str]
    emailAddress: Optional[str]
    domain: Optional[str]
    role: Optional[str]
    allowFileDiscovery: Optional[bool]
    displayName: Optional[str]
    photoLink: Optional[str]
    permissionDetails: Optional[List[PermissionDetail]] = []
    deleted: Optional[bool]
    pendingOwner: Optional[bool]
    inherited: bool = False
    inherited_from: str = None
    file_id: Optional[str] = None


class File(BaseModel):
    mimeType: str  # whether type is file or folder
    id: str
    name: str
    parents: Optional[List[str]] = []
    modifiedTime: Optional[datetime]
    # sharedWithMeTime: Optional[datetime]
    # sharingUser: Optional[SharingUser]
    # owners: Optional[List[Owner]] = []
    driveId: str = None
    shared: Optional[bool]
    # ownedByMe: Optional[bool]
    size: Optional[int]
    path: str = None
