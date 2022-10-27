from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str
    given_name: str
    family_name: str
    picture: Optional[str]
    email: str
