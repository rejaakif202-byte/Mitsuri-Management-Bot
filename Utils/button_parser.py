import re
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def parse_buttons(text):

    pattern = r"\[(.*?)\]\((.*?)\)"

    buttons = []
    cleaned_text = text

    matches = re.findall(pattern, text)

    if not matches:
        return text, None

    keyboard = []

    for name, url in matches:

        if url.startswith("buttonurl:"):
            link = url.replace("buttonurl:", "")

            keyboard.append(
                [InlineKeyboardButton(name, url=link)]
            )

        cleaned_text = cleaned_text.replace(
            f"[{name}]({url})", ""
        )

    return cleaned_text.strip(), InlineKeyboardMarkup(keyboard)
