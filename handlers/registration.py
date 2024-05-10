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

router = Router()


class RegistrationStates(StatesGroup):
    nickname = State()
    bio = State()
    favorite_music = State()
    favorite_colour = State()
    photo = State()


@router.callback_query(lambda call: call.data == "registration")
async def registration_start(call: types.CallbackQuery,
                             state: FSMContext,
                             db=AsyncDatabase()):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Send your Nickname,please!"
    )

    await state.set_state(RegistrationStates.nickname)


@router.message(RegistrationStates.nickname)
async def process_nickname(message: types.Message,
                           state: FSMContext):
    await state.update_data(nickname=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Please,tell me about your self"

    )
    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.bio)


@router.message(RegistrationStates.bio)
async def process_bio(message: types.Message,
                      state: FSMContext):
    await state.update_data(bio=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Please,send me your favorite music"

    )
    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.favorite_music)


@router.message(RegistrationStates.favorite_music)
async def process_favorite_music(message: types.Message,
                                 state: FSMContext):
    await state.update_data(favorite_music=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Please,write your favorite colour"

    )
    data = await state.update_data()
    print(data)
    await state.set_state(RegistrationStates.favorite_colour)


@router.message(RegistrationStates.favorite_colour)
async def process_favorite_colour(message: types.Message,
                                  state: FSMContext):
    await state.update_data(favorite_colour=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Please,send me your photo"

    )
    data = await state.update_data()
    print(data)
    await state.set_state(RegistrationStates.photo)


@router.message(RegistrationStates.photo)
async def process_photo(message: types.Message,
                        state: FSMContext,
                        db=AsyncDatabase()):
    file_id = message.photo[-1].file_id
    print(message.photo)
    file = await bot.get_file(file_id)
    file_path = file.file_path
    media_final_path = 'media/' + file_path
    print(media_final_path)
    print(file_path)
    print('media/' + file_path)
    await bot.download_file(
        file_path,
        'media/' + file_path
    )
    data = await state.get_data()
    photo = FSInputFile('media/' + file_path)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=data['nickname'],
            bio=data['bio'],
            favorite_music=data['favorite_music'],
            favorite_colour=data['favorite_colour'],
        )
    )

    await bot.send_message(
        chat_id=message.from_user.id,
        text="You have registered successfully"
    )

    await db.execute_query(
        query=sql_queries.INSERT_PROFILE_QUERY,
        params=(
            None,
            message.from_user.id,
            data['nickname'],
            data['bio'],
            data['favorite_music'],
            data['favorite_colour'],
            'media/' + file_path

        ),
        fetch="none"
    )

    await db.execute_query(
        query=sql_queries.SELECT_PROFILE_QUERY,
        params=(
            None,
            message.from_user.id,
            data['nickname'],
            data['bio'],
            data['favorite_music'],
            data['favorite_colour'],
            'media/' + file_path
        ),
        fetch='all'
    )

