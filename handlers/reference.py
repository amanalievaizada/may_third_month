import sqlite3
import binascii
import os

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, user
from aiogram.utils.deep_linking import create_start_link

from config import bot
from config import ADMIN_ID, MEDIA_PATH
from const import PROFILE_TEXT
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.start import start_menu_keyboard
from keyboards.reference import reference_menu_keyboard

router = Router()


@router.callback_query(lambda call: call.data == "reference_menu")
async def reference_menu(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Hi,this is a reference menu\n"
             "u can create reference link,share with your friends\n"
             "we will send ur account wallet 100 points",

        reply_markup=await reference_menu_keyboard()
    )


@router.callback_query(lambda call: call.data == "reference_link")
async def reference_link_creation(call: types.CallbackQuery,
                                   db=AsyncDatabase()):
    user = await db.execute_query(
        query=sql_queries.SELECT_USER_QUERY,
        params=(

            call.from_user.id,
        ),
        fetch="one",
    )
    if user is None:
        token = binascii.hexlify(os.urandom(8)).decode()
        print(token)
        link = await create_start_link(bot=bot, payload='token')
        print(link)

        print(user)

        await db.execute_query(
           query=sql_queries.UPDATE_USER_LINK_QUERY,
           params=(
               link,
               call.from_user.id,
           ),
           fetch="none"
       )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=link,
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=user['REFERENCE_LINK']
        )


@router.callback_query(lambda call: call.data == "reference_balance")
async def view_balance(call: types.CallbackQuery,
                                   db=AsyncDatabase()):
    user1= await db.execute_query(
        query=sql_queries.SELECT_USER_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch="one"
    )
    await bot.send_message(
       chat_id=call.from_user.id,
       text=f"ur balance:{user1['balance']}"
    )
