# handlers/start.py
from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message
from utils.logger import get_logger
from utils.keyboards import get_main_menu_keyboard

router = Router()
logger = get_logger(__name__)

@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    Handles /start command.
    Sends a greeting message with main menu keyboard.
    """
    user = message.from_user
    
    if user and user.username:
        welcome_text = (
            f"Hello, {html.bold(user.username)}! 👋\n\n"
            f"Welcome to the Ads Bot! 📱\n"
            f"Here you can create and browse advertisements.\n\n"
            f"Use the menu below to get started:"
        )
    else:
        welcome_text = (
            f"Hello! 👋\n\n"
            f"Welcome to the Ads Bot! 📱\n"
            f"Here you can create and browse advertisements.\n\n"
            f"Use the menu below to get started:"
        )
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )
    
    logger.info(f"Start command executed by user {user.id if user else 'unknown'}")