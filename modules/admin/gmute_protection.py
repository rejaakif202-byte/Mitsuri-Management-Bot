from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

from database.gmute_db import is_gmuted


@Client.on_message(filters.new_chat_members)
async def auto_gmute(client, message):

    for user in message.new_chat_members:

        if await is_gmuted(user.id):

            try:

                await client.restrict_chat_member(
                    message.chat.id,
                    user.id,
                    ChatPermissions()
                )

            except:
                pass
