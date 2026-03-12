filters_db = {}


async def add_filter(chat_id, word, text=None, buttons=None, media=None):

    if chat_id not in filters_db:
        filters_db[chat_id] = {}

    filters_db[chat_id][word] = {
        "text": text,
        "buttons": buttons,
        "media": media
    }


async def remove_filter(chat_id, word):

    if chat_id in filters_db:
        if word in filters_db[chat_id]:
            del filters_db[chat_id][word]


async def remove_all_filters(chat_id):

    if chat_id in filters_db:
        filters_db[chat_id] = {}


async def get_filters(chat_id):

    return filters_db.get(chat_id, {})


async def get_filter(chat_id, word):

    if chat_id in filters_db:
        return filters_db[chat_id].get(word)

    return None
