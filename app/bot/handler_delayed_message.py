import asyncio
import logging

from main import bot
from utils import (get_delayed_message, broadcast_message,
                   get_tg_users, patch_status_delayed_message,
                   make_image_from_base64)


logger = logging.getLogger(__name__)


async def send_delayed_message(message_id: str):
    """
    Получает отложенное сообщение по id.
    Получает список id пользователей.
    Рассылает сообщения.
    Меняет статус отложенного сообщения после успешной отправки.
    """
    message = await get_delayed_message(message_id)
    if message:
        text = message.get('text', '')
        users_id = await get_tg_users()
        image_file = await make_image_from_base64(
            message=message, filename=message_id)
        count = 0
        try:
            for user_id in [user_id.get('tg_id') for user_id in users_id]:
                if await broadcast_message(bot=bot,
                                           user_id=user_id,
                                           text=text,
                                           photo=image_file):
                    count += 1
                await asyncio.sleep(
                    0.05
                )  # 20 сообщений в секунду (Лимит: 30)
        except Exception:
            logger.exception(
                'Необработанная ошибка при рассылке отложенного сообщения.')
        else:
            await patch_status_delayed_message(
                message_id=message_id, status=True)
        finally:
            logger.info(f'Успешно отправлено: {count}')
