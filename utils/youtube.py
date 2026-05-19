# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                   utils/youtube.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from database.db import get_next_api_key, cache_song, get_cached_song


def _parse_duration(iso_duration: str) -> str:
    """
    ISO 8601 duration → human readable
    PT3M49S → 3:49
    PT1H2M5S → 1:02:05
    """
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, iso_duration)
    if not match:
        return "0:00"

    hours   = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def _format_views(view_count: str) -> str:
    """
    View count format
    87000000 → 87M views
    """
    try:
        n = int(view_count)
        if n >= 1_000_000_000:
            return f"{n/1_000_000_000:.1f}B views"
        elif n >= 1_000_000:
            return f"{n/1_000_000:.1f}M views"
        elif n >= 1_000:
            return f"{n/1_000:.1f}K views"
        return f"{n} views"
    except Exception:
        return "N/A"


async def search_youtube(query: str) -> dict | None:
    """
    YouTube mein song search karo.
    - Pehle cache check karta hai (24hr)
    - Cache miss hone pe API call karta hai key rotation ke saath
    
    Returns dict:
        {
            video_id, title, artist (channel),
            duration, views, thumbnail,
            url
        }
    Returns None agar kuch nahi mila ya sab keys quota khatam.
    """

    # ── 1. Cache check ────────────────────────────
    cached = await get_cached_song(query)
    if cached:
        cached["url"] = f"https://www.youtube.com/watch?v={cached['video_id']}"
        return cached

    # ── 2. API key lo (rotation) ──────────────────
    api_key = await get_next_api_key()
    if not api_key:
        return None  # Sab keys ka quota khatam

    try:
        # ── 3. YouTube search ─────────────────────
        youtube = build("youtube", "v3", developerKey=api_key)

        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=1,
            type="video",
            videoCategoryId="10",   # Music category
        ).execute()

        items = search_response.get("items", [])
        if not items:
            return None

        item    = items[0]
        vid_id  = item["id"]["videoId"]
        snippet = item["snippet"]
        title   = snippet.get("title", "Unknown Title")
        channel = snippet.get("channelTitle", "Unknown Artist")
        thumb   = (
            snippet.get("thumbnails", {})
                   .get("high", {})
                   .get("url", "")
        )

        # ── 4. Video details (duration + views) ───
        details_response = youtube.videos().list(
            part="contentDetails,statistics",
            id=vid_id
        ).execute()

        detail_items = details_response.get("items", [])
        duration_str = "0:00"
        views_str    = "N/A"

        if detail_items:
            content  = detail_items[0].get("contentDetails", {})
            stats    = detail_items[0].get("statistics", {})
            duration_str = _parse_duration(content.get("duration", "PT0S"))
            views_str    = _format_views(stats.get("viewCount", "0"))

        result = {
            "video_id" : vid_id,
            "title"    : title,
            "artist"   : channel,
            "duration" : duration_str,
            "views"    : views_str,
            "thumbnail": thumb,
            "url"      : f"https://www.youtube.com/watch?v={vid_id}",
        }

        # ── 5. Cache mein save karo ───────────────
        await cache_song(
            query, vid_id, title, channel,
            duration_str, views_str, thumb
        )

        return result

    except HttpError as e:
        # Quota exceed hone pe next key try karo (recursive nahi, next call pe)
        if e.resp.status in (403, 429):
            print(f"[YouTube] Key quota exceeded, will rotate next call.")
        return None

    except Exception as e:
        print(f"[YouTube] Search error: {e}")
        return None
