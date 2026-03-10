from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.welcome_db import (
    set_welcome,
    get_welcome,
    reset_welcome,
    toggle_welcome
)

from utils.permissions import is_admin


# /welcome command

@Client.on_message(filters.command("welcome") & filters.group)
async def welcome_settings(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text(
            "<b>You are not allowed to use this command</b>"
        )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ON", callback_data="welcome_on"),
            InlineKeyboardButton("OFF", callback_data="welcome_off")
        ]
    ])

    await message.reply_text(
        "<b>Set your welcome here</b>",
        reply_markup=buttons
    )


# button handler

@Client.on_callback_query(filters.regex("welcome_"))
async def welcome_toggle(client, query):

    chat_id = query.message.chat.id

    if query.data == "welcome_on":

        await toggle_welcome(chat_id, True)

        await query.message.edit_text(
            "<b>Welcome system enabled</b>"
        )

    elif query.data == "welcome_off":

        await toggle_welcome(chat_id, False)

        await query.message.edit_text(
            "<b>Welcome system disabled</b>"
        )


# /setwelcome

@Client.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome_message(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text(
            "<b>You are not allowed to use this command</b>"
        )

    if not message.reply_to_message:
        return await message.reply_text(
            "<b>Reply to a message to set welcome</b>"
        )

    reply = message.reply_to_message

    await set_welcome(message.chat.id, reply)

    await message.reply_text(
        "<b>Custom welcome message saved</b>"
    )


# /resetwelcome

@Client.on_message(filters.command("resetwelcome") & filters.group)
async def reset_welcome_message(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text(
            "<b>You are not allowed to use this command</b>"
        )

    await reset_welcome(message.chat.id)

    await message.reply_text(
        "<b>Welcome message reset to default</b>"
    )


# join event

@Client.on_message(filters.new_chat_members)
async def welcome_new_user(client, message: Message):

    data = await get_welcome(message.chat.id)

    if not data["enabled"]:
        return

    for user in message.new_chat_members:

        text = data["text"] me 

        text = text.replace("{first_name}", user.first_name or "")
        text = text.replace("{Last_name}", user.last_name or "")
        text = text.replace("{Username}", f"@{user.username}" if user.username else "None")
        text = text.replace("{Uid}", str(user.id))
        text = text.replace("{Chatname}", message.chat.title)
        text = text.replace("{Mention}", user.mention)

        await message.reply_text(text)
