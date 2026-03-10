from pyrogram import Client, filters

from database.users_db import add_user


@Client.on_message(filters.private)
async def save_user(client, message):

    if message.from_user:

        await add_user(message.from_user.id)
