import asyncio
import re

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired

from utils.permissions import is_admin


# ---------------- TIME PARSER ---------------- #

def parse_time(time_str):

    match = re.match(r"(\d+)([smhd])", time_str.lower())

    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    if unit == "d":
        return value * 86400


# ---------------- TARGET USER ---------------- #

async def get_target_user(client, message: Message):

    if message.reply_to_message:
        return message.reply_to_message.from_user.id

    if len(message.command) > 1:

        user = message.command[1]

        if user.startswith("@"):
            data = await client.get_users(user)
            return data.id

        return int(user)

    return None


# ---------------- BAN ---------------- #

@Client.on_message(filters.command("ban") & filters.group)
async def ban_user(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    user_id = await get_target_user(client, message)

    if not user_id:
        return await message.reply_text("Reply to a user or give username/user_id.")

    try:
        member = await client.get_chat_member(message.chat.id, user_id)
    except:
        return await message.reply_text("User not found in this chat.")

    if member.status in ["administrator", "creator"]:
        return await message.reply_text("I can't ban an admin.")

    try:
        await client.ban_chat_member(message.chat.id, user_id)
    except ChatAdminRequired:
        return await message.reply_text("I need ban permissions.")

    user = await client.get_users(user_id)

    await message.reply_text(f"{user.mention} is banned from the chat.")


# ---------------- UNBAN ---------------- #

@Client.on_message(filters.command("unban") & filters.group)
async def unban_user(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    user_id = await get_target_user(client, message)

    if not user_id:
        return await message.reply_text("Reply to a user or give username/user_id.")

    await client.unban_chat_member(message.chat.id, user_id)

    user = await client.get_users(user_id)

    await message.reply_text(f"{user.mention} is now unbanned.")


# ---------------- SILENT BAN ---------------- #

@Client.on_message(filters.command("sban") & filters.group)
async def silent_ban(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    user_id = await get_target_user(client, message)

    if not user_id:
        return

    try:
        member = await client.get_chat_member(message.chat.id, user_id)
    except:
        return

    if member.status in ["administrator", "creator"]:
        return

    await client.ban_chat_member(message.chat.id, user_id)


# ---------------- DELETE BAN ---------------- #

@Client.on_message(filters.command("dban") & filters.group)
async def delete_ban(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    if not message.reply_to_message:
        return await message.reply_text("Reply to a user message.")

    user_id = message.reply_to_message.from_user.id

    try:
        member = await client.get_chat_member(message.chat.id, user_id)
    except:
        return

    if member.status in ["administrator", "creator"]:
        return await message.reply_text("I can't ban an admin.")

    await client.ban_chat_member(message.chat.id, user_id)

    try:
        await message.reply_to_message.delete()
    except:
        pass

    try:
        await message.delete()
    except:
        pass


# ---------------- TEMP BAN ---------------- #

@Client.on_message(filters.command("tban") & filters.group)
async def temp_ban(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    if message.reply_to_message:

        if len(message.command) < 2:
            return await message.reply_text("Usage: /tban 10m (reply to user)")

        user_id = message.reply_to_message.from_user.id
        time_str = message.command[1]

    else:

        if len(message.command) < 3:
            return await message.reply_text("Usage: /tban @user 10m")

        user = message.command[1]
        time_str = message.command[2]

        if user.startswith("@"):
            data = await client.get_users(user)
            user_id = data.id
        else:
            user_id = int(user)

    seconds = parse_time(time_str)

    if not seconds:
        return await message.reply_text("Invalid time format.")

    member = await client.get_chat_member(message.chat.id, user_id)

    if member.status in ["administrator", "creator"]:
        return await message.reply_text("I can't ban an admin.")

    await client.ban_chat_member(message.chat.id, user_id)

    user = await client.get_users(user_id)

    await message.reply_text(f"{user.mention} banned for {time_str}")

    await asyncio.sleep(seconds)

    await client.unban_chat_member(message.chat.id, user_id)

    await message.reply_text(f"{user.mention} is now unbanned.")
