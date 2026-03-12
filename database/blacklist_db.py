blacklist_db = {}


async def add_blacklist(chat_id, word):

    if chat_id not in blacklist_db:
        blacklist_db[chat_id] = []

    if word not in blacklist_db[chat_id]:
        blacklist_db[chat_id].append(word)


async def remove_blacklist(chat_id, word):

    if chat_id in blacklist_db:

        if word in blacklist_db[chat_id]:
            blacklist_db[chat_id].remove(word)


async def get_blacklist(chat_id):

    if chat_id not in blacklist_db:
        return []

    return blacklist_db[chat_id]
