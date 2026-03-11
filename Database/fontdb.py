FONT_DATA = {}


def save_text(user_id, text):
    FONT_DATA[user_id] = text


def get_text(user_id):
    return FONT_DATA.get(user_id)


def delete_text(user_id):
    if user_id in FONT_DATA:
        del FONT_DATA[user_id]
