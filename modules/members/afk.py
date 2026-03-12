import time
import random
from pyrogram import Client, filters
from pyrogram.types import Message

afk_users = {}

# AFK activate lines
afk_lines = [
"I shall take my leave for a while; duties beyond this realm now summon me.",
"Pray excuse my absence, for I must depart and wander afar for a time.",
"I withdraw from this discourse for the moment; summon me again when fate allows.",
"For a brief hour I vanish into silence—think not I have abandoned thee.",
"My presence fades for now; the world beyond this screen demands my attention.",
"Permit me a short retreat, for matters of the mortal world call upon me.",
"I shall be but a shadow for a while; await my return with patience.",
"Let it be known that I depart for a time, though my return shall not be long delayed.",
"Silence shall claim me for the moment; speak freely until I walk these halls again.",
"I step away from this gathering for a spell, yet I shall return when time permits."
]

# Mention lines
mention_lines = [
"Thy call echoes in vain, for I am absent from this place.",
"Summon me not, for I wander afar and cannot heed thy voice.",
"Though thou callest my name, I am but a silent shadow for now.",
"Your summons reaches empty halls; I am away for a time.",
"Call as thou may, yet I shall not answer until my return.",
"Thy voice is heard not by me, for I am presently absent.",
"Seek me not at this hour, for I have departed for a while.",
"Though my name be spoken, I am not here to answer thee.",
"The bell you ring finds no keeper; I am away from these chambers.",
"Thy call is noted, yet my presence shall return only in time."
]

# Welcome back lines
back_lines = [
"Lo, thou hast returned from thy silent wandering.",
"The absent soul walks among us once more.",
"At last thy shadow graces these halls again.",
"The silence breaks, for thou hast returned.",
"From distant absence thou hast found thy way back.",
"Welcome back; thy presence was sorely missed.",
"The void thou left behind is now filled again.",
"Thy return ends the quiet that once lingered here.",
"The halls awaken again with thy presence.",
"From thy brief exile thou hast come back to these chambers."
]


def format_time(seconds):

    days = seconds // 86400
    seconds %= 86400

    hours = seconds // 3600
    seconds %= 3600

    minutes = seconds // 60
    seconds %= 60

    parts = []

    if days:
        parts.append(f"{days}d")

    if hours:
        parts.append(f"{hours}h")

    if minutes:
        parts.append(f"{minutes}m")

    if seconds:
        parts.append(f"{seconds}s")

    return " ".join(parts)


@Client.on_message(filters.command("afk"))
async def set_afk(client: Client, message: Message):

    user = message.from_user
    reason = None

    if len(message.command) > 1:
        reason = message.text.split(None, 1)[1]

    afk_users[user.id] = {
        "time": time.time(),
        "reason": reason
    }

    line = random.choice(afk_lines)

    if reason:
        text = f"{user.mention} is now AFK\n{line}\nReason: {reason}"
    else:
        text = f"{user.mention} is now AFK\n{line}"

    await message.reply_text(text)


@Client.on_message(filters.all)
async def afk_watcher(client: Client, message: Message):

    user = message.from_user

    if not user:
        return

    # Remove AFK if user sends message
    if user.id in afk_users and not message.text.startswith("/afk"):

        data = afk_users.pop(user.id)

        duration = format_time(int(time.time() - data["time"]))

        line = random.choice(back_lines)

        if data["reason"]:
            text = (
                f"Welcome Back {user.mention}\n"
                f"{line}\n"
                f"You were AFK for: {duration}\n"
                f"Reason: {data['reason']}"
            )
        else:
            text = (
                f"Welcome Back {user.mention}\n"
                f"{line}\n"
                f"You were AFK for: {duration}"
            )

        await message.reply_text(text)

    # Reply detection
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        if target and target.id in afk_users:

            data = afk_users[target.id]

            duration = format_time(int(time.time() - data["time"]))

            line = random.choice(mention_lines)

            if data["reason"]:
                text = (
                    f"{target.mention}\n"
                    f"{line}\n"
                    f"Since: {duration}\n"
                    f"Reason: {data['reason']}"
                )
            else:
                text = (
                    f"{target.mention}\n"
                    f"{line}\n"
                    f"Since: {duration}"
                )

            await message.reply_text(text)

    # Mention detection
    if message.entities:

        for entity in message.entities:

            if entity.type == "mention":

                username = message.text[
                    entity.offset: entity.offset + entity.length
                ]

                try:

                    user_obj = await client.get_users(username)

                    if user_obj.id in afk_users:

                        data = afk_users[user_obj.id]

                        duration = format_time(
                            int(time.time() - data["time"])
                        )

                        line = random.choice(mention_lines)

                        if data["reason"]:
                            text = (
                                f"{user_obj.mention}\n"
                                f"{line}\n"
                                f"Since: {duration}\n"
                                f"Reason: {data['reason']}"
                            )
                        else:
                            text = (
                                f"{user_obj.mention}\n"
                                f"{line}\n"
                                f"Since: {duration}"
                            )

                        await message.reply_text(text)

                except:
                    pass
