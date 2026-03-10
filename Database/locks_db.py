locks = {}


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
