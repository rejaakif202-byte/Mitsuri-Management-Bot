from pyrogram.types import Message


# ---------------- USER ADMIN CHECK ---------------- #

async def is_admin(client, message: Message):

    if not message.from_user:
        return False

    try:
        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        if member.status in ["administrator", "creator"]:
            return True

    except:
        pass

    await message.reply_text(
        "<b>You must be an admin to use this command.</b>"
    )

    return False


# ---------------- OWNER CHECK ---------------- #

async def is_owner(client, message: Message):

    try:
        member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )

        if member.status == "creator":
            return True

    except:
        pass

    await message.reply_text(
        "<b>Only the group owner can use this command.</b>"
    )

    return False


# ---------------- BOT ADMIN CHECK ---------------- #

async def bot_is_admin(client, message: Message):

    try:
        bot = await client.get_chat_member(
            message.chat.id,
            "me"
        )

        if bot.status in ["administrator", "creator"]:
            return True

    except:
        pass

    await message.reply_text(
        "<b>I need admin permissions to perform this action.</b>"
    )

    return False
