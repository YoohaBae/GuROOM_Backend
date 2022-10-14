from pydantic import BaseModel
from typing import List
from datetime import datetime


class SharedDrive(BaseModel):
    id: str
    name: str


class FileSnapshot(BaseModel):
    name: str
    created: datetime
    root_id: str
    shared_drives: List[SharedDrive]
