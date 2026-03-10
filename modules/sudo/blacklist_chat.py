from pyrogram import Client, filters
from pyrogram.types import Message

from database.blacklist_chat_db import (
    add_blacklist_chat,
    remove_blacklist_chat,
    get_blacklist_chats,
    is_blacklisted_chat
)

from utils.permissions import is_sudo


# ---------------- BLACKLIST CHAT ---------------- #

@Client.on_message(filters.command("blacklistchat"))
async def blacklist_chat(client: Client, message: Message):

    if not await is_sudo(client, message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Give a chat id to blacklist</b>"
        )

    chat_id = int(message.command[1])

    try:
        chat = await client.get_chat(chat_id)
        title = chat.title
    except:
        title = "Unknown Chat"

    await add_blacklist_chat(chat_id, title)

    await message.reply_text(
        "<b>This chat has been blacklisted</b>"
    )

    try:
        await client.send_message(
            chat_id,
            "<b>This chat is blacklisted. I cannot stay here.</b>"
        )
        await client.leave_chat(chat_id)
    except:
        pass


# ---------------- WHITELIST CHAT ---------------- #

@Client.on_message(filters.command("whitelistchat"))
async def whitelist_chat(client: Client, message: Message):

    if not await is_sudo(client, message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Give a chat id to whitelist</b>"
        )

    chat_id = int(message.command[1])

    await remove_blacklist_chat(chat_id)

    await message.reply_text(
        "<b>This chat has been removed from blacklist</b>"
    )


# ---------------- SHOW BLACKLIST CHATS ---------------- #

@Client.on_message(filters.command("allblacklistchats"))
async def show_blacklist_chats(client: Client, message: Message):

    if not await is_sudo(client, message.from_user.id):
        return

    chats = await get_blacklist_chats()

    if not chats:
        return await message.reply_text(
            "<b>No blacklisted chats</b>"
        )

    text = "<b>Blacklisted Chats:</b>\n\n"

    for i, chat in enumerate(chats, 1):

        title = chat["title"]
        chat_id = chat["chat_id"]

        text += f"{i}. {title} | <code>{chat_id}</code>\n"

    await message.reply_text(text)


# ---------------- AUTO LEAVE PROTECTION ---------------- #

@Client.on_message(filters.new_chat_members)
async def auto_leave_blacklisted(client, message):

    chat_id = message.chat.id

    if await is_blacklisted_chat(chat_id):

        try:
            await client.send_message(
                chat_id,
                "<b>This chat is blacklisted. I cannot stay here.</b>"
            )
        except:
            pass

        await client.leave_chat(chat_id)
