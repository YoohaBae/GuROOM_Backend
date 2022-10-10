from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: str
    given_name: str
    family_name: str
    picture: str
    locale: str
