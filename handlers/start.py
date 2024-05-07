from aiogram import Router,types
from aiogram .filters import Command


from config import bot
from config import ADMIN_ID
from database import sql_queries
from database.a_db import AsyncDatabase

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
        fetch="all"
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"hello {message.from_user.first_name}"

    )

@router.message(lambda message:message.text == "hoho")
async def hoho(message: types.Message,
                       db=AsyncDatabase()):
    if message.from_users.id(ADMIN_ID) == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_users.id,
            text=f"Hi admin{message.from_user.first_name}"

        )
    else:
        await bot.send_message(
            chat_id=message.from_users.id,
            text=f"Hi you are not admin{message.from_user.first_name}"
    )