from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[DATABASE_NAME]

blacklist = db["blacklist"]


# ADD BLACKLIST WORD

async def add_blacklist(chat_id, word):

    data = await blacklist.find_one({"chat_id": chat_id})

    if not data:
        await blacklist.insert_one({
            "chat_id": chat_id,
            "words": [word]
        })
        return

    if word not in data["words"]:
        await blacklist.update_one(
            {"chat_id": chat_id},
            {"$push": {"words": word}}
        )


# REMOVE BLACKLIST WORD

async def remove_blacklist(chat_id, word):

    await blacklist.update_one(
        {"chat_id": chat_id},
        {"$pull": {"words": word}}
    )


# GET BLACKLIST WORDS

async def get_blacklist(chat_id):

    data = await blacklist.find_one({"chat_id": chat_id})

    if not data:
        return []

    return data.get("words", [])
