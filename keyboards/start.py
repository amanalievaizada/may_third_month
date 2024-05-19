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
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [my_profile_button],
            [profiles_button]
        ]
    )
    return markup
