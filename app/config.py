import os

from pydantic import BaseModel


class FastAPISettings(BaseModel):
    title: str = 'Georgian Spell Checker'
    version: str = '0.1.0'
    description: str = 'Georgian Spell Checker API'


class MongoDBSettings(BaseModel):
    MONGO_HOST: str = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT: int = int(os.getenv('MONGO_PORT', 27017))
    MONGO_DB: str = os.getenv('MONGO_DB')
    MONGO_USER: str = os.getenv('MONGO_USER')
    MONGO_PASSWORD: str = os.getenv('MONGO_PASSWORD')
    ARGS: str = 'retryWrites=true&w=majority&authSource=admin'
    MONGO_URI: str = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?{ARGS}'


class GeorgianSpellCorrectorModelSettings(BaseModel):
    MODEL_API: str = os.getenv('GSC_MODEL_API')
    BEARER_TOKEN: str = os.getenv('GSC_BEARER_TOKEN')
    payload: dict = {
        'url': MODEL_API,
        'headers': {'Authorization': f'Bearer {BEARER_TOKEN}'},
    }
