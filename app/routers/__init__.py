from fastapi import APIRouter

from app.routers import users, texts

api = APIRouter()

api.include_router(users.router, prefix='/users', tags=['users'])
api.include_router(texts.router, prefix='/texts', tags=['texts'])
