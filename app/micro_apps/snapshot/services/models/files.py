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
    kind: str
    displayName: str
    me: bool
    permissionId: str
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
    inheritedFrom: str
    inherited: bool


class Permission(BaseModel):
    kind: str
    id: Optional[str]
    type: Optional[str]
    emailAddress: Optional[str]
    domain: Optional[str]
    role: Optional[str]
    allowFileDiscovery: Optional[bool]
    displayName: Optional[str]
    permissionDetails: Optional[List[PermissionDetail]] = []
    deleted: Optional[bool]
    pendingOwner: Optional[bool]


class Capabilities(BaseModel):
    canComment: bool
    canEdit: bool
    canShare: bool


class Restriction(BaseModel):
    readOnly: bool
    reason: Optional[str]
    restrictingUser: Optional[RestrictUser]


class File(BaseModel):
    kind: str
    id: str
    name: str
    parents: Optional[List[str]] = []
    spaces: Optional[List[str]] = []
    createdTime: datetime
    modifiedTime: datetime
    sharedWithMeTime: Optional[datetime]
    sharingUser: Optional[SharingUser]
    owners: Optional[List[Permission]] = []
    driveId: Optional[str]
    shared: Optional[bool]
    ownedByMe: Optional[bool]
    capabilities: Capabilities
    permissions: Optional[List[Permission]] = []
    permissionIds: Optional[List[str]] = []
    fullFileExtension: Optional[str]
    fileExtension: Optional[str]
    size: Optional[str]
    contentRestrictions: Optional[List[Restriction]] = []
