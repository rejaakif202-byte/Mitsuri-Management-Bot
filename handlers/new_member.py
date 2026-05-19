# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                 handlers/new_member.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatMemberUpdated,
)
from database.db import save_group
from utils.fonts import sc, DOTS
import config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BOT GROUP MEIN ADD HONE PE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.new_chat_members & filters.group)
async def bot_added_to_group(client: Client, message: Message):
    # Check: kya bot khud add hua hai?
    for member in message.new_chat_members:
        if member.id == config.BOT_ID:
            # Group save karo DB mein
            await save_group(
                message.chat.id,
                message.chat.title or "Group"
            )

            caption = (
                f"**{DOTS}**\n"
                f"**{sc('makima xpro music bot')}** 🎵\n"
                f"**{DOTS}**\n\n"
                f"**{sc('thanks for adding me!')}** 🙏\n\n"
                f"**{sc('i am ready to stream high quality')}**\n"
                f"**{sc('music in this group voice chat!')}**\n\n"
                f"**{sc('━ start me in dm to know more')}**\n"
                f"**{sc('━ use /play to play a song')}**\n\n"
                f"**{DOTS}**"
            )

            # 2 buttons:
            # 1. Start in DM — bot ko DM mein open karta hai
            # 2. Support Channel
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    f"🚀  {sc('click here to know me')}",
                    url=f"https://t.me/{config.BOT_USERNAME}?start=hello"
                )],
                [InlineKeyboardButton(
                    f"📢  {sc('support channel')}  ↗",
                    url=config.SUPPORT_CHANNEL
                )],
            ])

            await message.reply_photo(
                photo=config.GROUP_ADD_PHOTO,
                caption=caption,
                reply_markup=buttons,
            )
            break  # Sirf ek baar bhejo


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BOT GROUP SE REMOVE HONE PE (optional logging)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.left_chat_member & filters.group)
async def bot_removed_from_group(client: Client, message: Message):
    if message.left_chat_member.id == config.BOT_ID:
        # Optional: LOG_GROUP mein log karo
        if config.LOG_GROUP_ID:
            try:
                await client.send_message(
                    config.LOG_GROUP_ID,
                    f"**{sc('bot removed from group')}**\n"
                    f"► {sc('group')}: {message.chat.title}\n"
                    f"► {sc('id')}: `{message.chat.id}`"
                )
            except Exception:
                pass
