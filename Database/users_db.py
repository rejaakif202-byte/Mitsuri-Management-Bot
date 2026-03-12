from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

users_collection = db.users
chats_collection = db.chats


# ADD USER

async def add_user(user_id):

    user = await users_collection.find_one({"user_id": user_id})

    if not user:
        await users_collection.insert_one({"user_id": user_id})


# ADD CHAT

async def add_chat(chat_id):

    chat = await chats_collection.find_one({"chat_id": chat_id})

    if not chat:
        await chats_collection.insert_one({"chat_id": chat_id})


# GET USERS LIST

async def get_users():

    users = []
    async for user in users_collection.find():
        users.append(user["user_id"])

    return users


# GET CHATS LIST

async def get_chats():

    chats = []
    async for chat in chats_collection.find():
        chats.append(chat["chat_id"])

    return chats


# TOTAL USERS

async def get_total_users():
    return await users_collection.count_documents({})


# TOTAL CHATS

async def get_total_chats():
    return await chats_collection.count_documents({})
