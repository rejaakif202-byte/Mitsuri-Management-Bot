from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

welcome_collection = db.welcome


# TOGGLE WELCOME

async def toggle_welcome(chat_id, state):

    data = await welcome_collection.find_one({"chat_id": chat_id})

    if not data:
        await welcome_collection.insert_one({
            "chat_id": chat_id,
            "enabled": state,
            "text": "hey there {first_name}, welcome to {Chatname}. How are you!?"
        })
    else:
        await welcome_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"enabled": state}}
        )


# SET WELCOME MESSAGE

async def set_welcome(chat_id, message):

    text = message.text or message.caption

    data = await welcome_collection.find_one({"chat_id": chat_id})

    if not data:
        await welcome_collection.insert_one({
            "chat_id": chat_id,
            "enabled": True,
            "text": text
        })
    else:
        await welcome_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"text": text}}
        )


# RESET WELCOME

async def reset_welcome(chat_id):

    await welcome_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "enabled": True,
            "text": "hey there {first_name}, welcome to {Chatname}. How are you!?"
        }},
        upsert=True
    )


# GET WELCOME DATA

async def get_welcome(chat_id):

    data = await welcome_collection.find_one({"chat_id": chat_id})

    if not data:
        default = {
            "chat_id": chat_id,
            "enabled": True,
            "text": "hey there {first_name}, welcome to {Chatname}. How are you!?"
        }

        await welcome_collection.insert_one(default)
        return default

    return data
