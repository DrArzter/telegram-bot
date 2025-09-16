from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message

from utils.logger import get_logger

router = Router()
logger = get_logger(__name__)


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    Handles commands like /start.
    Sends a greeting message and logs the user's info.
    """
    user = message.from_user

    if user and user.username:
        await message.answer(f"Hello, {html.bold(user.username)}!")
    else:
        await message.answer("Hello!")
