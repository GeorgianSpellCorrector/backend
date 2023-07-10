from app.utils.class_accessories import get_meta_classes
from app.utils.uvicorn_logger import logger


async def create_indexes_if_necessary(db):
    meta_classes = get_meta_classes('app.models')
    indexes = [indexes for meta in meta_classes for indexes in meta.indexes if hasattr(meta, 'indexes')]

    existing_indexes = await db['texts'].index_information()
    for index in indexes:
        name = index.get('name')
        if name not in existing_indexes:
            logger.info(f'creating index {name}')
            await db['texts'].create_index(**index)
