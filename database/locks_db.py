from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["management"]

locks_db = db["locks"]
approve_db = db["approved_users"]


# ---------------- APPROVE USER ---------------- #

async def approve_user(chat_id, user_id):

    data = await approve_db.find_one({"chat_id": chat_id})

    if not data:
        await approve_db.insert_one({
            "chat_id": chat_id,
            "users": [user_id]
        })
        return

    if user_id not in data["users"]:
        await approve_db.update_one(
            {"chat_id": chat_id},
            {"$push": {"users": user_id}}
        )


# ---------------- UNAPPROVE USER ---------------- #

async def unapprove_user(chat_id, user_id):

    await approve_db.update_one(
        {"chat_id": chat_id},
        {"$pull": {"users": user_id}}
    )


# ---------------- CHECK APPROVED ---------------- #

async def is_approved(chat_id, user_id):

    data = await approve_db.find_one({"chat_id": chat_id})

    if not data:
        return False

    return user_id in data["users"]


# ---------------- ADD LOCK ---------------- #

async def add_lock(chat_id, lock):

    data = await locks_db.find_one({"chat_id": chat_id})

    if not data:
        await locks_db.insert_one({
            "chat_id": chat_id,
            "locks": [lock]
        })
        return

    if lock not in data["locks"]:
        await locks_db.update_one(
            {"chat_id": chat_id},
            {"$push": {"locks": lock}}
        )


# ---------------- REMOVE LOCK ---------------- #

async def remove_lock(chat_id, lock):

    await locks_db.update_one(
        {"chat_id": chat_id},
        {"$pull": {"locks": lock}}
    )


# ---------------- GET LOCKS ---------------- #

async def get_locks(chat_id):

    data = await locks_db.find_one({"chat_id": chat_id})

    if not data:
        return []

    return data["locks"]
