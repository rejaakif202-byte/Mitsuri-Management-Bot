from pyrogram import Client, filters
from pyrogram.types import Message

from database.users_db import add_block, remove_block, is_blocked
from utils.permissions import is_sudo


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


# ---------------- BLOCK ---------------- #

@Client.on_message(filters.command("block"))
async def block_user(client: Client, message: Message):

    if not await is_sudo(client, message.from_user.id):
        return

    user_id = await get_target_user(client, message)

    if not user_id:
        return await message.reply_text(
            "<b>Reply to a user or give username/user_id</b>"
        )

    already = await is_blocked(user_id)

    if already:
        return await message.reply_text(
            "<b>This user is already blocked</b>"
        )

    await add_block(user_id)

    user = await client.get_users(user_id)

    await message.reply_text(
        f"<b>{user.mention} has been blocked from using this bot</b>"
    )


# ---------------- UNBLOCK ---------------- #

@Client.on_message(filters.command("unblock"))
async def unblock_user(client: Client, message: Message):

    if not await is_sudo(client, message.from_user.id):
        return

    user_id = await get_target_user(client, message)

    if not user_id:
        return await message.reply_text(
            "<b>Reply to a user or give username/user_id</b>"
        )

    blocked = await is_blocked(user_id)

    if not blocked:
        return await message.reply_text(
            "<b>This user is not blocked</b>"
        )

    await remove_block(user_id)

    user = await client.get_users(user_id)

    await message.reply_text(
        f"<b>{user.mention} is now unblocked</b>"
    )
