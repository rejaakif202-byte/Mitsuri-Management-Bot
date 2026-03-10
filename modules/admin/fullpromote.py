from pyrogram import Client, filters
from pyrogram.types import Message

OWNER_ID = 7846306818  # <-- apna id yaha daalna


@Client.on_message(filters.command("fullpromote") & filters.group)
async def fullpromote(client: Client, message: Message):

    user = None

    # reply method
    if message.reply_to_message:
        user = message.reply_to_message.from_user

    # username / id
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply_text("User not found.")

    # OWNER SELF PROMOTE FEATURE
    if message.from_user.id == OWNER_ID and message.reply_to_message:
        user = message.reply_to_message.from_user

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
            can_pin_messages=True,
            can_manage_chat=True,
            can_manage_video_chats=True,
            can_promote_members=True

        )

    except:
        return await message.reply_text(
            "I need full admin rights to promote users."
        )

    await message.reply_text(
        f"<b>{user.mention}</b> fully promoted to admin."
    )
