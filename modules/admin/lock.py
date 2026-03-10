from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from utils.permissions import is_admin
from database.locks_db import add_lock, remove_lock, get_locks
from database.approve_db import is_approved


LOCK_TYPES = [
"album","anonchannel","audio","bot","command",
"contact","document","onlyemoji","gif","text",
"url","media","invitelink","sticker","video"
]


# LOCK COMMAND

@Client.on_message(filters.command("lock") & filters.group)
async def lock_type(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text("<b>You are not allowed to use this command</b>")

    if len(message.command) < 2:
        return await message.reply_text("<b>Give a lock type</b>")

    lock = message.command[1].lower()

    if lock == "all":
        for l in LOCK_TYPES:
            await add_lock(message.chat.id, l)

        return await message.reply_text("<b>All lock types enabled</b>")

    if lock not in LOCK_TYPES:
        return await message.reply_text("<b>Invalid lock type</b>")

    await add_lock(message.chat.id, lock)

    await message.reply_text(f"<b>{lock} locked in this chat</b>")


# UNLOCK COMMAND

@Client.on_message(filters.command("unlock") & filters.group)
async def unlock_type(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text("<b>You are not allowed to use this command</b>")

    if len(message.command) < 2:
        return await message.reply_text("<b>Give a lock type</b>")

    lock = message.command[1].lower()

    await remove_lock(message.chat.id, lock)

    await message.reply_text(f"<b>{lock} unlocked in this chat</b>")


# LOCKTYPES COMMAND

@Client.on_message(filters.command("locktypes") & filters.group)
async def locktypes(client, message: Message):

    buttons = []

    row = []
    for i, lock in enumerate(LOCK_TYPES, start=1):

        row.append(InlineKeyboardButton(lock, callback_data="lockinfo"))

        if i % 3 == 0:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    keyboard = InlineKeyboardMarkup(buttons)

    await message.reply_photo(
        photo="LOCK_IMAGE_URL",
        caption="<b>The available locktypes are:</b>",
        reply_markup=keyboard
    )
