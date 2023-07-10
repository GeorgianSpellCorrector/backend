from bson import ObjectId
from fastapi import HTTPException


def check_object_id(pk: str):
    if not ObjectId.is_valid(pk):
        raise HTTPException(status_code=400, detail='Object id is invalid')
    return pk


def check_user_object_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail='User id is invalid')
    return user_id
