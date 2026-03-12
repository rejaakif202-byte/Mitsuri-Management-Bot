import time

from pyrogram import Client, filters
from pyrogram.types import Message

from database.users_db import get_total_users, get_total_chats
from database.sudo_db import is_sudo

START_TIME = time.time()


# ---------------- UPTIME ---------------- #

def get_uptime():

    seconds = int(time.time() - START_TIME)

    days = seconds // 86400
    seconds %= 86400

    hours = seconds // 3600
    seconds %= 3600

    minutes = seconds // 60
    seconds %= 60

    return f"{days}d {hours}h {minutes}m {seconds}s"


# ---------------- STATS ---------------- #

@Client.on_message(filters.command("stats"))
async def stats(client: Client, message: Message):

    if not await is_sudo(message.from_user.id):
        return

    users = await get_total_users()
    chats = await get_total_chats()

    uptime = get_uptime()

    ping_start = time.time()
    msg = await message.reply_text("Calculating stats...")
    ping = round((time.time() - ping_start) * 1000)

    text = f"""
<b>🤖 StrawHat Manager Bot Stats</b>

🏘 <b>Total Groups :</b> <code>{chats}</code>
👥 <b>Total Users :</b> <code>{users}</code>

⚡ <b>Ping :</b> <code>{ping} ms</code>
⏳ <b>Uptime :</b> <code>{uptime}</code>
"""

    await msg.delete()

    await message.reply_photo(
        photo="https://graph.org/file/0c1d9a4c93e6e7c4b6e6c.jpg",
        caption=text
    )
