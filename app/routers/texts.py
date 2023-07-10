import re
from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, Body, Query, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import GeorgianSpellCorrectorModelSettings
from app.db.mongodb.wrapper import get_database
from app.models.generic import Text, PydanticObjectId
from app.models.serializers import SpellErrorSerializer, TextInputSerializer, TextOutputSerializer
from app.routers.utils import check_object_id, check_user_object_id
from app.utils.httpx import httpx_client_wrapper

router = APIRouter()
gsc_settings = GeorgianSpellCorrectorModelSettings()


@router.post('/create_and_check_text')
async def create_and_check_text(text: TextInputSerializer = Body(), user_id: str = Depends(check_object_id),
                                async_httpx=Depends(httpx_client_wrapper),
                                db: AsyncIOMotorClient = Depends(get_database)) -> List[SpellErrorSerializer]:
    text_to_check = text.text
    response = await async_httpx.post(
        **gsc_settings.payload,
        json={'inputs': text_to_check}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=response.text)
    data = response.json()
    corrected_texts = re.sub(' +', ' ', data[0]['generated_text'].strip()).split(' ')
    errors = []
    offset = 0
    good_text = ''
    for x, y in zip(text_to_check.split(' '), corrected_texts):
        if x != y:
            errors.append(SpellErrorSerializer(**{
                'bad': x,
                'better': [y],
                'offset': offset,
                'length': len(x)
            }))
            good_text += y + ' '
        else:
            good_text += x + ' '
        offset += len(x) + 1

    obj = Text(user_id=PydanticObjectId(user_id),
               text=text_to_check,
               rating=None,
               corrected_text=' '.join(corrected_texts),
               corrected_text_cleaned=good_text.strip(),
               suggested_text=None,
               created_at=datetime.utcnow(),
               updated_at=datetime.utcnow()
               )
    await db['texts'].insert_one(obj.model_dump())
    return errors


@router.get('/get_texts/{pk}')
async def get_texts(pk: str = Depends(check_object_id),
                    db: AsyncIOMotorClient = Depends(get_database),
                    page: int = 1, limit: int = 10
                    ) -> List[TextOutputSerializer]:
    texts: List[TextOutputSerializer] = []
    async for text in db['texts'].find({'user_id': ObjectId(pk)}).skip((page - 1) * limit).limit(limit):
        texts.append(TextOutputSerializer(**text))
    return texts


@router.get('/search_text/{pk}')
async def search_text(q: str,
                      rating: int = Query(default=None, ge=0, le=5),
                      rated: bool = Query(default=None),
                      pk: str = Depends(check_object_id),
                      full_text_search: bool = Query(default=False),
                      db: AsyncIOMotorClient = Depends(get_database),
                      page: int = 1, limit: int = 10,
                      ) -> List[TextOutputSerializer]:
    texts: List[TextOutputSerializer] = []
    if rated is not None and not rated:
        rating = None

    if full_text_search:
        async for text in db['texts'].find(
                {'user_id': ObjectId(pk),
                 **({'rating': rating} if rating is not None else {}),
                 '$text': {'$search': q}},
        ).skip((page - 1) * limit).limit(limit):
            texts.append(TextOutputSerializer(**text))
    else:
        async for text in db['texts'].find(
                {'user_id': ObjectId(pk), **({'rating': rating} if rating else {}),
                 '$or': [{'text': {'$regex': q}},
                         {'corrected_text': {'$regex': q}},
                         {'suggested_text': {'$regex': q}}]},
        ).skip((page - 1) * limit).limit(limit):
            texts.append(TextOutputSerializer(**text))

    return texts


@router.put('/update_text/{pk}')
async def update_text(pk: str = Depends(check_object_id),
                      suggested_text: str = Body(default=None),
                      rating: int = Body(default=None, ge=0, le=5),
                      user_id: str = Depends(check_user_object_id),
                      db: AsyncIOMotorClient = Depends(get_database)):
    text = await db['texts'].find_one({'_id': ObjectId(pk), 'user_id': ObjectId(user_id)})
    if text is None:
        raise HTTPException(status_code=404, detail='Text not found')

    if suggested_text is None and rating is None:
        raise HTTPException(status_code=400, detail='Nothing to update')
    if suggested_text is not None:
        await db['texts'].update_one({'_id': ObjectId(pk)}, {'$set': {'suggested_text': suggested_text,
                                                                      'updated_at': datetime.utcnow()}})
    if rating is not None:
        await db['texts'].update_one({'_id': ObjectId(pk)}, {'$set': {'rating': rating,
                                                                      'updated_at': datetime.utcnow()}})
    return {'detail': 'Updated successfully'}
