import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from database.users import add_user
from utils.uptime import get_uptime

START_IMAGE = "https://files.catbox.moe/45n49c.mp4"

SUPPORT = "https://t.me/ANIMEXVERSE"
CREATOR = "tg://openmessage?user_id=7846306818"

DM_TEXT = """Hey There, {mention}!? This is {mention_of_bot_name}.

This is a powerful group Management bot for managing your group with all the security.

Type /help to know my all commands and how to use me.
"""

GROUP_TEXT = """{mention_of_bot_name} is alive again.

I didn't sleep since - {time_duration}
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    bot = context.bot
    user = update.effective_user
    chat = update.effective_chat

    bot_username = bot.username
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    bot_mention = f"@{bot_username}"

    # ---------------- DM START ----------------

    if chat.type == "private":

        add_user(user.id)

        text = DM_TEXT.replace("{mention}", mention)
        text = text.replace("{mention_of_bot_name}", bot_mention)

        buttons = [

            [
                InlineKeyboardButton(
                    "➕ Add me in your group",
                    url=f"https://t.me/{bot_username}?startgroup=true"
                )
            ],

            [
                InlineKeyboardButton("📢 Support Channel", url=SUPPORT),
                InlineKeyboardButton("👑 Creator", url=CREATOR)
            ],

            [
                InlineKeyboardButton("📚 Commands", callback_data="commands")
            ]
        ]

        keyboard = InlineKeyboardMarkup(buttons)

        await update.message.reply_photo(
            photo=START_IMAGE,
            caption=text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

    # ---------------- GROUP START ----------------

    else:

        uptime = get_uptime()

        text = GROUP_TEXT.replace("{mention_of_bot_name}", bot_mention)
        text = text.replace("{time_duration}", uptime)

        buttons = [
            [
                InlineKeyboardButton(
                    "➕ Add Me",
                    url=f"https://t.me/{bot_username}?startgroup=true"
                ),
                InlineKeyboardButton("📢 Support Channel", url=SUPPORT)
            ]
        ]

        keyboard = InlineKeyboardMarkup(buttons)

        await update.message.reply_photo(
            photo=START_IMAGE,
            caption=text,
            reply_markup=keyboard
        )
