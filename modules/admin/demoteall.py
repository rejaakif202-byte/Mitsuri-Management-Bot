from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("demoteall") & filters.group)
async def demote_all(client: Client, message: Message):

    admins = await client.get_chat_members(
        message.chat.id,
        filter="administrators"
    )

    count = 0

    async for admin in admins:

        user = admin.user

        if admin.status == "creator":
            continue

        promoted = Bot.getProperty(
            f"promoted_{message.chat.id}_{user.id}"
        )

        if not promoted:
            continue

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

            Bot.deleteProperty(
                f"promoted_{message.chat.id}_{user.id}"
            )

            count += 1

        except:
            pass

    await message.reply_text(
        f"Demoted {count} admins."
    )
