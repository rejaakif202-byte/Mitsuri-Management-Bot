from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.goodbye_db import (
    set_goodbye,
    get_goodbye,
    reset_goodbye,
    toggle_goodbye
)

from utils.permissions import is_admin


# /goodbye command

@Client.on_message(filters.command("goodbye") & filters.group)
async def goodbye_settings(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text(
            "<b>You are not allowed to use this command</b>"
        )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ON", callback_data="goodbye_on"),
            InlineKeyboardButton("OFF", callback_data="goodbye_off")
        ]
    ])

    await message.reply_text(
        "<b>Set your goodbye here</b>",
        reply_markup=buttons
    )


# button handler

@Client.on_callback_query(filters.regex("goodbye_"))
async def goodbye_toggle(client, query):

    chat_id = query.message.chat.id

    if query.data == "goodbye_on":

        await toggle_goodbye(chat_id, True)

        await query.message.edit_text(
            "<b>Goodbye system enabled</b>"
        )

    elif query.data == "goodbye_off":

        await toggle_goodbye(chat_id, False)

        await query.message.edit_text(
            "<b>Goodbye system disabled</b>"
        )


# /setgoodbye

@Client.on_message(filters.command("setgoodbye") & filters.group)
async def set_goodbye_message(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text(
            "<b>You are not allowed to use this command</b>"
        )

    if not message.reply_to_message:
        return await message.reply_text(
            "<b>Reply to a message to set goodbye</b>"
        )

    reply = message.reply_to_message

    await set_goodbye(message.chat.id, reply)

    await message.reply_text(
        "<b>Custom goodbye message saved</b>"
    )


# /resetgoodbye

@Client.on_message(filters.command("resetgoodbye") & filters.group)
async def reset_goodbye_message(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text(
            "<b>You are not allowed to use this command</b>"
        )

    await reset_goodbye(message.chat.id)

    await message.reply_text(
        "<b>Goodbye message reset to default</b>"
    )


# leave event

@Client.on_message(filters.left_chat_member)
async def goodbye_user(client, message: Message):

    data = await get_goodbye(message.chat.id)

    if not data["enabled"]:
        return

    user = message.left_chat_member

    text = data["text"]

    text = text.replace("{first_name}", user.first_name or "")
    text = text.replace("{Last_name}", user.last_name or "")
    text = text.replace("{Username}", f"@{user.username}" if user.username else "None")
    text = text.replace("{Uid}", str(user.id))
    text = text.replace("{Chatname}", message.chat.title)
    text = text.replace("{Mention}", user.mention)

    await message.reply_text(text)
