async def is_admin(client, message):

    member = await client.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    return member.status in ["administrator", "creator"]
