from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

START_IMAGE = "https://files.catbox.moe/45n49c.mp4"

SUPPORT = "https://t.me/ANIMEXVERSE"

ADDED_TEXT = """Wassup Groupmates

Thanks for adding {mention_of_bot_name} in {chatname}.
Make me admin to use all my features.

Type /help to see commands.
"""


async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat
    bot_username = context.bot.username

    text = ADDED_TEXT.replace("{mention_of_bot_name}", f"@{bot_username}")
    text = text.replace("{chatname}", chat.title)

    buttons = [
        [
            InlineKeyboardButton("📚 Commands", callback_data="commands"),
            InlineKeyboardButton("📢 Support Channel", url=SUPPORT)
        ]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await context.bot.send_photo(
        chat_id=chat.id,
        photo=START_IMAGE,
        caption=text,
        reply_markup=keyboard
    )
