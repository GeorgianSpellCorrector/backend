from fastapi import APIRouter

from app.routers import users

api = APIRouter()

api.include_router(users.router, prefix='/users', tags=['users'])
