users = set()


async def add_user(user_id):

    users.add(user_id)


async def get_users():

    return list(users)
