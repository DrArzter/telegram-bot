from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from utils.storage import load_ads, like_ad, delete_ad, get_ad_by_id
from utils.keyboards import (
    get_ad_actions_keyboard,
    get_main_menu_keyboard,
    get_ads_navigation_keyboard,
)
from utils.logger import get_logger
from math import ceil

router = Router()
logger = get_logger(__name__)

ADS_PER_PAGE = 5


@router.message(Command("list"))
async def command_list_handler(message: Message) -> None:
    """
    Handles /list command.
    Shows all saved advertisements with pagination.
    """
    await show_ads_page(message, page=1, user_id=message.from_user.id)


async def show_ads_page(message: Message, page: int = 1, user_id: int = None) -> None:
    ads = load_ads()

    if not ads:
        await message.answer(
            "📋 <b>No Advertisements Found</b>\n\n"
            "There are no advertisements yet. Be the first to create one!",
            reply_markup=get_main_menu_keyboard(),
        )
        return

    total_ads = len(ads)
    total_pages = ceil(total_ads / ADS_PER_PAGE)
    start_idx = (page - 1) * ADS_PER_PAGE
    end_idx = min(start_idx + ADS_PER_PAGE, total_ads)

    page_ads = ads[start_idx:end_idx]

    header_text = (
        f"📋 <b>Advertisements</b>\n"
        f"Page {page}/{total_pages} | Total: {total_ads}\n"
        f"{'='*30}\n\n"
    )

    await message.answer(header_text)

    current_user_id = user_id or message.from_user.id

    for i, ad in enumerate(page_ads, start=start_idx + 1):
        await send_single_ad(message, ad, i, current_user_id)

    nav_keyboard = get_ads_navigation_keyboard(page, total_pages)
    await message.answer("📑 Navigation:", reply_markup=nav_keyboard)


async def send_single_ad(
    message: Message, ad: dict, ad_number: int, current_user_id: int
) -> None:
    """
    Sends a single advertisement with action buttons.

    Args:
        message: Message object
        ad: Advertisement data
        ad_number: Sequential number of the ad
        current_user_id: ID of current user viewing the ad
    """
    ad_id = ad["id"]
    ad_type = ad["type"]
    likes = ad.get("likes", 0)
    owner_id = ad["user_id"]

    keyboard = get_ad_actions_keyboard(ad_id, current_user_id, owner_id)

    header = f"#{ad_number} | ❤️ {likes} | Type: {ad_type.upper()}"

    try:
        if ad_type == "text":
            content = ad.get("content", "No content")
            await message.answer(
                f"📝 <b>{header}</b>\n\n{content}", reply_markup=keyboard
            )

        elif ad_type == "photo":
            file_id = ad.get("file_id", "")
            caption = ad.get("caption", "")

            caption_text = f"📸 <b>{header}</b>"
            if caption:
                caption_text += f"\n\n{caption}"

            await message.answer_photo(
                photo=file_id, caption=caption_text, reply_markup=keyboard
            )

        elif ad_type in ["audio", "voice"]:
            file_id = ad.get("file_id", "")
            caption = ad.get("caption", "")

            caption_text = f"🎵 <b>{header}</b>"
            if caption:
                caption_text += f"\n\n{caption}"

            if ad_type == "audio":
                await message.answer_audio(
                    audio=file_id, caption=caption_text, reply_markup=keyboard
                )
            else:
                await message.answer_voice(
                    voice=file_id, caption=caption_text, reply_markup=keyboard
                )

    except TelegramBadRequest as e:
        logger.error(f"Failed to send ad {ad_id}: {e}")
        await message.answer(
            f"❌ <b>Ad #{ad_number} - Error</b>\n\n"
            f"Failed to load this advertisement.\n"
            f"Type: {ad_type} | Likes: ❤️ {likes}",
            reply_markup=keyboard,
        )


@router.callback_query(F.data.startswith("like_ad:"))
async def like_ad_callback(callback: CallbackQuery) -> None:
    """
    Handles like button press for advertisements.
    """
    ad_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    success, message_text = like_ad(ad_id, user_id)

    if success:
        ad = get_ad_by_id(ad_id)
        if ad:
            await callback.answer(f"❤️ {message_text}", show_alert=True)

            new_keyboard = get_ad_actions_keyboard(
                ad_id, callback.from_user.id, ad["user_id"]
            )

            if callback.message.caption:
                new_caption = callback.message.caption
                import re

                pattern = r"❤️ \d+"
                new_caption = re.sub(pattern, f"❤️ {ad['likes']}", new_caption)

                try:
                    await callback.message.edit_caption(
                        caption=new_caption, reply_markup=new_keyboard
                    )
                except TelegramBadRequest:
                    pass
            else:
                new_text = callback.message.text
                import re

                pattern = r"❤️ \d+"
                new_text = re.sub(pattern, f"❤️ {ad['likes']}", new_text)

                try:
                    await callback.message.edit_text(
                        text=new_text, reply_markup=new_keyboard
                    )
                except TelegramBadRequest:
                    pass
        else:
            await callback.answer("❌ Advertisement not found", show_alert=True)
    else:
        await callback.answer(f"❌ {message_text}", show_alert=True)


@router.callback_query(F.data.startswith("delete_ad:"))
async def delete_ad_callback(callback: CallbackQuery) -> None:
    """
    Handles delete button press for advertisements.
    Only works for ad owners.
    """
    ad_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    success = delete_ad(ad_id, user_id)

    if success:
        await callback.answer("🗑️ Advertisement deleted successfully!", show_alert=True)

        try:
            await callback.message.delete()
            logger.info(
                f"Ad message {callback.message.message_id} deleted by user {user_id}"
            )
        except TelegramBadRequest as e:
            logger.error(f"Failed to delete message {callback.message.message_id}: {e}")
            await callback.message.edit_text(
                "🗑️ <b>This advertisement has been deleted.</b>"
            )
    else:
        await callback.answer(
            "❌ Failed to delete advertisement. You can only delete your own ads.",
            show_alert=True,
        )


@router.callback_query(F.data == "current_page")
async def current_page_callback(callback: CallbackQuery) -> None:
    """
    Handles current page button press (does nothing, just shows current page).
    """
    await callback.answer("You are currently viewing this page")


@router.callback_query(F.data.startswith("page:"))
async def page_navigation_callback(callback: CallbackQuery) -> None:
    """
    Handles page navigation button press.
    """
    page = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    # Edit the original message to show new page
    await callback.message.edit_text("Loading...")
    await show_ads_page(callback.message, page=page, user_id=user_id)
    await callback.answer()
