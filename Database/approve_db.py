approve_db = {}


# ---------------- APPROVE USER ---------------- #

async def approve_user(chat_id, user_id):

    if chat_id not in approve_db:
        approve_db[chat_id] = {"all": False, "users": []}

    if user_id not in approve_db[chat_id]["users"]:
        approve_db[chat_id]["users"].append(user_id)


# ---------------- UNAPPROVE USER ---------------- #

async def unapprove_user(chat_id, user_id):

    if chat_id in approve_db:

        if user_id in approve_db[chat_id]["users"]:
            approve_db[chat_id]["users"].remove(user_id)


# ---------------- CHECK APPROVED ---------------- #

async def is_approved(chat_id, user_id):

    if chat_id not in approve_db:
        return False

    if approve_db[chat_id]["all"]:
        return True

    if user_id in approve_db[chat_id]["users"]:
        return True

    return False


# ---------------- APPROVE ALL ---------------- #

async def approve_all(chat_id):

    if chat_id not in approve_db:
        approve_db[chat_id] = {"all": True, "users": []}
    else:
        approve_db[chat_id]["all"] = True


# ---------------- UNAPPROVE ALL ---------------- #

async def unapprove_all(chat_id):

    approve_db[chat_id] = {"all": False, "users": []}


# ---------------- GET APPROVED LIST ---------------- #

async def get_approved_list(chat_id):

    if chat_id not in approve_db:
        return []

    if approve_db[chat_id]["all"]:
        return []

    return approve_db[chat_id]["users"]
