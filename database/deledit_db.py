from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[DATABASE_NAME]

deledit = db["deledit"]


# TOGGLE EDIT DELETE

async def toggle_edit_delete(chat_id, status):

    data = await deledit.find_one({"chat_id": chat_id})

    if not data:
        await deledit.insert_one({
            "chat_id": chat_id,
            "enabled": status,
            "timer": 5
        })
        return

    await deledit.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}}
    )


# SET TIMER

async def set_timer(chat_id, timer):

    data = await deledit.find_one({"chat_id": chat_id})

    if not data:
        await deledit.insert_one({
            "chat_id": chat_id,
            "enabled": False,
            "timer": timer
        })
        return

    await deledit.update_one(
        {"chat_id": chat_id},
        {"$set": {"timer": timer}}
    )


# GET SETTINGS

async def get_edit_settings(chat_id):

    data = await deledit.find_one({"chat_id": chat_id})

    if not data:
        return {"enabled": False, "timer": 5}

    return {
        "enabled": data.get("enabled", False),
        "timer": data.get("timer", 5)
    }
