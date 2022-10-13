from pydantic import BaseModel
from datetime import datetime


class FileSnapshot(BaseModel):
    name: str
    created: datetime
    root_id: str
