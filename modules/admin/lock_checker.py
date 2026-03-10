from pyrogram import Client, filters
from database.locks_db import get_locks
from utils.permissions import is_admin_or_approved


@Client.on_message(filters.group)
async def check_locks(client, message):

    if await is_admin_or_approved(client, message):
        return

    locks = await get_locks(message.chat.id)

    text = message.text or ""

    if "text" in locks and text:
        await message.delete()

    if "url" in locks and ("http" in text or "t.me" in text):
        await message.delete()

    if "sticker" in locks and message.sticker:
        await message.delete()

    if "gif" in locks and message.animation:
        await message.delete()

    if "video" in locks and message.video:
        await message.delete()

    if "audio" in locks and message.audio:
        await message.delete()

    if "document" in locks and message.document:
        await message.delete()

    if "contact" in locks and message.contact:
        await message.delete()

    if "photo" in locks and message.photo:
        await message.delete()
