from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, OWNER_ID

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["management"]

sudo_db = db["sudo_users"]


# ADD SUDO

async def add_sudo(user_id):

    data = await sudo_db.find_one({"user_id": user_id})

    if not data:
        await sudo_db.insert_one({
            "user_id": user_id
        })


# REMOVE SUDO

async def remove_sudo(user_id):

    await sudo_db.delete_one({
        "user_id": user_id
    })


# GET ALL SUDOS

async def get_sudos():

    users = []

    async for user in sudo_db.find():
        users.append(user["user_id"])

    return users


# OWNER CHECK

async def is_owner(user_id):

    return user_id == OWNER_ID


# SUDO CHECK

async def is_sudo(user_id):

    if user_id == OWNER_ID:
        return True

    data = await sudo_db.find_one({"user_id": user_id})

    return bool(data)


# BROADCAST PERMISSION

async def is_broadcast_allowed(user_id):

    return user_id == OWNER_ID
