import asyncio
from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from utils.handlers import include_routers
from utils.set_commands import set_commands
from utils.logger import get_logger

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

logger = get_logger(__name__)

if TOKEN is None:
    raise ValueError("No token provided")

dp = Dispatcher()

# Connecting handlers
include_routers(dp)


async def main() -> None:
    """
    Main function of the bot.

    It initializes the bot and dispatcher, sets commands and starts the event dispatching loop.
    """

    # Just to satisfy linter
    if TOKEN is None:
        raise ValueError("No token provided")

    # Initialize Bot and Dispatcher
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Set commands
    await set_commands(bot)

    logger.info("Bot started")

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
