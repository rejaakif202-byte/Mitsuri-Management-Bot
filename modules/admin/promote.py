from pyrogram import Client, filters
from pyrogram.types import Message

from utils.permissions import is_admin


@Client.on_message(filters.command("promote") & filters.group)
async def promote_user(client: Client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text(
            "Only admins can use this command."
        )

    user = None

    # reply method
    if message.reply_to_message:
        user = message.reply_to_message.from_user

    # username / id
    elif len(message.command) > 1:

        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply_text(
                "User not found."
            )

    if not user:
        return await message.reply_text(
            "Reply to a user or give username/user id."
        )

    try:

        member = await client.get_chat_member(
            message.chat.id,
            user.id
        )

    except:
        return await message.reply_text(
            "User is not in this group."
        )

    try:

        await client.promote_chat_member(

            message.chat.id,
            user.id,

            can_change_info=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_invite_users=True,

            can_promote_members=False,
            can_manage_chat=False,
            can_manage_video_chats=False,
            can_pin_messages=False,
            is_anonymous=False

        )

    Bot.setProperty(f"promoted_{message.chat.id}_{user.id}", True)

    except:
        return await message.reply_text(
            "I need full admin rights to promote users."
        )

    await message.reply_text(
        f"<b>{user.mention}</b> promoted successfully."
    )
