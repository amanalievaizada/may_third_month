import sqlite3
from email import message

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.deep_linking import create_start_link

from config import bot
from config import ADMIN_ID, MEDIA_PATH
from const import START_MENU_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.start import start_menu_keyboard

router = Router()


@router.message(Command("start"))
async def start_menu(message: types.Message,
                     db=AsyncDatabase()):
    command = message.text
    token = command.split()
    print(token)
    if len(token) > 1:
        await process_reference_link(token[1],
                                     message)

    await db.execute_query(
        query=sql_queries.INSERT_USER_QUERY,
        params=(
            None,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            None,
            0

        ),
        fetch="none"
    )
    animation_file = types.FSInputFile(MEDIA_PATH + "botbot.gif")
    await bot.send_animation(
        chat_id=message.from_user.id,
        animation=animation_file,
        caption=START_MENU_TEXT.format(
            user=message.from_user.first_name,
        ),
        reply_markup=await start_menu_keyboard()
    )


async def process_reference_link(token, message, db=AsyncDatabase()):
    link = await create_start_link(bot=bot, payload=token)
    owner = await db.execute_query(
        query=sql_queries.SELECT_USER_BY_LINK_QUERY,
        params=(
            link,
        ),
        fetch='one'
    )

    if owner['TELEGRAM_ID'] == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="U can not use ur own link"
        )
        return
    try:
        await db.execute_query(
            query=sql_queries.INSERT_REFERENCE_USER_QUERY,
            params=(
                None,
                owner['TELEGRAM_ID'],
                message.from_user.id
            ),
            fetch='none'
        )
        await db.execute_query(
            query=sql_queries.UPDATE_USER_BALANCE_QUERY,
            params=(
                owner['TELEGRAM_ID'],
            ),
            fetch='none'
        )
        await bot.send_message(
            chat_id=owner['TELEGRAM_ID'],
            text='U got new reference user\n'
                 'Congrats'
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='U have used this link '
        )


@router.message(lambda message: message.text == "hoho")
async def hoho(message: types.Message,
               db=AsyncDatabase(), queries=None):
    if message.from_users.id(ADMIN_ID) == int(ADMIN_ID):
        await bot.send_message(
            chat_id=message.from_users.id,
            text=f"Hi admin{message.from_user.first_name}"

        )
        await bot.send_message(
            chat_id=message.from_users.id,
            text=f"Hi you are not admin{message.from_user.first_name}"

        )
        USERS = await db.execute_query(query=queries.SELECT_USER, fetch='all')

    await bot.send_message(message.from_user.id,
                           chat_id=message.from_user.id,
                           text=f'{USERS}'
                           )
