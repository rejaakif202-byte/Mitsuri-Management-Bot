from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_db import add_user
from utils.uptime import get_uptime

START_IMAGE = "https://files.catbox.moe/45n49c.mp4"

SUPPORT = "https://t.me/ANIMEXVERSE"
CREATOR = "tg://openmessage?user_id=7846306818"


@Client.on_message(filters.command("start"))
async def start(client, message):

    user = message.from_user
    chat = message.chat

    bot_username = (await client.get_me()).username

    mention = user.mention
    bot_mention = f"@{bot_username}"

    # -------- DM START --------

    if chat.type == "private":

        await add_user(user.id)

        text = f"""Hey There, {mention}! This is {bot_mention}.

This is a powerful group management bot.

Type /help to know my commands.
"""

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "➕ Add me in your group",
                    url=f"https://t.me/{bot_username}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton("📢 Support Channel", url=SUPPORT),
                InlineKeyboardButton("👑 Creator", url=CREATOR)
            ]
        ])

        await message.reply_photo(
            photo=START_IMAGE,
            caption=text,
            reply_markup=buttons
        )

    # -------- GROUP START --------

    else:

        uptime = get_uptime()

        text = f"""{bot_mention} is alive again.

I didn't sleep since - {uptime}
"""

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "➕ Add Me",
                    url=f"https://t.me/{bot_username}?startgroup=true"
                ),
                InlineKeyboardButton("📢 Support Channel", url=SUPPORT)
            ]
        ])

        await message.reply_photo(
            photo=START_IMAGE,
            caption=text,
            reply_markup=buttons
        )
