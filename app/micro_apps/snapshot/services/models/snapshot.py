from pydantic import BaseModel
from typing import List
from .files import File
from datetime import datetime


class FileSnapshot(BaseModel):
    name: str
    files: List[File]
    created: datetime
    search_query: List[str]
    user_id: str
