from telegram import Update
from telegram.ext import ContextTypes

async def adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    # Only work in groups
    if chat.type == "private":
        await update.message.reply_text("This command only works in groups.")
        return

    admins = await context.bot.get_chat_administrators(chat.id)

    owner = None
    admin_list = []

    for admin in admins:

        user = admin.user
        mention = f"[{user.first_name}](tg://user?id={user.id})"

        if admin.status == "creator":
            owner = f"1. {mention} - Owner"
        else:
            admin_list.append(mention)

    text = ""

    if owner:
        text += owner + "\n"

    count = 2
    for adm in admin_list:
        text += f"{count}. {adm} - Admin\n"
        count += 1

    await update.message.reply_text(text, parse_mode="Markdown")
