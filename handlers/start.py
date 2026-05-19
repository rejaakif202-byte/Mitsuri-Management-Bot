# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                   handlers/start.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from database.db import save_user, save_group
from utils.fonts import sc, DOTS
import config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /start — PRIVATE CHAT (DM)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.command("start") & filters.private)
async def start_private(client: Client, message: Message):
    user = message.from_user

    # User ko DB mein save karo (broadcast ke liye)
    await save_user(user.id, user.first_name or "Unknown")

    name = user.first_name or "User"

    caption = (
        f"**{DOTS}**\n"
        f"**{sc('Hey')} {name}! 👋**\n"
        f"**{DOTS}**\n\n"
        f"**{sc('welcome to makima xpro music bot!')}** 🎵\n\n"
        f"**{sc('i am a powerful music bot that streams')}**\n"
        f"**{sc('high quality audio in your group')}**\n"
        f"**{sc('voice chats!')}**\n\n"
        f"**{sc('━ powered by')}** @{config.BOT_USERNAME}\n"
        f"**{DOTS}**"
    )

    # 4 buttons — screenshot jaisi layout
    buttons = InlineKeyboardMarkup([
        # Row 1 — Full width (Add Bot)
        [InlineKeyboardButton(
            f"➕  {sc('click here to add me')}",
            url=config.ADD_BOT_LINK
        )],
        # Row 2 — Commands (blue feel) | Creator (green feel)
        [
            InlineKeyboardButton(
                f"📋  {sc('commands')}",
                callback_data="show_commands"
            ),
            InlineKeyboardButton(
                f"👑  {sc('creator')}",
                url=config.CREATOR_USERNAME
            ),
        ],
        # Row 3 — Full width (Support Channel)
        [InlineKeyboardButton(
            f"📢  {sc('support channel')}  ↗",
            url=config.SUPPORT_CHANNEL
        )],
    ])

    # Photo bhejo
    await message.reply_photo(
        photo=config.START_PHOTO,
        caption=caption,
        reply_markup=buttons,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /start — GROUP CHAT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.command("start") & filters.group)
async def start_group(client: Client, message: Message):
    # Group ko DB mein save karo
    await save_group(message.chat.id, message.chat.title or "Group")

    caption = (
        f"**{DOTS}**\n"
        f"**{sc('makima xpro music bot')}** 🎵\n"
        f"**{DOTS}**\n\n"
        f"**{sc('hello!')} 👋 {sc('i am online and ready')}**\n"
        f"**{sc('to play music in this group!')}**\n\n"
        f"**{sc('use')}** `/play {sc('song name')}` **{sc('to get started!')}**\n\n"
        f"**{DOTS}**"
    )

    # Group mein sirf 2 buttons
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f"➕  {sc('add me to your group')}",
            url=config.ADD_BOT_LINK
        )],
        [InlineKeyboardButton(
            f"📋  {sc('commands')}",
            callback_data="show_commands"
        )],
    ])

    await message.reply_photo(
        photo=config.START_PHOTO,
        caption=caption,
        reply_markup=buttons,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  COMMANDS CALLBACK — /commands button press hone pe
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_callback_query(filters.regex("show_commands"))
async def show_commands_cb(client: Client, callback: CallbackQuery):
    text = (
        f"**{DOTS}**\n"
        f"**{sc('makima xpro')} — {sc('commands')}** 📋\n"
        f"**{DOTS}**\n\n"
        f"**{sc('music commands')}** 🎵\n"
        f"► `/play` — {sc('play a song in voice chat')}\n"
        f"► `/pause` — {sc('pause current song')}\n"
        f"► `/resume` — {sc('resume paused song')}\n"
        f"► `/skip` — {sc('skip to next song')}\n"
        f"► `/stop` — {sc('stop and leave voice chat')}\n"
        f"► `/queue` — {sc('show song queue')}\n\n"
        f"**{sc('other commands')}** ⚙️\n"
        f"► `/start` — {sc('start the bot')}\n"
        f"► `/help` — {sc('get help')}\n\n"
        f"**{DOTS}**"
    )

    back_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔙 {sc('back')}", callback_data="back_start")]
    ])

    await callback.message.edit_caption(
        caption=text,
        reply_markup=back_btn,
    )
    await callback.answer()


# ── Back button ───────────────────────────────────
@Client.on_callback_query(filters.regex("back_start"))
async def back_start_cb(client: Client, callback: CallbackQuery):
    user = callback.from_user
    name = user.first_name or "User"

    caption = (
        f"**{DOTS}**\n"
        f"**{sc('Hey')} {name}! 👋**\n"
        f"**{DOTS}**\n\n"
        f"**{sc('welcome to makima xpro music bot!')}** 🎵\n\n"
        f"**{sc('i am a powerful music bot that streams')}**\n"
        f"**{sc('high quality audio in your group')}**\n"
        f"**{sc('voice chats!')}**\n\n"
        f"**{sc('━ powered by')}** @{config.BOT_USERNAME}\n"
        f"**{DOTS}**"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f"➕  {sc('click here to add me')}",
            url=config.ADD_BOT_LINK
        )],
        [
            InlineKeyboardButton(f"📋  {sc('commands')}", callback_data="show_commands"),
            InlineKeyboardButton(f"👑  {sc('creator')}", url=config.CREATOR_USERNAME),
        ],
        [InlineKeyboardButton(
            f"📢  {sc('support channel')}  ↗",
            url=config.SUPPORT_CHANNEL
        )],
    ])

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=buttons,
    )
    await callback.answer()
