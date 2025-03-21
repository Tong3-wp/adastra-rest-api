from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    role: str = "user"


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
