from pyrogram import Client, filters
from pyrogram.types import Message

from database.sudo_db import (
    add_sudo,
    remove_sudo,
    get_sudos,
    OWNER_ID
)


# ADD SUDO
@Client.on_message(filters.command("addsudo"))
async def addsudo(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text(
            "Only owner can add sudo users."
        )

    user = None

    if message.reply_to_message:
        user = message.reply_to_message.from_user

    elif len(message.command) > 1:

        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply_text("User not found.")

    if not user:
        return await message.reply_text(
            "Reply or give username/userid"
        )

    await add_sudo(user.id)

    await message.reply_text(
        f"<b>Added to sudo users:</b>\n{user.mention}"
    )


# REMOVE SUDO
@Client.on_message(filters.command("remsudo"))
async def remsudo(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text(
            "Only owner can remove sudo."
        )

    user = None

    if message.reply_to_message:
        user = message.reply_to_message.from_user

    elif len(message.command) > 1:

        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply_text("User not found.")

    if not user:
        return await message.reply_text(
            "Reply or give username/userid"
        )

    await remove_sudo(user.id)

    await message.reply_text(
        f"<b>Removed from sudo users:</b>\n{user.mention}"
    )


# SUDO LIST
@Client.on_message(filters.command("sudolist"))
async def sudolist(client: Client, message: Message):

    sudos = await get_sudos()

    text = "<b>Owner</b>\n"

    owner = await client.get_users(OWNER_ID)

    text += f"1. {owner.mention}\n\n"

    text += "<b>Admin</b>\n"

    if not sudos:

        text += "No sudo users"

    else:

        for i, user_id in enumerate(sudos, 1):

            try:
                user = await client.get_users(user_id)

                text += f"{i}. {user.mention}\n"

            except:
                pass

    await message.reply_text(text)
