from motor.motor_asyncio import AsyncIOMotorClient

from app.config import MongoDBSettings
from app.utils.uvicorn_logger import logger

settings = MongoDBSettings()


class MongoClientWrapper:
    client = None

    def start(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        try:
            logger.info('checking db connection')
            self.client.admin.command('ping')
            logger.info('db connection established')
        except Exception as e:
            logger.error(e)
            raise e

    def stop(self):
        logger.info('closing db connection')
        self.client.close()
        self.client = None
        logger.info('db connection closed')

    def __call__(self):
        assert self.client is not None, 'MongoClientWrapper not started'
        return self.client


mongo_client_wrapper = MongoClientWrapper()


async def get_database() -> AsyncIOMotorClient:
    client = mongo_client_wrapper()
    return client[settings.MONGO_DB]
