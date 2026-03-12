from pyrogram import Client, filters
from database.users_db import add_user, add_chat


# Save private users

@Client.on_message(filters.private)
async def save_private_user(client, message):

    if message.from_user:
        await add_user(message.from_user.id)


# Save group users and chats

@Client.on_message(filters.group)
async def save_group_user(client, message):

    if message.from_user:
        await add_user(message.from_user.id)

    if message.chat:
        await add_chat(message.chat.id)
