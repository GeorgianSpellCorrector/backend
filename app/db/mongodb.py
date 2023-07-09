from motor.motor_asyncio import AsyncIOMotorClient

from app.config import MongoDBSettings

settings = MongoDBSettings()


async def get_database() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    return client[settings.MONGO_DB]
