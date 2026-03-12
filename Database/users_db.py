users = set()
chats = set()


async def add_user(user_id):
    users.add(user_id)


async def add_chat(chat_id):
    chats.add(chat_id)


async def get_users():
    return list(users)


async def get_total_users():
    return len(users)


async def get_total_chats():
    return len(chats)
