import base64
from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, HTTPException

from models import Knife
from schemas import KnifeBase, PreviewKnifeList


router = APIRouter()


@router.get('/{knife_id}', response_model=KnifeBase)
async def get_tg_user(knife_id: str):
    knife = Knife.objects(name=knife_id, active=True).first()
    if not knife:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Нож с id {knife_id} не найден или недоступен.')
    image = knife.photo.read()
    if image:
        image_base64 = base64.b64encode(image).decode('utf-8')
    else:
        image_base64 = None
    response_data = {
        'name': knife.name,
        'photo': image_base64,
        'desc':  knife.desc,
        'weight': knife.weight,
        'length': knife.length,
        'width': knife.width,
        'thickness': knife.thickness,
        'features': knife.features,
        'pretentious_quote': knife.pretentious_quote,
    }
    return response_data


@router.get('/', response_model=Optional[List[PreviewKnifeList]])
async def get_tg_users():
    return Knife.objects(active=True)
