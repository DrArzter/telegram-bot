from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message(Command("list"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/list` command
    """
    await message.answer("list")