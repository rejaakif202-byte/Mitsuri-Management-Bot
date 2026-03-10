gban_users = set()


async def add_gban(user_id):

    gban_users.add(user_id)


async def remove_gban(user_id):

    gban_users.discard(user_id)


async def is_gbanned(user_id):

    if user_id in gban_users:
        return True

    return False


async def get_gbans():

    return list(gban_users)
