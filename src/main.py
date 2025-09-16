import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv

from handlers import include_routers
from utils.set_commands import set_commands
from utils.logger import get_logger


# Load environment variables
load_dotenv()
TOKEN = getenv("BOT_TOKEN")
logger = get_logger(__name__)

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")


# Initialize dispatcher
dp = Dispatcher()
include_routers(dp)


async def on_startup(bot: Bot) -> None:
    """Actions to perform on bot startup."""
    logger.info("Bot is starting up...")


async def on_shutdown(bot: Bot) -> None:
    """Actions to perform on bot shutdown."""
    logger.info("Bot is shutting down...")


async def main() -> None:
    """Main entry point of the bot."""

    # TO KEEP FUCKING LINTER HAPPY
    if not TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables.")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await set_commands(bot)
    logger.info("Bot commands set successfully.")
    logger.info("Bot is starting polling...")

    await dp.start_polling(bot, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == "__main__":
    asyncio.run(main())
