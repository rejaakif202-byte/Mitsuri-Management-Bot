# ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ — Termux Setup Guide

## Step 1 — Termux Setup

```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg git -y
pip install -r requirements.txt
```

## Step 2 — config.py Fill Karo

`config.py` kholo aur ye sab fill karo:

| Field | Kahan se milega |
|-------|----------------|
| `API_ID` | https://my.telegram.org |
| `API_HASH` | https://my.telegram.org |
| `BOT_TOKEN` | @BotFather |
| `STRING_SESSION` | Neeche dekho |
| `YOUTUBE_API_KEYS` | Google Cloud Console |
| `START_PHOTO` | Photo ka file_id ya URL |
| `SUPPORT_CHANNEL` | Apna channel link |
| `CREATOR_USERNAME` | Apna profile link |
| `OWNER_ID` | Apna Telegram ID (@userinfobot se lo) |

## Step 3 — String Session Generate Karo

```bash
python3 -c "
from pyrogram import Client
import asyncio

async def get_session():
    async with Client('assistant', api_id=YOUR_API_ID, api_hash='YOUR_API_HASH') as app:
        print(await app.export_session_string())

asyncio.run(get_session())
"
```

Ye assistant account ka session generate karega. Assistant alag Telegram account hona chahiye.

## Step 4 — Bot Start Karo

```bash
python3 bot.py
```

## Step 5 — Bot Ko Group Mein Add Karo

Bot ko admin banao in permissions ke saath:
- ✅ Manage Video Chats
- ✅ Invite Users

## Commands

| Command | Use |
|---------|-----|
| `/play <song>` | Song play karo voice chat mein |
| `/pause` | Pause karo |
| `/resume` | Resume karo |
| `/skip` | Next song |
| `/stop` | Stop karo |
| `/queue` | Queue dekho |

## Background Mein Chalao (Termux)

```bash
# tmux install karo
pkg install tmux -y

# New session shuru karo
tmux new -s musicbot

# Bot start karo
python3 bot.py

# Detach karo (Ctrl+B phir D)
# Wapas aane ke liye:
tmux attach -t musicbot
```
