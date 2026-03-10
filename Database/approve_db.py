approve_db = {}


async def approve_user(chat_id, user_id):

    if chat_id not in approve_db:
        approve_db[chat_id] = []

    if user_id not in approve_db[chat_id]:
        approve_db[chat_id].append(user_id)


async def unapprove_user(chat_id, user_id):

    if chat_id in approve_db:

        if user_id in approve_db[chat_id]:
            approve_db[chat_id].remove(user_id)


async def is_approved(chat_id, user_id):

    if chat_id in approve_db:

        if user_id in approve_db[chat_id]:
            return True

    return False


async def approve_all(chat_id):

    approve_db[chat_id] = "all"


async def unapprove_all(chat_id):

    approve_db[chat_id] = []


async def get_approved_list(chat_id):

    if chat_id not in approve_db:
        return []

    if approve_db[chat_id] == "all":
        return []

    return approve_db[chat_id]
