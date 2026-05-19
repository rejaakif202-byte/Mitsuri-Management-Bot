# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                  handlers/controls.py
#
#  Commands  : /pause  /resume  /skip  /end
#  Who can   : Group Admins + Bot Owner only
#  Who can't : Regular members (they can /play only)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

import utils.vc_manager as vcm
from utils.fonts import sc, DOTS
import config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PERMISSION CHECKER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def _is_admin_or_owner(client: Client, chat_id: int, user_id: int) -> bool:
    """
    Check karo:
    - Bot owner hai (config.OWNER_ID)?
    - Group admin/creator hai?
    Returns True ya False.
    """
    # Bot owner always allowed
    if user_id == config.OWNER_ID:
        return True

    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
    except Exception:
        return False


async def _bot_is_admin(client: Client, chat_id: int) -> bool:
    """Bot khud admin hai ya nahi"""
    try:
        bot_id = (await client.get_me()).id
        member = await client.get_chat_member(chat_id, bot_id)
        return member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
    except Exception:
        return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  RESPONSE TEMPLATES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _err(text: str) -> str:
    return f"**{DOTS}**\n**❌ {text}**\n**{DOTS}**"

def _ok(text: str) -> str:
    return f"**{DOTS}**\n**{text}**\n**{DOTS}**"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /pause
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  Possible cases:
#  [1] User admin/owner nahi                → permission denied
#  [2] Bot khud admin nahi                  → bot ko admin banao
#  [3] Koi bhi song play nahi ho raha       → nothing playing
#  [4] Song already paused hai              → already paused
#  [5] VC exist nahi / bot VC mein nahi     → no active session
#  [6] Sab theek → pause success
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.command("pause") & filters.group)
async def pause_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    user    = message.from_user

    # [1] Permission check
    if not await _is_admin_or_owner(client, chat_id, user.id):
        await message.reply(
            _err(
                f"{sc('only admins can use this command!')}\n\n"
                f"**{sc('tip :')} {sc('members can only use')}** `/play`"
            ),
            quote=True
        )
        return

    # [2] Bot admin check
    if not await _bot_is_admin(client, chat_id):
        await message.reply(
            _err(f"{sc('make me admin first!')}"),
            quote=True
        )
        return

    # [3] Koi bhi play nahi
    if not vcm.is_playing(chat_id):
        await message.reply(
            _err(
                f"{sc('no song is playing right now!')}\n\n"
                f"**{sc('use')}** `/play {sc('song name')}` **{sc('to start.')}"
                f"**"
            ),
            quote=True
        )
        return

    # [5] VC session check
    if vcm.get_current(chat_id) is None:
        await message.reply(
            _err(f"{sc('no active music session found!')}"),
            quote=True
        )
        return

    # [6] Pause karo
    success = await vcm.pause(chat_id)

    if not success:
        # [4] Already paused ya error
        await message.reply(
            _err(f"{sc('already paused or unable to pause!')}"),
            quote=True
        )
        return

    current = vcm.get_current(chat_id)
    await message.reply(
        _ok(
            f"⏸ {sc('paused by')} **{user.first_name}**\n\n"
            f"**► {sc('song')} :** `{current['title'] if current else 'N/A'}`\n"
            f"**{sc('use')}** `/resume` **{sc('to continue.')}"
            f"**"
        ),
        quote=True
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /resume
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  Possible cases:
#  [1] User admin/owner nahi                → permission denied
#  [2] Bot khud admin nahi                  → bot ko admin banao
#  [3] Koi bhi song play nahi / session nahi→ kuch nahi chal raha
#  [4] Song already chal raha (paused nahi) → already playing
#  [5] VC mein bot nahi                     → no active session
#  [6] Sab theek → resume success
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.command("resume") & filters.group)
async def resume_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    user    = message.from_user

    # [1] Permission check
    if not await _is_admin_or_owner(client, chat_id, user.id):
        await message.reply(
            _err(
                f"{sc('only admins can use this command!')}\n\n"
                f"**{sc('tip :')} {sc('members can only use')}** `/play`"
            ),
            quote=True
        )
        return

    # [2] Bot admin check
    if not await _bot_is_admin(client, chat_id):
        await message.reply(
            _err(f"{sc('make me admin first!')}"),
            quote=True
        )
        return

    # [3] Session hi nahi
    if vcm.get_current(chat_id) is None:
        await message.reply(
            _err(
                f"{sc('nothing to resume!')}\n\n"
                f"**{sc('no active music session found.')}\n"
                f"{sc('use')}** `/play {sc('song name')}` **{sc('to start.')}"
                f"**"
            ),
            quote=True
        )
        return

    # [6] Resume karo
    success = await vcm.resume(chat_id)

    if not success:
        # [4] Already playing ya error
        await message.reply(
            _err(
                f"{sc('already playing or unable to resume!')}\n\n"
                f"**{sc('if song is stuck, try')}** `/skip`"
            ),
            quote=True
        )
        return

    current = vcm.get_current(chat_id)
    await message.reply(
        _ok(
            f"▷ {sc('resumed by')} **{user.first_name}**\n\n"
            f"**► {sc('song')} :** `{current['title'] if current else 'N/A'}`"
        ),
        quote=True
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /skip
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  Possible cases:
#  [1] User admin/owner nahi                → permission denied
#  [2] Bot khud admin nahi                  → bot ko admin banao
#  [3] Koi bhi song play nahi               → nothing to skip
#  [4] Queue empty hai (next song nahi)     → stops, leaves VC
#  [5] VC nahi / session nahi              → no active session
#  [6] Next song play hua                   → now playing next
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.command("skip") & filters.group)
async def skip_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    user    = message.from_user

    # [1] Permission check
    if not await _is_admin_or_owner(client, chat_id, user.id):
        await message.reply(
            _err(
                f"{sc('only admins can use this command!')}\n\n"
                f"**{sc('tip :')} {sc('members can only use')}** `/play`"
            ),
            quote=True
        )
        return

    # [2] Bot admin check
    if not await _bot_is_admin(client, chat_id):
        await message.reply(
            _err(f"{sc('make me admin first!')}"),
            quote=True
        )
        return

    # [3] Koi play hi nahi
    if not vcm.is_playing(chat_id):
        await message.reply(
            _err(
                f"{sc('no song is playing right now!')}\n\n"
                f"**{sc('use')}** `/play {sc('song name')}` **{sc('to start.')}"
                f"**"
            ),
            quote=True
        )
        return

    skipped = vcm.get_current(chat_id)
    queue   = vcm.get_queue(chat_id)

    # [4] Queue empty — skip karne ke baad kuch nahi
    if not queue:
        await vcm.stop(chat_id)
        await message.reply(
            _ok(
                f"⏭ {sc('skipped by')} **{user.first_name}**\n\n"
                f"**► {sc('skipped')} :** `{skipped['title'] if skipped else 'N/A'}`\n\n"
                f"**📭 {sc('queue is empty!')}**\n"
                f"**{sc('left voice chat.')}\n"
                f"{sc('use')}** `/play {sc('song name')}` **{sc('to start again.')}"
                f"**"
            ),
            quote=True
        )
        return

    # [6] Next song play karo
    next_song = await vcm.skip(chat_id)

    if next_song:
        await message.reply(
            _ok(
                f"⏭ {sc('skipped by')} **{user.first_name}**\n\n"
                f"**↻ {sc('now playing')}**\n\n"
                f"**► {sc('title')} :** `{next_song['title']}`\n"
                f"**► {sc('duration')} :** `{next_song['duration']} {sc('minutes')}`\n"
                f"**► {sc('requested by')} :** {next_song['requested_by']}"
            ),
            quote=True
        )
    else:
        # [5] Skip hua but next play nahi hua (VC issue)
        await message.reply(
            _err(
                f"{sc('skipped but could not play next song!')}\n\n"
                f"**{sc('voice chat may have ended.')}\n"
                f"{sc('start vc and use')}** `/play` **{sc('again.')}"
                f"**"
            ),
            quote=True
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /end
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  Possible cases:
#  [1] User admin/owner nahi                → permission denied
#  [2] Bot khud admin nahi                  → bot ko admin banao
#  [3] Koi session hi nahi                  → nothing to end
#  [4] Song nahi par queue hai              → clears queue, leaves
#  [5] Song chal raha + queue hai           → stop all, leave VC
#  [6] Sab theek → end success
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@Client.on_message(filters.command("end") & filters.group)
async def end_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    user    = message.from_user

    # [1] Permission check
    if not await _is_admin_or_owner(client, chat_id, user.id):
        await message.reply(
            _err(
                f"{sc('only admins can use this command!')}\n\n"
                f"**{sc('tip :')} {sc('members can only use')}** `/play`"
            ),
            quote=True
        )
        return

    # [2] Bot admin check
    if not await _bot_is_admin(client, chat_id):
        await message.reply(
            _err(f"{sc('make me admin first!')}"),
            quote=True
        )
        return

    # [3] Koi session hi nahi
    current = vcm.get_current(chat_id)
    queue   = vcm.get_queue(chat_id)

    if not current and not queue:
        await message.reply(
            _err(
                f"{sc('no active music session to end!')}\n\n"
                f"**{sc('bot is not playing anything right now.')}"
                f"**"
            ),
            quote=True
        )
        return

    # Queue count save karo (before clearing)
    queue_count = len(queue)
    current_title = current['title'] if current else None

    # [4] / [5] / [6] — Sab stop karo
    success = await vcm.stop(chat_id)

    if success:
        text = (
            f"**{DOTS}**\n"
            f"**⏹ {sc('music ended by')} {user.first_name}**\n\n"
        )

        if current_title:
            text += f"**► {sc('was playing')} :** `{current_title}`\n"

        if queue_count > 0:
            text += (
                f"**► {sc('cleared')} :** "
                f"`{queue_count} {sc('song(s) from queue')}`\n"
            )

        text += (
            f"\n**{sc('left voice chat.')}**\n"
            f"**{sc('use')}** `/play {sc('song name')}` "
            f"**{sc('to start again.')}**\n\n"
            f"**{DOTS}**"
        )
        await message.reply(text, quote=True)

    else:
        await message.reply(
            _err(
                f"{sc('failed to end session!')}\n\n"
                f"**{sc('try again or restart the bot.')}"
                f"**"
            ),
            quote=True
        )
