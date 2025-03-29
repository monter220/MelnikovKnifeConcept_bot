import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.bot import DefaultBotProperties

from bot_menu import setup_bot_commands
from config import settings
from handlers import router as main_router
from handler_errors import router as errors_router


logging.basicConfig(
    level=logging.INFO if settings.bot.debug else logging.ERROR,
    format='%(asctime)s - [%(levelname)s] - %(name)s - '
           '%(filename)s.%(funcName)s(%(lineno)d) - %(message)s')

bot = Bot(token=settings.bot.telegram_token.get_secret_value(),
          default=DefaultBotProperties(parse_mode=settings.bot.parse_mode))


async def main():
    """Запуск бота."""
    dispatcher = Dispatcher()
    dispatcher.startup.register(setup_bot_commands)
    dispatcher.include_router(main_router)
    dispatcher.include_router(errors_router)

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())