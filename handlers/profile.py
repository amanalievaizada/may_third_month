import random
import re
import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from config import bot
from config import ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.profile import my_profile_keyboard
from keyboards.start import start_menu_keyboard
from keyboards.like_dislike import like_dislike_keyboard

router = Router()


@router.callback_query(lambda call: call.data == "my_profile")
async def my_profiles_call(call: types.CallbackQuery,
                               db=AsyncDatabase()):
    profile = await db.execute_query(
        query=sql_queries.SELECT_PROFILE_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    if profile:
        print(profile)
        photo = types.FSInputFile(profile["PHOTO"])
        print(profile['PHOTO'])
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=PROFILE_TEXT.format(
                telegram_id=profile["TELEGRAM_ID"],
                nickname=profile['NICKNAME'],
                bio=profile['BIO'],
                favorite_music=profile['FAVORITE_MUSIC'],
                favorite_colour=profile['FAVORITE_COLOUR'],


            ),
            reply_markup=await my_profile_keyboard()
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="u have not registered"
        ,
    )


