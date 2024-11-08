from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException

from app.admin_panel.models import Knife
from app.admin_panel.schemas import KnifeBase, PreviewKnifeList


router = APIRouter()


@router.get('/{knife_id}', response_model=KnifeBase)
async def get_tg_user(knife_id: int):
    knife = Knife.objects(tg_id=knife_id, active=True).first()
    if not knife:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Нож с id {knife_id} не найден или недоступен.')
    return knife


@router.get('/', response_model=List[PreviewKnifeList])
async def get_tg_users():
    return Knife.objects(active=True)
