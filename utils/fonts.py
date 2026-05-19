# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              ᴍᴀᴋɪᴍᴀ xᴘʀᴏ ᴍᴜꜱɪᴄ ʙᴏᴛ
#                    utils/fonts.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Small Caps Unicode Map — ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ
SMALL_CAPS_MAP = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ',
    'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
    'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ',
    'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ',
    'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ',
    'z': 'ᴢ',
}


def sc(text: str) -> str:
    """
    Kisi bhi text ko small caps mein convert karo.
    Special characters, numbers, emojis — sab as-is rehte hain.
    
    Usage:
        sc("Hello World")  →  "ʜᴇʟʟᴏ ᴡᴏʀʟᴅ"
        sc("Play Song 🎵")  →  "ᴘʟᴀʏ ꜱᴏɴɢ 🎵"
    """
    result = []
    for char in text:
        lower = char.lower()
        if lower in SMALL_CAPS_MAP:
            result.append(SMALL_CAPS_MAP[lower])
        else:
            result.append(char)
    return ''.join(result)


def bold_sc(text: str) -> str:
    """Small caps + Telegram bold markdown"""
    return f"**{sc(text)}**"


# ── Pre-built common strings ──────────────────────────────
# Inhe directly use karo templates mein

DOTS  = "━━━━━━━━━━━━━━━━━━━━━━"
ARROW = "►"
MUSIC = "🎵"
WAVE  = "〰"
