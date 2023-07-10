from datetime import datetime
from typing import List, Optional, Union

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from app.models.generic import PydanticObjectId


class UserInputSerializer(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class UserOutputSerializer(BaseModel):
    id: Union[PydanticObjectId, ObjectId] = Field(..., alias='_id')
    username: str = Field(..., min_length=3, max_length=50)
    ip_address: str
    created_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    @field_validator('id')
    def check_object_id(cls, v):
        return str(v)


class TextInputSerializer(BaseModel):
    text: str = Field(..., min_length=3, max_length=10000)


class TextOutputSerializer(BaseModel):
    id: Union[PydanticObjectId, ObjectId] = Field(..., alias='_id')
    user_id: Union[PydanticObjectId, ObjectId]
    text: str
    rating: Optional[int] = Field(default=None)
    corrected_text: str
    corrected_text_cleaned: str
    suggested_text: Optional[str] = Field(default=None)
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    @field_validator('id')
    def check_object_id(cls, v):
        return str(v)

    @field_validator('user_id')
    def check_user_id(cls, v):
        return str(v)


class SpellErrorSerializer(BaseModel):
    bad: str
    better: List[str]
    offset: int
    length: int
