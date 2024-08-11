from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
