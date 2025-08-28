from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    is_active: bool
    is_superuser: bool


class Token(BaseModel):
    access_token: str
    token_type: str
