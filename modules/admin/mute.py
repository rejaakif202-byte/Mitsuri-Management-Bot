from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserAdminInvalid, ChatAdminRequired

# MUTE COMMAND

@Client.on_message(filters.command("mute") & filters.group)
async def mute_user(client: Client, message: Message):

    # Check admin
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.reply_text("You are not allowed to use this command.")

    # Bot permission check
    bot = await client.get_chat_member(message.chat.id, "me")
    if bot.status != "administrator":
        return await message.reply_text("I don't have enough permissions to mute users.")

    # Get target user
    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user = message.command[1]

        if user.startswith("@"):
            user_data = await client.get_users(user)
            user_id = user_data.id
        else:
            user_id = int(user)

    if not user_id:
        return await message.reply_text("Reply to a user or give a username/user_id.")

    # Check user exists
    try:
        target = await client.get_chat_member(message.chat.id, user_id)
    except:
        return await message.reply_text("this user is no longer exist here")

    # Prevent admin mute
    if target.status in ["administrator", "creator"]:
        return await message.reply_text("I can't mute an admin.")

    # Mute user
    try:
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions={}
        )
    except ChatAdminRequired:
        return await message.reply_text("I don't have enough permissions to mute users.")

    user = await client.get_users(user_id)

    await message.reply_text(
        f"{user.mention} is now muted from the chat"
    )


# UNMUTE COMMAND

@Client.on_message(filters.command("unmute") & filters.group)
async def unmute_user(client: Client, message: Message):

    # Check admin
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.reply_text("You are not allowed to use this command.")

    # Bot permission check
    bot = await client.get_chat_member(message.chat.id, "me")
    if bot.status != "administrator":
        return await message.reply_text("I don't have enough permissions to unmute users.")

    # Get target user
    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user = message.command[1]

        if user.startswith("@"):
            user_data = await client.get_users(user)
            user_id = user_data.id
        else:
            user_id = int(user)

    if not user_id:
        return await message.reply_text("Reply to a user or give a username/user_id.")

    # Check user exists
    try:
        await client.get_chat_member(message.chat.id, user_id)
    except:
        return await message.reply_text("this user is no longer exist here")

    # Unmute user
    await client.unban_chat_member(
        message.chat.id,
        user_id
    )

    user = await client.get_users(user_id)

    await message.reply_text(
        f"{user.mention} is now unmuted from the chat"
    )
