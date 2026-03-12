deledit_db = {}


async def toggle_edit_delete(chat_id, status):

    if chat_id not in deledit_db:
        deledit_db[chat_id] = {"enabled": False, "timer": 5}

    deledit_db[chat_id]["enabled"] = status


async def set_timer(chat_id, timer):

    if chat_id not in deledit_db:
        deledit_db[chat_id] = {"enabled": False, "timer": 5}

    deledit_db[chat_id]["timer"] = timer


async def get_edit_settings(chat_id):

    if chat_id not in deledit_db:
        deledit_db[chat_id] = {"enabled": False, "timer": 5}

    return deledit_db[chat_id]
