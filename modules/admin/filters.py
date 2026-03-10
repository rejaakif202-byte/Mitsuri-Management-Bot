from pyrogram import Client, filters
from pyrogram.types import Message

from database.filters_db import (
    add_filter,
    remove_filter,
    remove_all_filters,
    get_filters
)

from utils.button_parser import parse_buttons
from utils.permissions import is_admin


@Client.on_message(filters.command("filter") & filters.group)
async def addfilter(client, message: Message):

    if not await is_admin(client, message):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/filter \"word\" reply message"
        )

    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to message to save filter"
        )

    word = message.command[1].lower()

    reply = message.reply_to_message

    text = reply.text or reply.caption

    buttons = None

    if text:
        text, buttons = parse_buttons(text)

    media = None

    if reply.photo:
        media = reply.photo.file_id

    elif reply.video:
        media = reply.video.file_id

    elif reply.document:
        media = reply.document.file_id

    await add_filter(
        message.chat.id,
        word,
        text,
        buttons,
        media
    )

    await message.reply_text(
        f"<b>Filter saved:</b> <code>{word}</code>"
    )


@Client.on_message(filters.command("stop") & filters.group)
async def stopfilter(client, message: Message):

    if not await is_admin(client, message):
        return

    if len(message.command) < 2:
        return

    word = message.command[1].lower()

    await remove_filter(message.chat.id, word)

    await message.reply_text(
        f"<b>Filter removed:</b> <code>{word}</code>"
    )


@Client.on_message(filters.command("stopall") & filters.group)
async def stopallfilters(client, message: Message):

    if not await is_admin(client, message):
        return

    await remove_all_filters(message.chat.id)

    await message.reply_text(
        "<b>All filters removed</b>"
    )


@Client.on_message(filters.command("filters") & filters.group)
async def listfilters(client, message: Message):

    data = await get_filters(message.chat.id)

    if not data:
        return await message.reply_text(
            "<b>No filters in this chat</b>"
        )

    text = "<b>Filters in this chat:</b>\n\n"

    for i, word in enumerate(data.keys(), 1):

        text += f"{i}. <b><code>{word}</code></b>\n"

    await message.reply_text(text)


@Client.on_message(filters.text & filters.group)
async def filterchecker(client, message: Message):

    data = await get_filters(message.chat.id)

    if not data:
        return

    text = message.text.lower()

    for word, info in data.items():

        if word in text:

            if info["media"]:

                await message.reply_photo(
                    info["media"],
                    caption=info["text"],
                    reply_markup=info["buttons"]
                )

            else:

                await message.reply_text(
                    info["text"],
                    reply_markup=info["buttons"]
                )

            break
