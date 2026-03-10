locks = {}
approved_users = {}


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


async def add_lock(chat_id, lock):

    if chat_id not in locks:
        locks[chat_id] = []

    if lock not in locks[chat_id]:
        locks[chat_id].append(lock)


async def remove_lock(chat_id, lock):

    if chat_id in locks:

        if lock in locks[chat_id]:
            locks[chat_id].remove(lock)


async def get_locks(chat_id):

    return locks.get(chat_id, [])
