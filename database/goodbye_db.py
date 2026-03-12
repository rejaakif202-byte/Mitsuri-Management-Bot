from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[DATABASE_NAME]

goodbye = db["goodbye"]


# ENABLE / DISABLE GOODBYE

async def toggle_goodbye(chat_id, state):

    await goodbye.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": state}},
        upsert=True
    )


# SET GOODBYE MESSAGE

async def set_goodbye(chat_id, message):

    text = message.text or message.caption

    await goodbye.update_one(
        {"chat_id": chat_id},
        {"$set": {"text": text}},
        upsert=True
    )


# RESET GOODBYE

async def reset_goodbye(chat_id):

    await goodbye.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "enabled": True,
                "text": "Goodbye {first_name}, we hope to see you again in {Chatname}"
            }
        },
        upsert=True
    )


# GET GOODBYE SETTINGS

async def get_goodbye(chat_id):

    data = await goodbye.find_one({"chat_id": chat_id})

    if not data:

        default = {
            "chat_id": chat_id,
            "enabled": True,
            "text": "Goodbye {first_name}, we hope to see you again in {Chatname}"
        }

        await goodbye.insert_one(default)

        return default

    return data
