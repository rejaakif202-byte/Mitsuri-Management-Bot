from pyrogram import Client, filters
from pyrogram.types import Message

from database.gban_db import (
    add_gban,
    remove_gban,
    get_gbans
)

from database.sudo_db import is_sudo


# GBAN
@Client.on_message(filters.command("gban"))
async def gban(client: Client, message: Message):

    if not await is_sudo(message.from_user.id):
        return await message.reply_text(
            "Only sudo users can use this command."
        )

    if len(message.command) < 2:
        return await message.reply_text(
            "Give username or user id."
        )

    try:
        user = await client.get_users(message.command[1])
    except:
        return await message.reply_text("User not found.")

    await add_gban(user.id)

    banned_groups = 0

    async for dialog in client.get_dialogs():

        if dialog.chat.type in ["group", "supergroup"]:

            try:
                await client.ban_chat_member(
                    dialog.chat.id,
                    user.id
                )

                banned_groups += 1

            except:
                pass

    await message.reply_text(
        f"<b>{user.mention}</b> globally banned.\n\n"
        f"Banned in <b>{banned_groups}</b> groups."
    )


# UNGBAN
@Client.on_message(filters.command("ungban"))
async def ungban(client: Client, message: Message):

    if not await is_sudo(message.from_user.id):
        return await message.reply_text(
            "Only sudo users can use this command."
        )

    if len(message.command) < 2:
        return

    try:
        user = await client.get_users(message.command[1])
    except:
        return await message.reply_text("User not found.")

    await remove_gban(user.id)

    unbanned_groups = 0

    async for dialog in client.get_dialogs():

        if dialog.chat.type in ["group", "supergroup"]:

            try:
                await client.unban_chat_member(
                    dialog.chat.id,
                    user.id
                )

                unbanned_groups += 1

            except:
                pass

    await message.reply_text(
        f"<b>{user.mention}</b> globally unbanned.\n\n"
        f"Unbanned in <b>{unbanned_groups}</b> groups."
    )


# GBAN LIST
@Client.on_message(filters.command("gbanlist"))
async def gbanlist(client: Client, message: Message):

    users = await get_gbans()

    if not users:
        return await message.reply_text(
            "No users in gban list."
        )

    text = "<b>Global Ban List</b>\n\n"

    for i, user_id in enumerate(users, 1):

        try:

            user = await client.get_users(user_id)

            text += (
                f"{i}. <b>{user.mention}</b> - "
                f"<code>{user_id}</code>\n"
            )

        except:

            text += (
                f"{i}. Unknown - "
                f"<code>{user_id}</code>\n"
            )

    await message.reply_text(text)
