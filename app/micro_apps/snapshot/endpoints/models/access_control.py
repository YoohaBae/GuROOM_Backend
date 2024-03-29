from pydantic import BaseModel
from typing import List


class AccessControlBody(BaseModel):
    name: str
    query: str
    AR: List[str] = []
    AW: List[str] = []
    DR: List[str] = []
    DW: List[str] = []
    Grp: bool


class DropboxAccessControlBody(BaseModel):
    name: str
    query: str
    AR: List[str] = []
    AW: List[str] = []
    DR: List[str] = []
    DW: List[str] = []


class DeleteAccessControlRequirementBody(BaseModel):
    name: str
