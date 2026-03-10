from pyrogram import Client, filters
from pyrogram.types import Message
from database.gban_db import is_gbanned


@Client.on_message(filters.command("info"))
async def user_info(client: Client, message: Message):

    user = None

    # reply method
    if message.reply_to_message:
        user = message.reply_to_message.from_user

    # username method
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply_text("User not found.")

    # self
    else:
        user = message.from_user

    if not user:
        return await message.reply_text("User not found.")

    # full name
    first = user.first_name or ""
    last = user.last_name or ""
    fullname = (first + " " + last).strip()

    # username
    username = f"@{user.username}" if user.username else "@none"

    # bot check
    bot = "Yes" if user.is_bot else "No"

    # bio
    try:
        chat = await client.get_chat(user.id)
        bio = chat.bio if chat.bio else "none"
    except:
        bio = "none"

    # gban check
    gbanned = "Yes" if await is_gbanned(user.id) else "No"

    # group status
    status = ""
    if message.chat.type != "private":
        try:
            member = await client.get_chat_member(message.chat.id, user.id)

            if member.status == "creator":
                status = "owner"
            elif member.status == "administrator":
                status = "admin"
            else:
                status = "member"

        except:
            status = "member"

    # caption
    if message.chat.type == "private":

        caption = (
            "User Information :\n\n"
            f"User ID = <code>{user.id}</code>\n"
            f"Mention = {user.mention}\n"
            f"Full Name = {fullname}\n"
            f"Username = {username}\n"
            f"Bio = {bio}\n"
            f"Bot = {bot}\n"
            f"Gbanned = {gbanned}"
        )

    else:

        caption = (
            "User Information :\n\n"
            f"User ID = <code>{user.id}</code>\n"
            f"Mention = {user.mention}\n"
            f"Full Name = {fullname}\n"
            f"Username = {username}\n"
            f"Bio = {bio}\n"
            f"Group Status = {status}\n"
            f"Bot = {bot}\n"
            f"Gbanned = {gbanned}"
        )

    # profile photo send
    try:

        async for photo in client.get_chat_photos(user.id, limit=1):
            return await message.reply_photo(
                photo.file_id,
                caption=caption
            )

        await message.reply_text(caption)

    except:
        await message.reply_text(caption)
