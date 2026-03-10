goodbye_db = {}


async def toggle_goodbye(chat_id, state):

    if chat_id not in goodbye_db:
        goodbye_db[chat_id] = {}

    goodbye_db[chat_id]["enabled"] = state


async def set_goodbye(chat_id, message):

    if chat_id not in goodbye_db:
        goodbye_db[chat_id] = {}

    goodbye_db[chat_id]["text"] = message.text or message.caption


async def reset_goodbye(chat_id):

    goodbye_db[chat_id] = {
        "enabled": True,
        "text": "Goodbye {first_name}, we hope to see you again in {Chatname}"
    }


async def get_goodbye(chat_id):

    if chat_id not in goodbye_db:

        goodbye_db[chat_id] = {
            "enabled": True,
            "text": "Goodbye {first_name}, we hope to see you again in {Chatname}"
        }

    return goodbye_db[chat_id]
