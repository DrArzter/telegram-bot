from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, html

router = Router()

@router.message(Command("add"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/add` command
    """
    await message.answer("add")