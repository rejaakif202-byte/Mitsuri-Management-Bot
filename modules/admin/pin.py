from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("pin") & filters.group)
async def pin_message(client: Client, message: Message):

    user = message.from_user

    member = await client.get_chat_member(message.chat.id, user.id)

    if not member.privileges or not member.privileges.can_pin_messages:
        return await message.reply_text(
            "<b>You are not allowed to use this command</b>"
        )

    if not message.reply_to_message:
        return await message.reply_text(
            "<b>Reply to a message to pin it</b>"
        )

    bot_member = await client.get_chat_member(message.chat.id, "me")

    if not bot_member.privileges.can_pin_messages:
        return await message.reply_text(
            "<b>I need pin message permission to do this</b>"
        )

    await message.reply_to_message.pin()

    await message.reply_text(
        "<b>Message has been pinned</b>"
    )
