# handlers/callbacks.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.keyboards import get_main_menu_keyboard
from utils.logger import get_logger

router = Router()
logger = get_logger(__name__)


@router.callback_query(F.data == "create_ad")
async def create_ad_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Handles 'Create advertisement' inline button press.
    """
    await state.clear()

    from handlers.add import command_add_handler

    await command_add_handler(callback.message)
    await callback.answer()
    logger.info(f"Create ad accessed by user {callback.from_user.id}")


@router.callback_query(F.data == "list_ads")
async def list_ads_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Handles 'List advertisements' inline button press.
    """
    await state.clear()

    from handlers.list import show_ads_page

    await show_ads_page(callback.message, page=1, user_id=callback.from_user.id)
    await callback.answer()
    logger.info(f"List ads accessed by user {callback.from_user.id}")


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Handles 'Help' inline button press.
    """
    await state.clear()

    from handlers.help import command_help_handler

    await command_help_handler(callback.message)
    await callback.answer()
    logger.info(f"Help accessed by user {callback.from_user.id}")


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Handles main menu button press from inline keyboards.
    Clears any active states and shows main menu.
    """
    await state.clear()

    await callback.message.answer(
        "🏠 <b>Main Menu</b>\n\n" "Choose an action from the buttons below:",
        reply_markup=get_main_menu_keyboard(),
    )

    await callback.answer()
    logger.info(f"Main menu accessed by user {callback.from_user.id}")


@router.callback_query(F.data == "current_page")
async def current_page_callback(callback: CallbackQuery) -> None:
    """
    Handles current page button press (does nothing, just shows current page).
    """
    await callback.answer("You are currently viewing this page")


@router.callback_query()
async def unhandled_callback(callback: CallbackQuery) -> None:
    """
    Handles unrecognized callback queries.
    """
    logger.warning(
        f"Unhandled callback query: {callback.data} from user {callback.from_user.id}"
    )
    await callback.answer("❌ Unknown action", show_alert=True)
