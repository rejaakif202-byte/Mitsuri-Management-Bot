edit_db = {}


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
