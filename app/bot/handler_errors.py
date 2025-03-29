import logging

from aiohttp.client_exceptions import ClientConnectionError
from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message, CallbackQuery

from constants import MessagesConstants


router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.errors(
        ExceptionTypeFilter(ClientConnectionError),
        (F.update.callback_query.message.as_('message') |
         F.update.message.as_('message'))
)
async def connection_error(
        event: ErrorEvent,
        message: Message | CallbackQuery = None) -> None:
    """Запись в лог ошибки соединения с api."""
    logger.critical(f'Ошибка подключения к api - {event.exception}')
    await message.answer(MessagesConstants.ERROR)


@router.errors(
        (F.update.callback_query.message.as_('message') |
         F.update.message.as_('message')))
async def unhandled_errors(
        event: ErrorEvent,
        message: Message | CallbackQuery = None) -> None:
    """Хендлер для всех необработанных исключений."""
    logger.error(event.exception)
    await message.answer(MessagesConstants.ERROR)
