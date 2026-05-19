# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                     config.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ── Telegram Bot Credentials ──────────────────────
# Get from https://my.telegram.org
API_ID = 0                          # apna API ID daalo
API_HASH = ""                       # apna API Hash daalo

# Get from @BotFather
BOT_TOKEN = ""                      # Bot token daalo

# ── Assistant (Userbot) ───────────────────────────
# String session generate karne ke liye:
# python -c "from pyrogram import Client; Client('assistant', API_ID, API_HASH).run()"
STRING_SESSION = ""                 # Assistant ka string session daalo

# ── Bot Info ──────────────────────────────────────
BOT_USERNAME = "Makima_Xprobot"
BOT_ID = 8771933924
OWNER_ID = 0                        # Apna Telegram user ID daalo

# ── Links (Change these) ──────────────────────────
SUPPORT_CHANNEL = "https://t.me/your_support_channel"   # Support channel link
CREATOR_USERNAME = "https://t.me/your_username"          # Creator profile link
ADD_BOT_LINK = f"https://t.me/{BOT_USERNAME}?startgroup=true&admin=can_manage_voice_chats+invite_users"

# ── Start Media ───────────────────────────────────
# Photo ya Video ka file_id ya URL daalo
# File ID use karne ke liye: pehle bot ko photo bhejo, then /id command se ID lo
START_PHOTO = ""                    # Start command ke liye photo/video
GROUP_ADD_PHOTO = ""                # Bot group mein add hone pe photo

# ── YouTube API Keys (10-15 keys daalo) ──────────
YOUTUBE_API_KEYS = [
    "",   # Key 1
    "",   # Key 2
    "",   # Key 3
    "",   # Key 4
    "",   # Key 5
    "",   # Key 6
    "",   # Key 7
    "",   # Key 8
    "",   # Key 9
    "",   # Key 10
    # Aur keys add karo...
]

# ── Database ──────────────────────────────────────
DATABASE_NAME = "makima_music.db"

# ── Audio Settings ────────────────────────────────
AUDIO_QUALITY = "bestaudio"         # yt-dlp quality
MAX_DURATION = 600                  # Max song duration in seconds (10 min)
DOWNLOAD_DIR = "./downloads"        # Temporary download folder

# ── Logging ───────────────────────────────────────
LOG_GROUP_ID = 0                    # Optional: errors yahan jayenge (group ID)
