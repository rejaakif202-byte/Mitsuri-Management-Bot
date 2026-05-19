# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                  utils/vc_manager.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from pytgcalls.exceptions import NoActiveGroupCall, AlreadyJoinedError
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, ChatAdminRequired, UserNotParticipant

from utils.downloader import download_audio, cleanup_file
import config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GLOBAL STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# PyTgCalls instance (bot.py mein initialize hoga)
call_py: PyTgCalls = None

# Per-group queue: { chat_id: [ {song_info}, ... ] }
queues: dict[int, list] = {}

# Per-group current song: { chat_id: {song_info} }
current_playing: dict[int, dict] = {}


def setup_pytgcalls(assistant: Client) -> PyTgCalls:
    """
    PyTgCalls instance banao aur global variable mein store karo.
    bot.py mein call karo.
    """
    global call_py
    call_py = PyTgCalls(assistant)
    return call_py


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ASSISTANT MANAGEMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def ensure_assistant_in_group(bot: Client, chat_id: int) -> bool:
    """
    Assistant group mein hai ya nahi check karo.
    Nahi hai to bot use invite karega.
    Returns True if assistant is in group, False if failed.
    """
    assistant_id = (await call_py._app.get_me()).id

    try:
        # Check karo assistant member hai ya nahi
        member = await bot.get_chat_member(chat_id, assistant_id)
        # Agar kicked ya banned hai to False return karo
        if member.status.value in ("banned", "left"):
            raise UserNotParticipant()
        return True

    except UserNotParticipant:
        # Assistant group mein nahi — bot use invite karega
        try:
            await bot.add_chat_members(chat_id, assistant_id)
            return True
        except UserAlreadyParticipant:
            return True
        except ChatAdminRequired:
            return False
        except Exception as e:
            print(f"[VCManager] Invite error: {e}")
            return False

    except Exception as e:
        print(f"[VCManager] Check member error: {e}")
        return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  QUEUE MANAGEMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_queue(chat_id: int) -> list:
    return queues.get(chat_id, [])


def add_to_queue(chat_id: int, song_info: dict) -> int:
    """Queue mein song add karo. Returns queue position (1-indexed)."""
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append(song_info)
    return len(queues[chat_id])


def get_current(chat_id: int) -> dict | None:
    return current_playing.get(chat_id)


def is_playing(chat_id: int) -> bool:
    return chat_id in current_playing and current_playing[chat_id] is not None


def clear_queue(chat_id: int):
    queues.pop(chat_id, None)
    current_playing.pop(chat_id, None)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PLAYBACK CONTROLS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def play_song(chat_id: int, song_info: dict) -> bool:
    """
    Song ko voice chat mein play karo.
    Returns True on success, False on failure.
    """
    global current_playing

    video_id = song_info["video_id"]

    # Audio download karo
    file_path = await download_audio(video_id)
    if not file_path:
        return False

    song_info["file_path"] = file_path

    try:
        # Already joined hai? Change stream karo
        await call_py.change_stream(
            chat_id,
            MediaStream(file_path)
        )
    except Exception:
        # Pehli baar join karo
        try:
            await call_py.join_group_call(
                chat_id,
                MediaStream(file_path)
            )
        except NoActiveGroupCall:
            return False   # VC active nahi
        except AlreadyJoinedError:
            await call_py.change_stream(chat_id, MediaStream(file_path))
        except Exception as e:
            print(f"[VCManager] Play error: {e}")
            return False

    current_playing[chat_id] = song_info
    return True


async def play_next(chat_id: int) -> dict | None:
    """
    Queue se next song play karo.
    Returns next song info, ya None agar queue empty.
    """
    queue = queues.get(chat_id, [])

    # Previous song ka file cleanup
    prev = current_playing.get(chat_id)
    if prev and prev.get("file_path"):
        await cleanup_file(prev["file_path"])

    if not queue:
        current_playing.pop(chat_id, None)
        try:
            await call_py.leave_group_call(chat_id)
        except Exception:
            pass
        return None

    next_song = queue.pop(0)
    success = await play_song(chat_id, next_song)

    if success:
        return next_song
    return None


async def pause(chat_id: int) -> bool:
    try:
        await call_py.pause_stream(chat_id)
        return True
    except Exception:
        return False


async def resume(chat_id: int) -> bool:
    try:
        await call_py.resume_stream(chat_id)
        return True
    except Exception:
        return False


async def skip(chat_id: int) -> dict | None:
    """Current song skip karo, next play karo."""
    return await play_next(chat_id)


async def stop(chat_id: int) -> bool:
    """Stop karo aur VC se leave karo."""
    try:
        # Current file cleanup
        prev = current_playing.get(chat_id)
        if prev and prev.get("file_path"):
            await cleanup_file(prev["file_path"])

        clear_queue(chat_id)
        await call_py.leave_group_call(chat_id)
        return True
    except Exception as e:
        print(f"[VCManager] Stop error: {e}")
        return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  AUTO PLAY NEXT — song khatam hone pe
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def register_stream_end_handler(bot: Client):
    """
    PyTgCalls ka stream_end event register karo.
    Jab song khatam ho, next song automatically play ho.
    bot.py mein call karo after setup_pytgcalls.
    """

    @call_py.on_stream_end()
    async def on_stream_end(_, update):
        chat_id = update.chat_id
        next_song = await play_next(chat_id)

        if next_song:
            # Optional: Now Playing update bhejo group mein
            try:
                from utils.fonts import sc, DOTS
                text = (
                    f"**{DOTS}**\n"
                    f"**🎵 {sc('now playing')}**\n"
                    f"**{DOTS}**\n\n"
                    f"**► {sc('title')} :** `{next_song['title']}`\n"
                    f"**► {sc('duration')} :** `{next_song['duration']} {sc('minutes')}`\n"
                    f"**► {sc('requested by')} :** {next_song['requested_by']}\n\n"
                    f"**{DOTS}**"
                )
                await bot.send_message(chat_id, text)
            except Exception:
                pass
