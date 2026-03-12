gmute_users = set()


async def add_gmute(user_id):

    gmute_users.add(user_id)


async def remove_gmute(user_id):

    gmute_users.discard(user_id)


async def is_gmuted(user_id):

    if user_id in gmute_users:
        return True

    return False


async def get_gmutes():

    return list(gmute_users)
