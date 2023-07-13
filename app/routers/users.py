from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from app.db.mongodb.wrapper import get_database
from app.models.generic import User
from app.models.serializers import UserInputSerializer, UserOutputSerializer
from app.routers.utils import check_object_id

router = APIRouter()


@router.post('/create_user')
async def create_user(request: Request, user: UserInputSerializer, db: AsyncIOMotorClient = Depends(get_database)):
    user_dump = user.model_dump()
    user = await db['users'].find_one({'username': user_dump['username'], 'ip_address': request.client.host})
    if user:
        return {'_id': str(user['_id'])}

    user = User(**user_dump, ip_address=request.client.host, created_at=datetime.utcnow())
    user = await db['users'].insert_one(user.model_dump())
    return {'_id': str(user.inserted_id)}


@router.get('/get_user/{pk}')
async def get_user(pk: str = Depends(check_object_id),
                   db: AsyncIOMotorClient = Depends(get_database)) -> UserOutputSerializer:
    user = await db['users'].find_one({'_id': ObjectId(pk)})
    if not user:
        raise HTTPException(status_code=404, detail='User not found!')
    return UserOutputSerializer(**user)


@router.post('/remove_user/{pk}')
async def remove_user(pk: str = Depends(check_object_id), db: AsyncIOMotorClient = Depends(get_database)):
    user = await db['users'].find_one({'_id': ObjectId(pk)})
    if not user:
        raise HTTPException(status_code=404, detail='User not found!')
    await db['texts'].delete_many({'user_id': ObjectId(pk)})
    await db['users'].delete_one({'_id': ObjectId(pk)})
    return {'_id': pk}
