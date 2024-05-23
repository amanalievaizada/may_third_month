from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def reference_menu_keyboard():
    link_button = InlineKeyboardButton(
        text="Link",
        callback_data=f"reference_link"
    )
    balance_button = InlineKeyboardButton(
        text="balance",
        callback_data="reference_balance"
    )
    list_button = InlineKeyboardButton(
        text="list",
        callback_data="reference_list"
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [link_button],
            [balance_button],
            [list_button],

        ]
    )
    return markup

