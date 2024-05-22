from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start_menu_keyboard():
    registration_button = InlineKeyboardButton(
        text="Registration",
        callback_data="registration"
    )
    my_profile_button = InlineKeyboardButton(
        text="My profile",
        callback_data="my_profile"
    )

    profiles_button = InlineKeyboardButton(
        text="View_profiles",
        callback_data="View_profiles"
    )

    reference_button = InlineKeyboardButton(
        text="reference menu",
        callback_data="reference_menu"
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [my_profile_button],
            [profiles_button],
            [reference_button],
        ]
    )
    return markup
