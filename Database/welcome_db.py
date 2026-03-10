welcome_db = {}


async def toggle_welcome(chat_id, state):

    if chat_id not in welcome_db:
        welcome_db[chat_id] = {}

    welcome_db[chat_id]["enabled"] = state


async def set_welcome(chat_id, message):

    if chat_id not in welcome_db:
        welcome_db[chat_id] = {}

    welcome_db[chat_id]["text"] = message.text or message.caption


async def reset_welcome(chat_id):

    welcome_db[chat_id] = {
        "enabled": True,
        "text": "hey there {first_name}, welcome to {Chatname}. How are you!?"
    }


async def get_welcome(chat_id):

    if chat_id not in welcome_db:

        welcome_db[chat_id] = {
            "enabled": True,
            "text": "hey there {first_name}, welcome to {Chatname}. How are you!?"
        }

    return welcome_db[chat_id]
