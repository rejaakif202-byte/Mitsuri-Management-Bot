from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from utils.permissions import is_admin
from database.deledit_db import (
    toggle_edit_delete,
    get_edit_settings,
    set_timer
)

from database.approve_db import is_approved


# /deleditmsg

@Client.on_message(filters.command("deleditmsg") & filters.group)
async def editmsg_settings(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text("<b>You are not allowed to use this command</b>")

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ON", callback_data="editmsg_on"),
            InlineKeyboardButton("OFF", callback_data="editmsg_off")
        ]
    ])

    await message.reply_text(
        "<b>Set your delete edited message to:</b>",
        reply_markup=buttons
    )


# BUTTON HANDLER

@Client.on_callback_query(filters.regex("editmsg_"))
async def editmsg_toggle(client, query):

    chat_id = query.message.chat.id

    if query.data == "editmsg_on":
        await toggle_edit_delete(chat_id, True)
        await query.message.edit_text("<b>Edited message delete system enabled</b>")

    elif query.data == "editmsg_off":
        await toggle_edit_delete(chat_id, False)
        await query.message.edit_text("<b>Edited message delete system disabled</b>")


# TIMER COMMAND

@Client.on_message(filters.command("setdelmsgtimer") & filters.group)
async def set_timer_command(client, message: Message):

    if not await is_admin(client, message):
        return await message.reply_text("<b>You are not allowed to use this command</b>")

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Increase Timer", callback_data="timer_increase")],
        [InlineKeyboardButton("Close", callback_data="timer_close")]
    ])

    await message.reply_text(
        "<b>Set your edited message delete timer</b>",
        reply_markup=buttons
    )


# TIMER BUTTON

@Client.on_callback_query(filters.regex("timer_"))
async def timer_buttons(client, query):

    chat_id = query.message.chat.id
    data = await get_edit_settings(chat_id)

    timer = data["timer"]

    if query.data == "timer_increase":

        if timer < 30:
            timer += 5
            await set_timer(chat_id, timer)

            if timer == 30:
                buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Back To Default", callback_data="timer_reset")],
                    [InlineKeyboardButton("Close", callback_data="timer_close")]
                ])

                await query.message.edit_text(
                    f"<b>Your timer is now {timer} minutes\nThis is the maximum limit</b>",
                    reply_markup=buttons
                )
            else:
                await query.message.edit_text(
                    f"<b>Your timer is now {timer} minutes</b>",
                    reply_markup=query.message.reply_markup
                )

    elif query.data == "timer_reset":

        await set_timer(chat_id, 5)

        await query.message.edit_text(
            "<b>Timer reset to default (5 minutes)</b>"
        )

    elif query.data == "timer_close":

        await query.message.delete()


# EDIT DETECTION

@Client.on_edited_message(filters.group)
async def detect_edit(client, message: Message):

    chat_id = message.chat.id
    user = message.from_user

    data = await get_edit_settings(chat_id)

    if not data["enabled"]:
        return

    if await is_approved(chat_id, user.id):
        return

    timer = data["timer"]

    warn = await message.reply_text(
        f"<b>Edit message detected, {user.mention} your message and this message will be deleted in {timer} minutes</b>"
    )

    await asyncio.sleep(timer * 60)

    try:
        await message.delete()
        await warn.delete()
    except:
        pass
