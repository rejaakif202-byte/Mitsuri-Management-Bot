# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                       bot.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode

# Handlers import
import handlers.start
import handlers.new_member
import handlers.play

# Utils import
from utils.vc_manager import setup_pytgcalls, register_stream_end_handler
from database.db import init_db
import config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BOT CLIENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
bot = Client(
    name       = "MakimaXproBot",
    api_id     = config.API_ID,
    api_hash   = config.API_HASH,
    bot_token  = config.BOT_TOKEN,
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ASSISTANT (USERBOT) CLIENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
assistant = Client(
    name         = "MakimaAssistant",
    api_id       = config.API_ID,
    api_hash     = config.API_HASH,
    session_string = config.STRING_SESSION,
)


async def main():
    # ── 1. Database initialize karo ───────────────
    await init_db()

    # ── 2. PyTgCalls setup karo ───────────────────
    call_py = setup_pytgcalls(assistant)
    register_stream_end_handler(bot)

    # ── 3. Dono clients start karo ────────────────
    await bot.start()
    await assistant.start()
    await call_py.start()

    bot_info = await bot.get_me()
    asst_info = await assistant.get_me()

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
  ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
━━━━━━━━━━━━━━━━━━━━━━━━━━
  Bot      : @{bot_info.username}
  Assistant: @{asst_info.username}
  Status   : ONLINE ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

    # ── 4. Bot chalta rahe ────────────────────────
    await asyncio.get_event_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
