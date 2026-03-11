from pyrogram import Client, filters
from pyrogram.types import Message

from utils.permissions import is_admin
from database.approve_db import (
    approve_user,
    unapprove_user,
    approve_all,
    unapprove_all,
    get_approved_list
)


# ---------------- APPROVE ---------------- #

@Client.on_message(filters.command("approve") & filters.group)
async def approve(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    if not message.reply_to_message:
        return await message.reply_text("<b>Reply to a user to approve</b>")

    user = message.reply_to_message.from_user

    if not user:
        return

    await approve_user(message.chat.id, user.id)

    await message.reply_text(
        f"<b>{user.mention} is now approved.</b>"
    )


# ---------------- UNAPPROVE ---------------- #

@Client.on_message(filters.command("unapprove") & filters.group)
async def unapprove(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    if not message.reply_to_message:
        return await message.reply_text("<b>Reply to a user to unapprove</b>")

    user = message.reply_to_message.from_user

    if not user:
        return

    await unapprove_user(message.chat.id, user.id)

    await message.reply_text(
        f"<b>{user.mention} is now unapproved.</b>"
    )


# ---------------- APPROVE ALL ---------------- #

@Client.on_message(filters.command("approveall") & filters.group)
async def approveall(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    await approve_all(message.chat.id)

    await message.reply_text(
        "<b>All members are now approved.</b>"
    )


# ---------------- UNAPPROVE ALL ---------------- #

@Client.on_message(filters.command("unapproveall") & filters.group)
async def unapproveall(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    await unapprove_all(message.chat.id)

    await message.reply_text(
        "<b>All members are now unapproved.</b>"
    )


# ---------------- APPROVE LIST ---------------- #

@Client.on_message(filters.command("approvelist") & filters.group)
async def approvelist(client: Client, message: Message):

    users = await get_approved_list(message.chat.id)

    if not users:
        return await message.reply_text("<b>No approved users.</b>")

    text = "<b>Approved Users:</b>\n\n"

    count = 1

    for user_id in users:

        try:
            user = await client.get_users(user_id)

            text += f"{count}. {user.mention} - <code>{user_id}</code>\n"

            count += 1

        except Exception:
            pass

    await message.reply_text(text)
