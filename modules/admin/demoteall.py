from pyrogram import Client, filters
from pyrogram.types import Message

from database.promote_db import get_promoted, remove_promoted


@Client.on_message(filters.command("demoteall") & filters.group)
async def demote_all(client: Client, message: Message):

    member = await client.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status != "creator":
        return await message.reply_text(
            "Only group owner can use this command."
        )

    promoted_users = await get_promoted(message.chat.id)

    count = 0

    for user_id in promoted_users:

        try:

            await client.promote_chat_member(

                message.chat.id,
                user_id,

                can_change_info=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
                can_promote_members=False

            )

            await remove_promoted(message.chat.id, user_id)

            count += 1

        except:
            pass

    await message.reply_text(
        f"Demoted {count} admins."
    )
