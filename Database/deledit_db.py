edit_db = {}
approved_users = {}


async def toggle_edit_delete(chat_id, state):

    if chat_id not in edit_db:
        edit_db[chat_id] = {"enabled": False, "timer": 5}

    edit_db[chat_id]["enabled"] = state


async def set_timer(chat_id, timer):

    if chat_id not in edit_db:
        edit_db[chat_id] = {"enabled": False, "timer": 5}

    edit_db[chat_id]["timer"] = timer


async def get_edit_settings(chat_id):

    if chat_id not in edit_db:
        edit_db[chat_id] = {"enabled": False, "timer": 5}

    return edit_db[chat_id]


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
