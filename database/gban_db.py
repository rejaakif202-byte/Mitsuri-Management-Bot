from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[DATABASE_NAME]

gban = db["gban_users"]


# ADD GBAN

async def add_gban(user_id):

    data = await gban.find_one({"user_id": user_id})

    if not data:
        await gban.insert_one({
            "user_id": user_id
        })


# REMOVE GBAN

async def remove_gban(user_id):

    await gban.delete_one({
        "user_id": user_id
    })


# CHECK GBAN

async def is_gbanned(user_id):

    data = await gban.find_one({
        "user_id": user_id
    })

    return bool(data)


# GET ALL GBANS

async def get_gbans():

    data = gban.find()

    users = []

    async for user in data:
        users.append(user["user_id"])

    return users
