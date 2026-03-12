from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat
    user = update.effective_user
    message = update.message

    # Only groups
    if chat.type == "private":
        return

    # Must reply to message
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to report it.")
        return

    reported_user = message.reply_to_message.from_user

    admins = await context.bot.get_chat_administrators(chat.id)

    admin_mentions = []

    for admin in admins:
        if not admin.user.is_bot:
            admin_mentions.append(f"[{admin.user.first_name}](tg://user?id={admin.user.id})")

    admin_text = " ".join(admin_mentions)

    reporter = f"[{user.first_name}](tg://user?id={user.id})"
    reported = f"[{reported_user.first_name}](tg://user?id={reported_user.id})"

    text = f"""
🚨 **Report Alert**

Reporter: {reporter}
Reported User: {reported}

Admins: {admin_text}
"""

    await message.reply_text(text, parse_mode="Markdown")
