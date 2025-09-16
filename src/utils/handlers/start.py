from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, html

from utils.logger import get_logger

router = Router()

logger = get_logger(__name__)

@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    logger.info("Received /start command")
    if message.from_user and message.from_user.username:
        await message.answer(f"Hello, {html.bold(message.from_user.username)}!")
    else:
        await message.answer("Hello!")