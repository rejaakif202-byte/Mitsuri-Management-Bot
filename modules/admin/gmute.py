from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions

from database.gmute_db import (
    add_gmute,
    remove_gmute,
    get_gmutes
)

from database.sudo_db import is_sudo


# GMUTE
@Client.on_message(filters.command("gmute"))
async def gmute(client: Client, message: Message):

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

    await add_gmute(user.id)

    muted_groups = 0

    async for dialog in client.get_dialogs():

        if dialog.chat.type in ["group", "supergroup"]:

            try:

                await client.restrict_chat_member(
                    dialog.chat.id,
                    user.id,
                    ChatPermissions()
                )

                muted_groups += 1

            except:
                pass

    await message.reply_text(

        f"<b>{user.mention}</b> globally muted.\n\n"
        f"Muted in <b>{muted_groups}</b> groups."

    )


# UNGMUTE
@Client.on_message(filters.command("ungmute"))
async def ungmute(client: Client, message: Message):

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

    await remove_gmute(user.id)

    unmuted_groups = 0

    async for dialog in client.get_dialogs():

        if dialog.chat.type in ["group", "supergroup"]:

            try:

                await client.restrict_chat_member(
                    dialog.chat.id,
                    user.id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_add_web_page_previews=True
                    )
                )

                unmuted_groups += 1

            except:
                pass

    await message.reply_text(

        f"<b>{user.mention}</b> globally unmuted.\n\n"
        f"Unmuted in <b>{unmuted_groups}</b> groups."

    )


# GMUTE LIST
@Client.on_message(filters.command("gmutelist"))
async def gmutelist(client: Client, message: Message):

    users = await get_gmutes()

    if not users:
        return await message.reply_text(
            "No users in gmute list."
        )

    text = "<b>Global Mute List</b>\n\n"

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
