from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["management"]

promoted_db = db["promoted_admins"]


# ADD PROMOTED ADMIN

async def add_promoted(chat_id, user_id):

    data = await promoted_db.find_one({"chat_id": chat_id})

    if not data:
        await promoted_db.insert_one({
            "chat_id": chat_id,
            "admins": [user_id]
        })
        return

    if user_id not in data["admins"]:
        await promoted_db.update_one(
            {"chat_id": chat_id},
            {"$push": {"admins": user_id}}
        )


# REMOVE PROMOTED ADMIN

async def remove_promoted(chat_id, user_id):

    await promoted_db.update_one(
        {"chat_id": chat_id},
        {"$pull": {"admins": user_id}}
    )


# CHECK PROMOTED

async def is_promoted(chat_id, user_id):

    data = await promoted_db.find_one({"chat_id": chat_id})

    if not data:
        return False

    return user_id in data["admins"]


# GET PROMOTED ADMINS

async def get_promoted(chat_id):

    data = await promoted_db.find_one({"chat_id": chat_id})

    if not data:
        return []

    return data["admins"]
