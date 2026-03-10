from pyrogram import Client, filters
from pyrogram.types import Message
from utils.permissions import is_admin


@Client.on_message(filters.command("purge") & filters.group)
async def purge_messages(client: Client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text("<b>You are not allowed to use this command</b>")

    if not message.reply_to_message:
        return await message.reply_text("<b>Reply to a message to start purge</b>")

    # Check bot delete permission
    bot = await client.get_chat_member(message.chat.id, "me")

    if not bot.can_delete_messages:
        return await message.reply_text(
            "<b>I need delete message permission to do this</b>"
        )

    start_id = message.reply_to_message.id
    end_id = message.id

    deleted = 0

    for msg_id in range(start_id, end_id + 1):

        try:
            await client.delete_messages(message.chat.id, msg_id)
            deleted += 1
        except:
            pass

    text = f"<b>Purge completed, {deleted} messages deleted in {message.chat.title}</b>"

    msg = await message.reply_text(text)

    try:
        await message.delete()
    except:
        pass
