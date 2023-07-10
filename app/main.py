from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import FastAPISettings
from app.db.mongodb.indexes import create_indexes_if_necessary
from app.db.mongodb.wrapper import mongo_client_wrapper, get_database
from app.routers import api
from app.utils.httpx import httpx_client_wrapper

settings = FastAPISettings()
app = FastAPI(**settings.model_dump())

app.include_router(api, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    mongo_client_wrapper.start()
    httpx_client_wrapper.start()
    db = await get_database()
    await create_indexes_if_necessary(db)


@app.on_event('shutdown')
async def shutdown():
    mongo_client_wrapper.stop()
    await httpx_client_wrapper.stop()
