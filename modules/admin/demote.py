from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("demote") & filters.group)
async def demote_user(client: Client, message: Message):

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text(
            "Reply to a user or give username/user id."
        )

    # user detect
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply_text("User not found.")

    # check promoted by bot
    promoted = Bot.getProperty(f"promoted_{message.chat.id}_{user.id}")

    if not promoted:
        return await message.reply_text(
            "This user was not promoted by me."
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

        Bot.deleteProperty(f"promoted_{message.chat.id}_{user.id}")

    except:
        return await message.reply_text(
            "I need admin rights to demote users."
        )

    await message.reply_text(
        f"<b>{user.mention}</b> demoted to member."
    )
