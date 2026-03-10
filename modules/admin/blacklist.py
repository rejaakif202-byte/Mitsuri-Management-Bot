from pyrogram import Client, filters
from pyrogram.types import Message

from database.blacklist_db import (
    add_blacklist,
    remove_blacklist,
    get_blacklist
)

from utils.permissions import is_admin
from database.approve_db import is_approved


# ADD BLACKLIST

@Client.on_message(filters.command("blacklist") & filters.group)
async def blacklist_word(client: Client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text("<b>You are not allowed to use this command</b>")

    if len(message.command) < 2:
        return await message.reply_text("<b>Give a word or item to blacklist</b>")

    word = message.text.split(None, 1)[1]

    await add_blacklist(message.chat.id, word)

    await message.reply_text(f"<b>{word} has been added to blacklist</b>")


# REMOVE BLACKLIST

@Client.on_message(filters.command("unblacklist") & filters.group)
async def unblacklist_word(client: Client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text("<b>You are not allowed to use this command</b>")

    if len(message.command) < 2:
        return await message.reply_text("<b>Give a word to remove from blacklist</b>")

    word = message.text.split(None, 1)[1]

    await remove_blacklist(message.chat.id, word)

    await message.reply_text(f"<b>{word} removed from blacklist</b>")


# SHOW BLACKLIST

@Client.on_message(filters.command("allblacklist") & filters.group)
async def show_blacklist(client: Client, message: Message):

    words = await get_blacklist(message.chat.id)

    if not words:
        return await message.reply_text("<b>No blacklisted items in this chat</b>")

    text = "<b>Blacklisted items in this chat:</b>\n\n"

    for i, word in enumerate(words, 1):
        text += f"{i}. {word}\n"

    await message.reply_text(text)


# MESSAGE CHECKER

@Client.on_message(filters.group)
async def check_blacklist(client: Client, message: Message):

    if not message.text:
        return

    if await is_admin(client, message):
        return

    if await is_approved(message.chat.id, message.from_user.id):
        return

    words = await get_blacklist(message.chat.id)

    if not words:
        return

    text = message.text.lower()

    for word in words:

        if word.lower() in text:

            try:
                await message.delete()
            except:
                pass

            break
