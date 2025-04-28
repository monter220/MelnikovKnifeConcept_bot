import asyncio
import base64
import logging
from http import HTTPStatus

from aiogram import exceptions, Bot
from aiohttp import ClientResponseError, ClientSession
from aiogram.types import BufferedInputFile

from config import settings
from constants import DEFAULT_MESSAGES_MAP


logger = logging.getLogger(__name__)


async def async_session(url, method, data=None):
    async with ClientSession() as session:
        async with session.request(method, url, json=data) as response:
            response.raise_for_status()
            if response.content_length:
                return await response.json()
        return None


async def get_tg_user(tg_user_id):
    """Получает пользователя телеграмм по id."""
    tg_user = await async_session(
        settings.bot.fastapi_url + f'tg_users/{tg_user_id}/', 'GET')
    return tg_user


async def get_tg_users():
    """Получает список id пользователй телеграмм."""
    tg_users = await async_session(
        settings.bot.fastapi_url + 'tg_users/', 'GET')
    return tg_users


async def create_tg_user(data):
    """Создает пользователя."""
    tg_user = await async_session(
        settings.bot.fastapi_url + 'tg_users/', 'POST', data)
    return tg_user


async def delete_tg_user(tg_user_id):
    """Деактивирует пользователя."""
    await async_session(
        settings.bot.fastapi_url + f'tg_users/{tg_user_id}/', 'DELETE')


async def get_default_message(message_type):
    """Получает сообщение для кнопок по его типу."""
    try:
        default_message = await async_session(
            settings.bot.fastapi_url + f'messages/{message_type}/', 'GET')
    except ClientResponseError as e:
        if e.status == HTTPStatus.NOT_FOUND:
            return {'text': DEFAULT_MESSAGES_MAP.get(message_type)}
    return default_message


async def get_knifes():
    """Получает список ножей."""
    knifes = await async_session(
        settings.bot.fastapi_url + 'knifes/', 'GET')
    return knifes


async def broadcast_message(
    bot: Bot,
    user_id: int,
    text: str,
    photo,
    disable_notification: bool = False,
) -> bool:
    """Safe messages sender"""
    try:
        if photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=text,
                disable_notification=disable_notification)
        else:
            await bot.send_message(
                chat_id=user_id,
                text=text,
                disable_notification=disable_notification)
    except exceptions.TelegramServerError:
        logger.error(f'Target [ID:{user_id}]: blocked by user')
    except exceptions.TelegramNotFound:
        logger.error(f'Target [ID:{user_id}]: invalid user ID')
    except exceptions.TelegramRetryAfter as e:
        logger.error(
            f'Target [ID:{user_id}]: Flood limit is exceeded.'
            f'Sleep {e.timeout} seconds.'
        )
        await asyncio.sleep(e.timeout)
        return await broadcast_message(
            bot=bot,
            user_id=user_id,
            text=text,
            photo=photo)  # Recursive call
    except exceptions.TelegramForbiddenError:
        logger.error(f'Target [ID:{user_id}]: user is deactivated')
        await delete_tg_user(tg_user_id=user_id)
    except exceptions.TelegramAPIError:
        logger.exception(f'Target [ID:{user_id}]: failed')
    except exceptions.TelegramBadRequest:
        logger.exception(f'Target [ID:{user_id}]: not found')
    else:
        logger.info(f'Target [ID:{user_id}]: success')
        return True
    return False


async def make_image_from_base64(
        message: dict, filename: str) -> BufferedInputFile | None:
    """Если у сообщения есть изображение в формате base64 делает
    из него BufferedInputFile для отправки в телеграмм."""
    image_base64 = message.get('image', None)
    if image_base64:
        return BufferedInputFile(
            file=base64.b64decode(image_base64),
            filename=f'{filename}.png')


async def get_single_knife(knife_id):
    """Получает нож по id."""
    knife = await async_session(
        settings.bot.fastapi_url + f'knifes/{knife_id}/', 'GET')
    return knife


async def get_delayed_message(message_id):
    """Получает отложенное сообщение по id."""
    delayed_message = await async_session(
        settings.bot.fastapi_url + f'delayed_messages/{message_id}/', 'GET')
    return delayed_message


async def patch_status_delayed_message(message_id, status):
    """Меняет статус сообщения после успешной оправки."""
    delayed_message = await async_session(
        settings.bot.fastapi_url + f'delayed_messages/{message_id}/status/',
        'PATCH',
        {'status': status}
    )
    return delayed_message
