from fastapi import APIRouter

from .endpoints import tgusers_router, messages_router, knifes_router, delayedmessages_router
from core.config import API_VERSION


api_router = APIRouter(prefix=f'/api/{API_VERSION}')
api_router.include_router(tgusers_router,
                          prefix='/tg_users',
                          tags=('Пользователи бота',))
api_router.include_router(messages_router,
                          prefix='/messages',
                          tags=('Базовые сообщения',))
api_router.include_router(messages_router,
                          prefix='/delayed_messages',
                          tags=('Отложенные сообщения',))
api_router.include_router(knifes_router,
                          prefix='/knifes',
                          tags=('Ножи',))
