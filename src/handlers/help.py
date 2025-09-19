# handlers/help.py
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from utils.keyboards import get_main_menu_keyboard

router = Router()

@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    Handles /help command.
    Shows bot instructions and available commands.
    """
    help_text = (
        "📱 <b>Ads Bot - Help</b>\n\n"
        
        "🔹 <b>Available commands:</b>\n"
        "/start - Start the bot and show main menu\n"
        "/help - Show this help message\n"
        "/add - Create a new advertisement\n"
        "/list - Show all saved advertisements\n\n"
        
        "🔹 <b>How to use:</b>\n"
        "• Use menu buttons for easy navigation\n"
        "• Send text to create text ads\n"
        "• Send photos to create photo ads\n"
        "• Send audio/voice to create audio ads\n"
        "• Like ads you enjoy ❤️\n"
        "• Delete your own ads 🗑\n\n"
        
        "🔹 <b>Supported media:</b>\n"
        "• Text messages\n"
        "• Photos with optional captions\n"
        "• Audio files\n"
        "• Voice messages\n\n"
        
        "💡 <b>Tip:</b> All ads are automatically saved and can be viewed by all users!"
    )
    
    await message.answer(help_text, reply_markup=get_main_menu_keyboard())