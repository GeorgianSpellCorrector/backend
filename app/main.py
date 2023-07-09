from fastapi import FastAPI

from app.config import FastAPISettings
from app.routers import api


settings = FastAPISettings()
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
)

app.include_router(api, prefix='/api')

