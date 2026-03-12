from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[DATABASE_NAME]

filters = db["filters"]


# ADD FILTER

async def add_filter(chat_id, word, text=None, buttons=None, media=None):

    await filters.update_one(
        {"chat_id": chat_id, "word": word},
        {
            "$set": {
                "text": text,
                "buttons": buttons,
                "media": media
            }
        },
        upsert=True
    )


# REMOVE FILTER

async def remove_filter(chat_id, word):

    await filters.delete_one({
        "chat_id": chat_id,
        "word": word
    })


# REMOVE ALL FILTERS

async def remove_all_filters(chat_id):

    await filters.delete_many({
        "chat_id": chat_id
    })


# GET ALL FILTERS

async def get_filters(chat_id):

    data = filters.find({"chat_id": chat_id})

    result = {}

    async for item in data:
        result[item["word"]] = {
            "text": item.get("text"),
            "buttons": item.get("buttons"),
            "media": item.get("media")
        }

    return result


# GET SINGLE FILTER

async def get_filter(chat_id, word):

    data = await filters.find_one({
        "chat_id": chat_id,
        "word": word
    })

    if not data:
        return None

    return {
        "text": data.get("text"),
        "buttons": data.get("buttons"),
        "media": data.get("media")
    }
