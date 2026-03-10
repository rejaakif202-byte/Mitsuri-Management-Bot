blacklist = {}
approved_users = {}


async def add_blacklist(chat_id, word):

    if chat_id not in blacklist:
        blacklist[chat_id] = []

    if word not in blacklist[chat_id]:
        blacklist[chat_id].append(word)


async def remove_blacklist(chat_id, word):

    if chat_id in blacklist:

        if word in blacklist[chat_id]:
            blacklist[chat_id].remove(word)


async def get_blacklist(chat_id):

    return blacklist.get(chat_id, [])


async def approve_user(chat_id, user_id):

    if chat_id not in approved_users:
        approved_users[chat_id] = []

    if user_id not in approved_users[chat_id]:
        approved_users[chat_id].append(user_id)


async def unapprove_user(chat_id, user_id):

    if chat_id in approved_users:

        if user_id in approved_users[chat_id]:
            approved_users[chat_id].remove(user_id)


async def is_approved(chat_id, user_id):

    if chat_id in approved_users:

        if user_id in approved_users[chat_id]:
            return True

    return False
