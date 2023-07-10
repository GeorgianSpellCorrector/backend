from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import ASCENDING, TEXT


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    ip_address: str
    created_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class Text(BaseModel):
    user_id: PydanticObjectId
    text: str = Field(..., min_length=3, max_length=10000)
    rating: Optional[int] = Field(..., ge=0, le=5)
    corrected_text: str
    corrected_text_cleaned: str
    suggested_text: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Meta:
        indexes = [
            dict(name='text_corrected_text_index', keys=[('text', TEXT),
                                                         ('corrected_text', TEXT),
                                                         ('suggested_text', TEXT)],
                 default_language='None'),
            dict(name='rating_index', keys=[('rating', ASCENDING)]),
            dict(name='user_id_index', keys=[('user_id', ASCENDING)]),
        ]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
