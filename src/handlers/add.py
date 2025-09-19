# handlers/add.py
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.keyboards import get_main_menu_keyboard
from utils.storage import add_ad
from utils.logger import get_logger

router = Router()
logger = get_logger(__name__)


class AddAdStates(StatesGroup):
    waiting_for_photo_description = State()


@router.message(Command("add"))
async def command_add_handler(message: Message) -> None:
    """
    Handles /add command.
    Provides instructions for creating advertisements.
    """
    add_text = (
        "📝 <b>Create New Advertisement</b>\n\n"
        "You can create different types of ads:\n\n"
        "🔸 <b>Text Ad:</b> Just send me any text message\n"
        "🔸 <b>Photo Ad:</b> Send a photo (with optional description)\n"
        "🔸 <b>Audio Ad:</b> Send an audio file or voice message\n\n"
        "💡 <b>What to do next:</b>\n"
        "Simply send me the content you want to turn into an advertisement!\n"
        "I'll guide you through the process."
    )

    await message.answer(add_text, reply_markup=get_main_menu_keyboard())


@router.callback_query(F.data == "add_photo_description")
async def add_photo_description_callback(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Handles callback when user wants to add description to photo.
    """
    await state.set_state(AddAdStates.waiting_for_photo_description)
    await callback.message.edit_text(
        "📝 <b>Add Photo Description</b>\n\n"
        "Send me a text description for your photo advertisement:"
    )
    await callback.answer()


@router.callback_query(F.data == "save_photo_no_desc")
async def save_photo_no_description_callback(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Handles saving photo without description.
    """
    user_data = await state.get_data()
    file_id = user_data.get("photo_file_id")
    user_id = callback.from_user.id

    if file_id:
        success = add_ad(user_id, "photo", file_id=file_id)

        if success:
            await callback.message.edit_text(
                "✅ <b>Photo Advertisement Created!</b>\n\n"
                "Your photo ad has been saved successfully!"
            )
            logger.info(f"Photo ad created by user {user_id}")
        else:
            await callback.message.edit_text(
                "❌ <b>Error</b>\n\n"
                "Failed to save your advertisement. Please try again."
            )
    else:
        await callback.message.edit_text(
            "❌ <b>Error</b>\n\n" "Photo not found. Please try again."
        )

    await state.clear()
    await callback.answer()


@router.message(AddAdStates.waiting_for_photo_description)
async def process_photo_description(message: Message, state: FSMContext) -> None:
    """
    Processes photo description input.
    """
    if not message.text:
        await message.answer("Please send a text description for your photo.")
        return

    user_data = await state.get_data()
    file_id = user_data.get("photo_file_id")
    user_id = message.from_user.id

    if file_id:
        success = add_ad(user_id, "photo", file_id=file_id, caption=message.text)

        if success:
            await message.answer(
                "✅ <b>Photo Advertisement Created!</b>\n\n"
                f"Your photo ad with description has been saved successfully!\n\n"
                f"<b>Description:</b> {message.text}",
                reply_markup=get_main_menu_keyboard(),
            )
            logger.info(f"Photo ad with description created by user {user_id}")
        else:
            await message.answer(
                "❌ <b>Error</b>\n\n"
                "Failed to save your advertisement. Please try again.",
                reply_markup=get_main_menu_keyboard(),
            )
    else:
        await message.answer(
            "❌ <b>Error</b>\n\n" "Photo not found. Please try again.",
            reply_markup=get_main_menu_keyboard(),
        )

    await state.clear()
