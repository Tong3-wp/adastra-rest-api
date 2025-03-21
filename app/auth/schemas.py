from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    role: str = "user"  # Default role is 'user'


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
