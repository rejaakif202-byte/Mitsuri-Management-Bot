OWNER_ID = 7846306818

sudo_users = set()


async def add_sudo(user_id):

    sudo_users.add(user_id)


async def remove_sudo(user_id):

    sudo_users.discard(user_id)


async def get_sudos():

    return list(sudo_users)


async def is_owner(user_id):

    return user_id == OWNER_ID


async def is_sudo(user_id):

    if user_id == OWNER_ID:
        return True

    if user_id in sudo_users:
        return True

    return False


async def is_broadcast_allowed(user_id):

    if user_id == OWNER_ID:
        return True

    return False
