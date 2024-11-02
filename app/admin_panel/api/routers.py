from fastapi import APIRouter

from .endpoints import tgusers_router
from app.admin_panel.core.config import API_VERSION


api_router = APIRouter(prefix=f'/api/{API_VERSION}')
api_router.include_router(tgusers_router,
                          prefix='/tg_users',
                          tags=('Пользователи бота',))
# api_router.include_router(delayed_messages_router,
#                           prefix='/delayed-messages',
#                           tags=('Отложенные сообщения',))
# api_router.include_router(events_router,
#                           prefix='/events',
#                           tags=('Мероприятия',))
# api_router.include_router(chats_router,
#                           prefix='/chats',
#                           tags=('Чаты выпускников',))
# api_router.include_router(default_messages_router,
#                           prefix='/messages',
#                           tags=('Базовые сообщения',))