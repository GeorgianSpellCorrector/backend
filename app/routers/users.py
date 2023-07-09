from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from app.db.mongodb import get_database
from app.models.generic import UserBase, User

router = APIRouter()


@router.post('/create_user')
async def create_user(request: Request, user: UserBase, db: AsyncIOMotorClient = Depends(get_database)):
    user = User(**user.model_dump(), ip_address=request.client.host,
                created_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    user = await db['users'].insert_one(user.model_dump())
    return {'_id': str(user['_id'])}


@router.get('/get_user/{pk}')
async def get_user(pk: str, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        user = await db['users'].find_one({'_id': ObjectId(pk)})
    except InvalidId:
        return {'message': f'User not found!'}
    if user is None:
        return {'message': f'User not found!'}
    return User(**user)


@router.post('/remove_user/{pk}')
async def remove_user(pk: str, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        user = await db['users'].delete_one({'_id': ObjectId(pk)})
    except InvalidId:
        return {'message': f'User not found!'}
    if user.deleted_count == 0:
        return {'message': f'User not found!'}
    return {'message': f'User {pk} deleted successfully'}
