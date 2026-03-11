from pyrogram.types import Message


async def is_admin(client, message: Message):

    user = message.from_user

    if not user:
        return False

    member = await client.get_chat_member(message.chat.id, user.id)

    if member.status in ["administrator", "creator"]:
        return True

    await message.reply_text(
        "<b>You must be an admin to use this command.</b>"
    )

    return False
