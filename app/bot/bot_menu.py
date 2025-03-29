from aiogram import Bot
from aiogram.types import BotCommand

from constants import MessagesConstants


async def setup_bot_commands(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in MessagesConstants.COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)
