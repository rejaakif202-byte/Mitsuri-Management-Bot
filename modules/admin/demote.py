from pyrogram import Client, filters
from pyrogram.types import Message

from database.promote_db import is_promoted, remove_promoted


@Client.on_message(filters.command("demote") & filters.group)
async def demote_user(client: Client, message: Message):

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text(
            "Reply to a user or give username/user id."
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply_text("User not found.")

    if not await is_promoted(message.chat.id, user.id):
        return await message.reply_text(
            "This admin was not promoted by me."
        )

    try:

        await client.promote_chat_member(

            message.chat.id,
            user.id,

            can_change_info=False,
            can_delete_messages=False,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_manage_chat=False,
            can_manage_video_chats=False,
            can_promote_members=False

        )

        await remove_promoted(message.chat.id, user.id)

    except:
        return await message.reply_text(
            "I need admin rights to demote users."
        )

    await message.reply_text(
        f"<b>{user.mention}</b> demoted to member."
    )
