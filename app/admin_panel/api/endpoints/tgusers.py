from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException

from models import TGUser
from schemas import TGUserBase, TGUsersList


router = APIRouter()


@router.post('/', response_model=TGUserBase)
async def create_user(user: TGUserBase):
    tg_user = TGUser.objects(tg_id=user.tg_id).first()
    if not tg_user:
        new_user = TGUser(
            tg_id=user.tg_id, nickname=user.nickname, gdpr=user.gdpr)
        new_user.save()
        return new_user
    elif tg_user and not tg_user.active:
        tg_user.update(set__active=True)
        tg_user.reload()
    return tg_user


@router.get('/{tg_user_id}', response_model=TGUserBase)
async def get_tg_user(tg_user_id: int):
    tg_user = TGUser.objects(tg_id=tg_user_id).first()
    if not tg_user or not tg_user.active:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Пользователь с id {tg_user_id} не найден или выключен.')
    return tg_user


@router.get('/', response_model=List[TGUsersList])
async def get_tg_users():
    return TGUser.objects(active=True, gdpr=True)


@router.delete('/{tg_user_id}', status_code=HTTPStatus.NO_CONTENT)
async def deactivate_tg_user(tg_user_id: int):
    tg_user = TGUser.objects(tg_id=tg_user_id).first()
    if tg_user:
        tg_user.update(set__active=False)
