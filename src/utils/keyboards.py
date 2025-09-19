from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="📝 Create advertisement", callback_data="create_ad"
            )
        ],
        [InlineKeyboardButton(text="📋 List advertisements", callback_data="list_ads")],
        [InlineKeyboardButton(text="❓ Help", callback_data="help")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_confirm_text_keyboard() -> InlineKeyboardMarkup:
    """
    Creates the keyboard for confirming text.

    Returns:
        InlineKeyboardMarkup: The keyboard for confirming text
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="✅ Save as advertisement", callback_data="confirm_text_ad"
            ),
            InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_text_ad"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_photo_description_keyboard() -> InlineKeyboardMarkup:
    """
    Creates the keyboard for adding a photo description.

    Returns:
        InlineKeyboardMarkup: The keyboard for adding a photo description
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="📝 Add description", callback_data="add_photo_description"
            ),
            InlineKeyboardButton(
                text="✅ Save without description",
                callback_data="save_photo_no_desc",
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_ad_actions_keyboard(
    ad_id: int, user_id: int, ad_owner_id: int
) -> InlineKeyboardMarkup:
    """
    Creates the keyboard for actions on an advertisement.
    """
    from utils.logger import get_logger

    logger = get_logger(__name__)

    logger.info(
        f"Creating keyboard for ad {ad_id}: user_id={user_id}, owner_id={ad_owner_id}"
    )

    keyboard = [[InlineKeyboardButton(text="❤️ Like", callback_data=f"like_ad:{ad_id}")]]

    if user_id == ad_owner_id:
        keyboard.append(
            [InlineKeyboardButton(text="🗑 Delete", callback_data=f"delete_ad:{ad_id}")]
        )
        logger.info(f"Added delete button for owner {user_id}")
    else:
        logger.info(f"No delete button: user {user_id} != owner {ad_owner_id}")

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_ads_navigation_keyboard(
    current_page: int, total_pages: int
) -> InlineKeyboardMarkup:
    """
    Creates the keyboard for navigation between advertisement pages.

    Args:
        current_page: Current page
        total_pages: Total number of pages

    Returns:
        InlineKeyboardMarkup: The keyboard for navigation
    """
    keyboard = []

    if total_pages > 1:
        nav_buttons = []

        if current_page > 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Back", callback_data=f"page:{current_page-1}"
                )
            )

        nav_buttons.append(
            InlineKeyboardButton(
                text=f"{current_page}/{total_pages}", callback_data="current_page"
            )
        )

        if current_page < total_pages:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="Next ➡️", callback_data=f"page:{current_page+1}"
                )
            )

        keyboard.append(nav_buttons)

    keyboard.append(
        [InlineKeyboardButton(text="🏠 Main menu", callback_data="main_menu")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
