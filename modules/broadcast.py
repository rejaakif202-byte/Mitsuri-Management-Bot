from pyrogram import Client, filters
from pyrogram.types import Message

from database.users_db import get_users
from database.sudo_db import OWNER_ID


@Client.on_message(filters.command("broadcast"))
async def broadcast(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to broadcast."
        )

    start = await message.reply_text("Broadcast begining")

    groups_success = 0
    groups_failed = 0

    users_success = 0
    users_failed = 0

    # GROUP BROADCAST
    async for dialog in client.get_dialogs():

        if dialog.chat.type in ["group", "supergroup"]:

            try:

                await message.reply_to_message.copy(
                    dialog.chat.id
                )

                groups_success += 1

            except:

                groups_failed += 1

    # USER BROADCAST
    users = await get_users()

    for user_id in users:

        try:

            await message.reply_to_message.copy(
                user_id
            )

            users_success += 1

        except:

            users_failed += 1

    await start.delete()

    await message.reply_text(

        f"broadcast completed\n\n"
        f"successful : {groups_success} groups, {users_success} users\n"
        f"unsuccessful : {groups_failed} groups, {users_failed} users"

    )
