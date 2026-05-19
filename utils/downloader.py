# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                  utils/downloader.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import os
import asyncio
import yt_dlp
import config


# Download folder ensure karo
os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)


def _get_ydl_opts(output_path: str) -> dict:
    """yt-dlp options"""
    return {
        "format"           : "bestaudio/best",
        "outtmpl"          : output_path,
        "quiet"            : True,
        "no_warnings"      : True,
        "noplaylist"       : True,
        "postprocessors"   : [{
            "key"            : "FFmpegExtractAudio",
            "preferredcodec" : "mp3",
            "preferredquality": "192",
        }],
        # Termux mein ffmpeg path
        "ffmpeg_location"  : "/data/data/com.termux/files/usr/bin",
    }


async def download_audio(video_id: str) -> str | None:
    """
    YouTube video ka audio download karo.
    Returns: mp3 file path, ya None agar error.
    
    Async wrapper — yt-dlp sync call ko thread pool mein run karta hai
    taaki bot block na ho.
    """
    output_template = os.path.join(config.DOWNLOAD_DIR, f"{video_id}.%(ext)s")
    final_path      = os.path.join(config.DOWNLOAD_DIR, f"{video_id}.mp3")

    # Pehle check karo — already downloaded hai?
    if os.path.exists(final_path):
        return final_path

    url = f"https://www.youtube.com/watch?v={video_id}"

    def _download():
        try:
            with yt_dlp.YoutubeDL(_get_ydl_opts(output_template)) as ydl:
                ydl.download([url])
            return final_path if os.path.exists(final_path) else None
        except Exception as e:
            print(f"[Downloader] Error: {e}")
            return None

    # Thread pool mein run karo (blocking call)
    loop   = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _download)
    return result


async def cleanup_file(file_path: str):
    """Played song ki file delete karo disk save karne ke liye"""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"[Downloader] Cleanup error: {e}")
