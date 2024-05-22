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
from keyboards.start import start_menu_keyboard
from keyboards.like_dislike import like_dislike_keyboard

router = Router()


@router.callback_query(lambda call: call.data == "View_profiles")
async def random_profiles_call(call: types.CallbackQuery,
                               db=AsyncDatabase()):
    if call.message.caption.startswith("Nickname"):
        await call.message.delete()
    profiles = await db.execute_query(
        query=sql_queries.SELECT_ALL_PROFILES,
        params=(
            call.from_user.id,
            call.from_user.id,
        ),
        fetch='all'
    )
    random_profile = random.choice(profiles)
    print(profiles)
    print(random_profile)
    photo = types.FSInputFile(random_profile["PHOTO"])
    await bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=random_profile['NICKNAME'],
            bio=random_profile['BIO'],
        ),
        reply_markup=await like_dislike_keyboard(tg_id=random_profile["TELEGRAM_ID"])

    )


@router.callback_query(lambda call: "like_" in call.data)
async def like_detect_call(call: types.CallbackQuery,
                           db=AsyncDatabase(), ):
    # print(call.data.replace("like_", ""))
    #print(call.data[5:])
    owner_tg_id = (re.sub('like', '', call.data))

    await db.execute_query(
        query=sql_queries.INSERT_LIKE_QUERY,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            1
        ),
        fetch='none'
    )

    await random_profiles_call(call=call)


@router.callback_query(lambda call: "dislike" in call.data)
async def dislike_detect_call(call: types.CallbackQuery,
                           db=AsyncDatabase(), ):
    # print(call.data.replace("dislike", ""))
    #print(call.data[5:])
    owner_tg_id = (re.sub('dislike', '', call.data))

    await db.execute_query(
        query=sql_queries.INSERT_LIKE_QUERY,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            -1
        ),
        fetch='none'
    )

    await random_profiles_call(call=call)
