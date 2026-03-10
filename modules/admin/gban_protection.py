from pyrogram import Client, filters

from database.gban_db import is_gbanned


@Client.on_message(filters.new_chat_members)
async def auto_gban(client, message):

    for user in message.new_chat_members:

        if await is_gbanned(user.id):

            try:

                await client.ban_chat_member(
                    message.chat.id,
                    user.id
                )

            except:
                pass
