from email import message

from aiogram import Router,types
from aiogram .filters import Command
from aiogram.types import InlineKeyboardMarkup

from config import bot
from config import ADMIN_ID,MEDIA_PATH
from const import  START_MENU_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.start import start_menu_keyboard

router = Router()

@router.message(Command("start"))
async def start_menu(message: types.Message,
                     db=AsyncDatabase()):
    print(message)
    await db.execute_query(
        query=sql_queries.INSERT_USER_QUERY,
        params=(
            None,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,

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

@router.message(lambda message:message.text == "hoho")
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
        USERS=await db.execute_query(query=queries.SELECT_USER,fetch='all')

    await bot.send_message(message.from_user.id,
          chat_id=message.from_user.id,
          text= f'{USERS}'
                           )
