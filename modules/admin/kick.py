from pyrogram import Client, filters
from pyrogram.types import Message

from utils.permissions import is_admin


@Client.on_message(filters.command("kick") & filters.group)
async def kick_user(client: Client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text(
            "Only admins can use this command."
        )

    user = None

    # reply kick
    if message.reply_to_message:
        user = message.reply_to_message.from_user

    # username / id kick
    elif len(message.command) > 1:

        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply_text("User not found.")

    if not user:
        return await message.reply_text(
            "Reply or give username/user id."
        )

    try:

        await client.ban_chat_member(
            message.chat.id,
            user.id
        )

        await client.unban_chat_member(
            message.chat.id,
            user.id
        )

    except:
        return await message.reply_text(
            "I need ban rights to kick users."
        )

    await message.reply_text(
        f"<b>{user.mention}</b> has been kicked."
    )
