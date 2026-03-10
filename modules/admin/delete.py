from pyrogram import Client, filters
from pyrogram.types import Message

from utils.permissions import is_admin


@Client.on_message(filters.command("del") & filters.group)
async def delete_message(client: Client, message: Message):

    if not await is_admin(client, message):
        return

    if not message.reply_to_message:
        return

    try:

        await message.reply_to_message.delete()

        await message.delete()

    except:
        pass
