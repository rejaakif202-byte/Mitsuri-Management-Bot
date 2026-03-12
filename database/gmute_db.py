from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo[DATABASE_NAME]

gmute = db["gmute_users"]


# ADD GMUTE

async def add_gmute(user_id):

    data = await gmute.find_one({"user_id": user_id})

    if not data:
        await gmute.insert_one({
            "user_id": user_id
        })


# REMOVE GMUTE

async def remove_gmute(user_id):

    await gmute.delete_one({
        "user_id": user_id
    })


# CHECK GMUTE

async def is_gmuted(user_id):

    data = await gmute.find_one({
        "user_id": user_id
    })

    return bool(data)


# GET ALL GMUTES

async def get_gmutes():

    data = gmute.find()

    users = []

    async for user in data:
        users.append(user["user_id"])

    return users
