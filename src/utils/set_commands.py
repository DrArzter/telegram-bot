from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot) -> None:
    """
    Sets the bot's commands.

    :param bot: The bot instance.
    :type bot: Bot
    """
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Start the bot"),
            BotCommand(command="/help", description="Get help"),
        ]
    )
