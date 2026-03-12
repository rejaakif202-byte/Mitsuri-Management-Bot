PROMOTED_ADMINS = {}


async def add_promoted(chat_id, user_id):

    if chat_id not in PROMOTED_ADMINS:
        PROMOTED_ADMINS[chat_id] = []

    if user_id not in PROMOTED_ADMINS[chat_id]:
        PROMOTED_ADMINS[chat_id].append(user_id)


async def remove_promoted(chat_id, user_id):

    if chat_id in PROMOTED_ADMINS:
        if user_id in PROMOTED_ADMINS[chat_id]:
            PROMOTED_ADMINS[chat_id].remove(user_id)


async def is_promoted(chat_id, user_id):

    if chat_id in PROMOTED_ADMINS:
        return user_id in PROMOTED_ADMINS[chat_id]

    return False


async def get_promoted(chat_id):

    return PROMOTED_ADMINS.get(chat_id, [])
