from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("id"))
async def get_id(client: Client, message: Message):

    user = message.from_user

    # 1️⃣ username/id argument
    if len(message.command) > 1:
        try:
            target = await client.get_users(message.command[1])

            return await message.reply_text(
                f"{target.mention} ID: <code>{target.id}</code>"
            )
        except:
            return await message.reply_text("User not found.")

    # 2️⃣ reply to forwarded channel/group message (works mostly in DM)
    if message.reply_to_message and message.reply_to_message.forward_from_chat:

        chat = message.reply_to_message.forward_from_chat

        return await message.reply_text(
            f"{chat.title} ID: <code>{chat.id}</code>"
        )

    # 3️⃣ DM usage
    if message.chat.type == "private":

        return await message.reply_text(
            f"User {user.mention} ID is: <code>{user.id}</code>"
        )

    # 4️⃣ Group usage
    if message.chat.type in ["group", "supergroup"]:

        return await message.reply_text(
            f"Your ID: <code>{user.id}</code>\n"
            f"Chat ID: <code>{message.chat.id}</code>"
        )
