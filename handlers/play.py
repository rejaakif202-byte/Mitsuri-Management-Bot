# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                   handlers/play.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from pyrogram import Client, filters
from pyrogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ChatPrivileges,
)
from pyrogram.errors import ChatAdminRequired
from pytgcalls.exceptions import NoActiveGroupCall

from utils.youtube import search_youtube
from utils.fonts import sc, DOTS
import utils.vc_manager as vcm
import config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HELPER — Bot admin check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def _is_bot_admin(client: Client, chat_id: int) -> bool:
    """Bot admin hai aur uske paas VC + invite permission hai?"""
    try:
        bot_id = (await client.get_me()).id
        member = await client.get_chat_member(chat_id, bot_id)
        privs  = member.privileges
        if not privs:
            return False
        return privs.can_manage_video_chats and privs.can_invite_users
    except Exception:
        return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HELPER — Control buttons
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _music_buttons(chat_id: int) -> InlineKeyboardMarkup:
    """▷ ⏸ ⏭ ⏹ buttons"""
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("▷",   callback_data=f"resume_{chat_id}"),
        InlineKeyboardButton("⏸",   callback_data=f"pause_{chat_id}"),
        InlineKeyboardButton("⏭⏭|", callback_data=f"skip_{chat_id}"),
        InlineKeyboardButton("⏹",   callback_data=f"stop_{chat_id}"),
    ]])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /play COMMAND
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.command("play") & filters.group)
async def play_command(client: Client, message: Message):
    chat_id = message.chat.id
    user    = message.from_user

    # ── 1. Song name check ────────────────────────
    query = " ".join(message.command[1:]).strip()
    if not query:
        await message.reply(
            f"**{sc('usage')} :** `/play {sc('song name')}`",
            quote=True
        )
        return

    # ── 2. Bot admin check ────────────────────────
    if not await _is_bot_admin(client, chat_id):
        await message.reply(
            f"**❌ {sc('make me admin first!')}**\n\n"
            f"**{sc('required permissions')} :**\n"
            f"**► {sc('manage video chats')}**\n"
            f"**► {sc('invite users')}**",
            quote=True
        )
        return

    # ── 3. Searching message ──────────────────────
    searching_msg = await message.reply(
        f"**🔍 {sc('searching for')}** `{query}`**...**",
        quote=True
    )

    # ── 4. YouTube search ─────────────────────────
    song = await search_youtube(query)
    if not song:
        await searching_msg.edit(
            f"**❌ {sc('no results found for')}** `{query}`\n"
            f"**{sc('try a different song name.')}**"
        )
        return

    # Requester info add karo
    song["requested_by"] = f"**{user.first_name or user.username or 'User'}**"
    song["requester_id"] = user.id

    # ── 5. Assistant ko group mein ensure karo ────
    await searching_msg.edit(f"**⚙️ {sc('connecting')}...**")

    assistant_ok = await vcm.ensure_assistant_in_group(client, chat_id)
    if not assistant_ok:
        await searching_msg.edit(
            f"**❌ {sc('failed to add assistant to group!')}**\n"
            f"**{sc('make sure bot has invite users permission.')}**"
        )
        return

    # ── 6. Kya kuch chal raha hai? ────────────────
    if vcm.is_playing(chat_id):
        # Queue mein add karo
        position = vcm.add_to_queue(chat_id, song)

        await searching_msg.edit(
            f"**{DOTS}**\n"
            f"**↻ {sc('added to queue at')} #{position}**\n\n"
            f"**► {sc('title')} :** `{song['title']}`\n"
            f"**► {sc('duration')} :** `{song['duration']} {sc('minutes')}`\n"
            f"**► {sc('requested by')} :** {song['requested_by']}\n\n"
            f"**{DOTS}**",
            reply_markup=_music_buttons(chat_id)
        )
        return

    # ── 7. VC active check + play ─────────────────
    await searching_msg.edit(f"**⏳ {sc('loading')}...**")

    success = await vcm.play_song(chat_id, song)

    if not success:
        # VC active nahi hai — screenshot 1 jaisa message
        await searching_msg.edit(
            f"**🔇 {sc('no active videochat found.')}**\n\n"
            f"**{sc('please start videochat in your')}**\n"
            f"**{sc('group/channel and try again.')}**"
        )
        return

    # ── 8. Now Playing message ────────────────────
    await searching_msg.edit(
        f"**{DOTS}**\n"
        f"**↻ {sc('started streaming')} |**\n\n"
        f"**► {sc('title')} :** `{song['title']}`\n"
        f"**► {sc('duration')} :** `{song['duration']} {sc('minutes')}`\n"
        f"**► {sc('requested by')} :** {song['requested_by']}\n\n"
        f"**{DOTS}**",
        reply_markup=_music_buttons(chat_id)
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CONTROL CALLBACKS — ▷ ⏸ ⏭ ⏹ buttons
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_callback_query(filters.regex(r"^(resume|pause|skip|stop)_(-?\d+)$"))
async def music_controls(client: Client, callback: CallbackQuery):
    action  = callback.matches[0].group(1)
    chat_id = int(callback.matches[0].group(2))
    user    = callback.from_user

    await callback.answer()  # Loading circle band karo

    if action == "pause":
        ok = await vcm.pause(chat_id)
        status = f"⏸ {sc('paused by')} **{user.first_name}**" if ok else f"❌ {sc('already paused')}"
        await callback.message.edit_caption(
            caption=(
                f"**{DOTS}**\n"
                f"**{status}**\n\n"
                f"**► {sc('title')} :** `{vcm.get_current(chat_id)['title'] if vcm.get_current(chat_id) else 'N/A'}`\n\n"
                f"**{DOTS}**"
            ),
            reply_markup=_music_buttons(chat_id)
        )

    elif action == "resume":
        ok = await vcm.resume(chat_id)
        status = f"▷ {sc('resumed by')} **{user.first_name}**" if ok else f"❌ {sc('nothing to resume')}"
        await callback.message.edit_caption(
            caption=(
                f"**{DOTS}**\n"
                f"**{status}**\n\n"
                f"**► {sc('title')} :** `{vcm.get_current(chat_id)['title'] if vcm.get_current(chat_id) else 'N/A'}`\n\n"
                f"**{DOTS}**"
            ),
            reply_markup=_music_buttons(chat_id)
        )

    elif action == "skip":
        next_song = await vcm.skip(chat_id)
        if next_song:
            await callback.message.edit_caption(
                caption=(
                    f"**{DOTS}**\n"
                    f"**⏭ {sc('skipped by')} {user.first_name}**\n\n"
                    f"**↻ {sc('now playing')}**\n"
                    f"**► {sc('title')} :** `{next_song['title']}`\n"
                    f"**► {sc('duration')} :** `{next_song['duration']} {sc('minutes')}`\n"
                    f"**► {sc('requested by')} :** {next_song['requested_by']}\n\n"
                    f"**{DOTS}**"
                ),
                reply_markup=_music_buttons(chat_id)
            )
        else:
            await callback.message.edit_caption(
                caption=(
                    f"**{DOTS}**\n"
                    f"**⏹ {sc('queue is empty')}**\n"
                    f"**{sc('left voice chat.')}**\n\n"
                    f"**{DOTS}**"
                )
            )

    elif action == "stop":
        await vcm.stop(chat_id)
        await callback.message.edit_caption(
            caption=(
                f"**{DOTS}**\n"
                f"**⏹ {sc('stopped by')} {user.first_name}**\n"
                f"**{sc('left voice chat.')}**\n\n"
                f"**{DOTS}**"
            )
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /queue COMMAND
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.command("queue") & filters.group)
async def show_queue(client: Client, message: Message):
    chat_id  = message.chat.id
    queue    = vcm.get_queue(chat_id)
    current  = vcm.get_current(chat_id)

    if not current and not queue:
        await message.reply(
            f"**📭 {sc('queue is empty!')}**\n"
            f"**{sc('use')}** `/play {sc('song name')}` **{sc('to add songs.')}**",
            quote=True
        )
        return

    text = f"**{DOTS}**\n**🎵 {sc('music queue')}**\n**{DOTS}**\n\n"

    if current:
        text += f"**▶ {sc('now playing')} :**\n`{current['title']}`\n\n"

    if queue:
        text += f"**📋 {sc('up next')} :**\n"
        for i, song in enumerate(queue, 1):
            text += f"**{i}.** `{song['title']}`\n"

    text += f"\n**{DOTS}**"
    await message.reply(text, quote=True)
