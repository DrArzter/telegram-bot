# handlers/media.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.keyboards import (
    get_confirm_text_keyboard,
    get_photo_description_keyboard,
    get_main_menu_keyboard,
)
from utils.storage import add_ad
from utils.logger import get_logger

router = Router()
logger = get_logger(__name__)


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_message(message: Message, state: FSMContext) -> None:
    """
    Handles text messages and offers to save as advertisement.
    """
    await state.update_data(text_content=message.text)

    await message.answer(
        f"📝 <b>Text Message Received</b>\n\n"
        f"<b>Your text:</b>\n{message.text}\n\n"
        f"Do you want to save this as a text advertisement?",
        reply_markup=get_confirm_text_keyboard(),
    )

    logger.info(f"Text message received from user {message.from_user.id}")


@router.callback_query(F.data == "confirm_text_ad")
async def confirm_text_ad_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Handles confirmation to save text as advertisement.
    """
    user_data = await state.get_data()
    text_content = user_data.get("text_content")
    user_id = callback.from_user.id

    if text_content:
        success = add_ad(user_id, "text", content=text_content)

        if success:
            await callback.message.edit_text(
                "✅ <b>Text Advertisement Created!</b>\n\n"
                f"Your text ad has been saved successfully!\n\n"
                f"<b>Content:</b> {text_content}",
                reply_markup=get_main_menu_keyboard(),
            )
            logger.info(f"Text ad created by user {user_id}")
        else:
            await callback.message.edit_text(
                "❌ <b>Error</b>\n\n"
                "Failed to save your advertisement. Please try again."
            )
    else:
        await callback.message.edit_text(
            "❌ <b>Error</b>\n\n" "Text content not found. Please try again."
        )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "cancel_text_ad")
async def cancel_text_ad_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Handles cancellation of text advertisement.
    """
    await callback.message.edit_text(
        "❌ <b>Cancelled</b>\n\n" "Text advertisement was not saved."
    )
    await state.clear()
    await callback.answer()


@router.message(F.photo)
async def handle_photo_message(message: Message, state: FSMContext) -> None:
    """
    Handles photo messages and asks for description.
    """
    photo = message.photo[-1]
    file_id = photo.file_id

    await state.update_data(photo_file_id=file_id)

    caption_text = ""
    if message.caption:
        caption_text = f"\n\n<b>Current caption:</b> {message.caption}"

    await message.answer(
        f"📸 <b>Photo Received</b>{caption_text}\n\n"
        f"Would you like to add a description to your photo advertisement?",
        reply_markup=get_photo_description_keyboard(),
    )

    logger.info(f"Photo received from user {message.from_user.id}")


@router.message(F.audio)
async def handle_audio_message(message: Message) -> None:
    """
    Handles audio files and saves as advertisement.
    """
    file_id = message.audio.file_id
    user_id = message.from_user.id

    caption = ""
    if message.audio.title:
        caption += f"Title: {message.audio.title}"
    if message.audio.performer:
        caption += f" | Artist: {message.audio.performer}"

    success = add_ad(user_id, "audio", file_id=file_id, caption=caption)

    if success:
        await message.answer(
            "🎶 <b>Audio Advertisement Added!</b>\n\n"
            f"Your audio file has been saved as an advertisement!\n"
            f"{f'<b>Info:</b> {caption}' if caption else ''}",
            reply_markup=get_main_menu_keyboard(),
        )
        logger.info(f"Audio ad created by user {user_id}")
    else:
        await message.answer(
            "❌ <b>Error</b>\n\n"
            "Failed to save your audio advertisement. Please try again.",
            reply_markup=get_main_menu_keyboard(),
        )


@router.message(F.voice)
async def handle_voice_message(message: Message) -> None:
    """
    Handles voice messages and saves as advertisement.
    """
    file_id = message.voice.file_id
    user_id = message.from_user.id

    duration = message.voice.duration
    caption = f"Voice message ({duration}s)" if duration else "Voice message"

    success = add_ad(user_id, "voice", file_id=file_id, caption=caption)

    if success:
        await message.answer(
            (
                "🎙️ <b>Voice Advertisement Added!</b>\n\n"
                f"Your voice message has been saved as an advertisement!\n"
                f"<b>Duration:</b> {duration}s"
                if duration
                else "Your voice message has been saved!"
            ),
            reply_markup=get_main_menu_keyboard(),
        )
        logger.info(f"Voice ad created by user {user_id}")
    else:
        await message.answer(
            "❌ <b>Error</b>\n\n"
            "Failed to save your voice advertisement. Please try again.",
            reply_markup=get_main_menu_keyboard(),
        )


@router.message(F.document)
async def handle_document_message(message: Message) -> None:
    """
    Handles document messages (not supported).
    """
    await message.answer(
        "📄 <b>Document Received</b>\n\n"
        "Sorry, documents are not supported for advertisements.\n"
        "Supported formats: text, photos, audio files, and voice messages.",
        reply_markup=get_main_menu_keyboard(),
    )
