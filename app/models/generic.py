from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class User(UserBase):
    ip_address: str
    created_at: str
