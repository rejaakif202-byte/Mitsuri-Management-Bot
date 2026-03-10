import asyncio
import re

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired


# ---------------- TIME PARSER ---------------- #

def parse_time(time_str):
    match = re.match(r"(\d+)([smhd])", time_str.lower())
    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    if unit == "s":
        return value
    elif unit == "m":
        return value * 60
    elif unit == "h":
        return value * 3600
    elif unit == "d":
        return value * 86400


# ---------------- USER FETCH ---------------- #

async def get_target_user(client, message: Message):

    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id

    elif len(message.command) > 1:
        user = message.command[1]

        if user.startswith("@"):
            data = await client.get_users(user)
            user_id = data.id
        else:
            user_id = int(user)

    return user_id


# ---------------- ADMIN CHECK ---------------- #

async def admin_check(client, message: Message):

    member = await client.get_chat_member(message.chat.id, message.from_user.id)

    if member.status not in ["administrator", "creator"]:
        await message.reply_text("You are not allowed to use this command.")
        return False

    bot = await client.get_chat_member(message.chat.id, "me")

    if bot.status != "administrator":
        await message.reply_text("I don't have enough permissions to ban users.")
        return False

    return True


# ---------------- BAN ---------------- #

@Client.on_message(filters.command("ban") & filters.group)
async def ban_user(client: Client, message: Message):

    if not await admin_check(client, message):
        return

    user_id = await get_target_user(client, message)

    if not user_id:
        return await message.reply_text("Reply to a user or give a username/user_id.")

    try:
        target = await client.get_chat_member(message.chat.id, user_id)
    except:
        return await message.reply_text("this user is no longer exist here")

    if target.status in ["administrator", "creator"]:
        return await message.reply_text("I can't ban an admin.")

    try:
        await client.ban_chat_member(message.chat.id, user_id)
    except ChatAdminRequired:
        return await message.reply_text("I don't have enough permissions to ban users.")

    user = await client.get_users(user_id)

    await message.reply_text(f"{user.mention} is now banned from the chat")


# ---------------- UNBAN ---------------- #

@Client.on_message(filters.command("unban") & filters.group)
async def unban_user(client: Client, message: Message):

    if not await admin_check(client, message):
        return

    user_id = await get_target_user(client, message)

    if not user_id:
        return await message.reply_text("Reply to a user or give a username/user_id.")

    await client.unban_chat_member(message.chat.id, user_id)

    user = await client.get_users(user_id)

    await message.reply_text(f"{user.mention} is now unbanned from the chat")


# ---------------- SILENT BAN ---------------- #

@Client.on_message(filters.command("sban") & filters.group)
async def silent_ban(client: Client, message: Message):

    if not await admin_check(client, message):
        return

    user_id = await get_target_user(client, message)

    if not user_id:
        return

    try:
        target = await client.get_chat_member(message.chat.id, user_id)
    except:
        return

    if target.status in ["administrator", "creator"]:
        return

    await client.ban_chat_member(message.chat.id, user_id)

    # No message (silent)


# ---------------- DELETE BAN ---------------- #

@Client.on_message(filters.command("dban") & filters.group)
async def delete_ban(client: Client, message: Message):

    if not await admin_check(client, message):
        return

    if not message.reply_to_message:
        return await message.reply_text("Reply to a user's message to dban.")

    user_id = message.reply_to_message.from_user.id

    try:
        target = await client.get_chat_member(message.chat.id, user_id)
    except:
        return await message.reply_text("this user is no longer exist here")

    if target.status in ["administrator", "creator"]:
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

    if not await admin_check(client, message):
        return

    if message.reply_to_message:
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

    try:
        target = await client.get_chat_member(message.chat.id, user_id)
    except:
        return await message.reply_text("this user is no longer exist here")

    if target.status in ["administrator", "creator"]:
        return await message.reply_text("I can't ban an admin.")

    await client.ban_chat_member(message.chat.id, user_id)

    user = await client.get_users(user_id)

    await message.reply_text(
        f"{user.mention} is banned for {time_str}"
    )

    await asyncio.sleep(seconds)

    await client.unban_chat_member(message.chat.id, user_id)

    await message.reply_text(
        f"{user.mention} is now unbanned from the chat"
  )
