# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                     database/db.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import aiosqlite
import time
import config

DB = config.DATABASE_NAME


async def init_db():
    """Sab tables create karo agar exist nahi karte"""
    async with aiosqlite.connect(DB) as db:

        # ── Users Table (broadcast ke liye) ──────
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                name        TEXT,
                joined_at   INTEGER DEFAULT (strftime('%s','now'))
            )
        """)

        # ── Groups Table ─────────────────────────
        await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                chat_id     INTEGER PRIMARY KEY,
                title       TEXT,
                joined_at   INTEGER DEFAULT (strftime('%s','now'))
            )
        """)

        # ── YouTube API Keys Table ────────────────
        await db.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key_index   INTEGER PRIMARY KEY,
                api_key     TEXT UNIQUE,
                used_today  INTEGER DEFAULT 0,
                reset_at    INTEGER DEFAULT 0
            )
        """)

        # ── Song Cache Table ──────────────────────
        await db.execute("""
            CREATE TABLE IF NOT EXISTS song_cache (
                query       TEXT PRIMARY KEY,
                video_id    TEXT,
                title       TEXT,
                artist      TEXT,
                duration    TEXT,
                views       TEXT,
                thumbnail   TEXT,
                cached_at   INTEGER DEFAULT (strftime('%s','now'))
            )
        """)

        await db.commit()

    # YouTube API keys ko seed karo config se
    await seed_api_keys()
    print("✅ Database initialized!")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  USER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def save_user(user_id: int, name: str):
    """User ko database mein save karo"""
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        await db.commit()


async def get_all_users():
    """Broadcast ke liye sab users ka list"""
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_users_count():
    """Total users count"""
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        row = await cursor.fetchone()
        return row[0]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GROUP FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def save_group(chat_id: int, title: str):
    """Group ko database mein save karo"""
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO groups (chat_id, title) VALUES (?, ?)",
            (chat_id, title)
        )
        await db.commit()


async def get_all_groups():
    """Broadcast ke liye sab groups ka list"""
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT chat_id FROM groups")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_groups_count():
    """Total groups count"""
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM groups")
        row = await cursor.fetchone()
        return row[0]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  YOUTUBE API KEY ROTATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def seed_api_keys():
    """config.py se API keys ko DB mein daalo"""
    async with aiosqlite.connect(DB) as db:
        for idx, key in enumerate(config.YOUTUBE_API_KEYS):
            if key:  # empty keys skip karo
                await db.execute(
                    "INSERT OR IGNORE INTO api_keys (key_index, api_key) VALUES (?, ?)",
                    (idx, key)
                )
        await db.commit()


async def get_next_api_key() -> str | None:
    """
    Available API key lo.
    Daily quota 10,000/key — agar used_today >= 9000 to next key use karo.
    Midnight pe sab keys reset ho jaati hain.
    """
    now = int(time.time())
    today_start = now - (now % 86400)  # aaj ka midnight (UTC)

    async with aiosqlite.connect(DB) as db:
        # Pehle keys ko reset karo agar new day hai
        await db.execute(
            "UPDATE api_keys SET used_today = 0 WHERE reset_at < ?",
            (today_start,)
        )
        await db.commit()

        # Aisa key dhoondo jiska usage 9000 se kam ho
        cursor = await db.execute(
            "SELECT api_key FROM api_keys WHERE used_today < 9000 ORDER BY used_today ASC LIMIT 1"
        )
        row = await cursor.fetchone()

        if row:
            key = row[0]
            # Usage increment karo
            await db.execute(
                "UPDATE api_keys SET used_today = used_today + 1, reset_at = ? WHERE api_key = ?",
                (today_start, key)
            )
            await db.commit()
            return key

    return None  # Sab keys ka quota khatam


async def get_keys_status():
    """Debug ke liye: sab keys ka status"""
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute(
            "SELECT key_index, used_today FROM api_keys ORDER BY key_index"
        )
        rows = await cursor.fetchall()
        return rows


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SONG CACHE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def cache_song(query: str, video_id: str, title: str, artist: str,
                     duration: str, views: str, thumbnail: str):
    """Search result cache karo taaki baar baar API call na ho"""
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            INSERT OR REPLACE INTO song_cache 
            (query, video_id, title, artist, duration, views, thumbnail)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (query.lower().strip(), video_id, title, artist, duration, views, thumbnail))
        await db.commit()


async def get_cached_song(query: str) -> dict | None:
    """Cache mein song dhoondo"""
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute(
            "SELECT video_id, title, artist, duration, views, thumbnail, cached_at FROM song_cache WHERE query = ?",
            (query.lower().strip(),)
        )
        row = await cursor.fetchone()
        if row:
            # Cache 24 ghante ke baad expire karo
            cached_at = row[6]
            if int(time.time()) - cached_at < 86400:
                return {
                    "video_id": row[0],
                    "title": row[1],
                    "artist": row[2],
                    "duration": row[3],
                    "views": row[4],
                    "thumbnail": row[5],
                }
    return None
