import asyncio
import re

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database.warns_db import get_warns, add_warn, remove_warns, set_warn_limit, get_warn_limit


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


# ---------------- TARGET USER ---------------- #

async def get_target_user(client, message: Message):

    if message.reply_to_message:
        return message.reply_to_message.from_user.id

    if len(message.command) > 1:
        user = message.command[1]

        if user.startswith("@"):
            data = await client.get_users(user)
            return data.id
        else:
            return int(user)

    return None


# ---------------- WARN ---------------- #

@Client.on_message(filters.command("warn") & filters.group)
async def warn_user(client: Client, message: Message):

    user_id = await get_target_user(client, message)

    if not user_id:
        return await message.reply_text("<b>Reply to a user or give username/user_id</b>")

    warns = await add_warn(message.chat.id, user_id)

    limit = await get_warn_limit(message.chat.id)

    user = await client.get_users(user_id)

    if warns > limit:

        await client.ban_chat_member(message.chat.id, user_id)

        return await message.reply_text(
            f"<b>{user.mention} exceeded the warn limit and has been banned</b>"
        )

    await message.reply_text(
        f"<b>{user.mention} has been warned</b>\n<b>Warns: {warns}/{limit}</b>"
    )


# ---------------- SILENT WARN ---------------- #

@Client.on_message(filters.command("swarn") & filters.group)
async def silent_warn(client: Client, message: Message):

    user_id = await get_target_user(client, message)

    if not user_id:
        return

    warns = await add_warn(message.chat.id, user_id)

    limit = await get_warn_limit(message.chat.id)

    if warns > limit:
        await client.ban_chat_member(message.chat.id, user_id)


# ---------------- DELETE WARN ---------------- #

@Client.on_message(filters.command("dwarn") & filters.group)
async def delete_warn(client: Client, message: Message):

    if not message.reply_to_message:
        return await message.reply_text("<b>Reply to a user message</b>")

    user_id = message.reply_to_message.from_user.id

    warns = await add_warn(message.chat.id, user_id)

    limit = await get_warn_limit(message.chat.id)

    try:
        await message.reply_to_message.delete()
        await message.delete()
    except:
        pass

    if warns > limit:
        await client.ban_chat_member(message.chat.id, user_id)


# ---------------- TEMP WARN ---------------- #

@Client.on_message(filters.command("twarn") & filters.group)
async def temp_warn(client: Client, message: Message):

    if message.reply_to_message:

        user_id = message.reply_to_message.from_user.id
        time_str = message.command[1]

    else:

        if len(message.command) < 3:
            return await message.reply_text("<b>Usage: /twarn @user 10m</b>")

        user = message.command[1]
        time_str = message.command[2]

        if user.startswith("@"):
            data = await client.get_users(user)
            user_id = data.id
        else:
            user_id = int(user)

    seconds = parse_time(time_str)

    if not seconds:
        return await message.reply_text("<b>Invalid time format</b>")

    warns = await add_warn(message.chat.id, user_id)

    limit = await get_warn_limit(message.chat.id)

    user = await client.get_users(user_id)

    await message.reply_text(
        f"<b>{user.mention} has been warned temporarily</b>"
    )

    await asyncio.sleep(seconds)

    await remove_warns(message.chat.id, user_id)


# ---------------- UNWARN ---------------- #

@Client.on_message(filters.command("unwarn") & filters.group)
async def unwarn_user(client: Client, message: Message):

    user_id = await get_target_user(client, message)

    if not user_id:
        return await message.reply_text("<b>Reply to a user</b>")

    await remove_warns(message.chat.id, user_id)

    user = await client.get_users(user_id)

    await message.reply_text(
        f"<b>All warns removed from {user.mention}</b>"
    )


# ---------------- WARN LIMIT ---------------- #

@Client.on_message(filters.command("setwarnlimit") & filters.group)
async def warn_limit(client: Client, message: Message):

    limit = await get_warn_limit(message.chat.id)

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Increase Limit", callback_data="increase_warn")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ]
    )

    await message.reply_text(
        f"<b>Your default warn limit is: {limit}</b>",
        reply_markup=buttons
    )


# ---------------- BUTTON HANDLER ---------------- #

@Client.on_callback_query(filters.regex("increase_warn"))
async def increase_warn(client, callback):

    chat_id = callback.message.chat.id

    limit = await get_warn_limit(chat_id)

    if limit >= 5:

        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Close", callback_data="close")]]
        )

        return await callback.message.edit_text(
            "<b>Your default warn limit set to: 5\nthis is the maximum warn limit</b>",
            reply_markup=buttons
        )

    limit += 1

    await set_warn_limit(chat_id, limit)

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Increase Limit", callback_data="increase_warn")],
            [InlineKeyboardButton("Close", callback_data="close")]
        ]
    )

    await callback.message.edit_text(
        f"<b>Your default warn limit set to: {limit}</b>",
        reply_markup=buttons
    )


@Client.on_callback_query(filters.regex("close"))
async def close_button(client, callback):

    await callback.message.delete()
