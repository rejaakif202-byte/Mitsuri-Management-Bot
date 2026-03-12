from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

approve_collection = db.approved


# ---------------- APPROVE USER ---------------- #

async def approve_user(chat_id, user_id):

    data = await approve_collection.find_one({"chat_id": chat_id})

    if not data:

        await approve_collection.insert_one({
            "chat_id": chat_id,
            "all": False,
            "users": [user_id]
        })

        return

    if user_id not in data["users"]:

        await approve_collection.update_one(
            {"chat_id": chat_id},
            {"$push": {"users": user_id}}
        )


# ---------------- UNAPPROVE USER ---------------- #

async def unapprove_user(chat_id, user_id):

    await approve_collection.update_one(
        {"chat_id": chat_id},
        {"$pull": {"users": user_id}}
    )


# ---------------- CHECK APPROVED ---------------- #

async def is_approved(chat_id, user_id):

    data = await approve_collection.find_one({"chat_id": chat_id})

    if not data:
        return False

    if data["all"]:
        return True

    if user_id in data["users"]:
        return True

    return False


# ---------------- APPROVE ALL ---------------- #

async def approve_all(chat_id):

    await approve_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"all": True}},
        upsert=True
    )


# ---------------- UNAPPROVE ALL ---------------- #

async def unapprove_all(chat_id):

    await approve_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"all": False, "users": []}},
        upsert=True
    )


# ---------------- GET APPROVED LIST ---------------- #

async def get_approved_list(chat_id):

    data = await approve_collection.find_one({"chat_id": chat_id})

    if not data:
        return []

    if data["all"]:
        return []

    return data["users"]
