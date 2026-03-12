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


# ---------------- SETTINGS COMMAND ---------------- #

@Client.on_message(filters.command("deleditmsg") & filters.group)
async def editmsg_settings(client, message: Message):

    if not await is_admin(client, message):
        return

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ON", callback_data="editmsg_on"),
            InlineKeyboardButton("OFF", callback_data="editmsg_off")
        ]
    ])

    await message.reply_text(
        "<b>Set edited message delete system:</b>",
        reply_markup=buttons
    )


# ---------------- BUTTON HANDLER ---------------- #

@Client.on_callback_query(filters.regex("^editmsg_"))
async def editmsg_toggle(client, query):

    member = await client.get_chat_member(query.message.chat.id, query.from_user.id)

    if member.status not in ["administrator", "creator"]:
        return await query.answer("Admins only!", show_alert=True)

    chat_id = query.message.chat.id

    if query.data == "editmsg_on":
        await toggle_edit_delete(chat_id, True)
        await query.message.edit_text("<b>Edited message delete system enabled</b>")

    elif query.data == "editmsg_off":
        await toggle_edit_delete(chat_id, False)
        await query.message.edit_text("<b>Edited message delete system disabled</b>")


# ---------------- TIMER COMMAND ---------------- #

@Client.on_message(filters.command("setdelmsgtimer") & filters.group)
async def set_timer_command(client, message: Message):

    if not await is_admin(client, message):
        return

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Increase Timer", callback_data="timer_increase")],
        [InlineKeyboardButton("Close", callback_data="timer_close")]
    ])

    await message.reply_text(
        "<b>Set edited message delete timer</b>",
        reply_markup=buttons
    )


# ---------------- TIMER BUTTONS ---------------- #

@Client.on_callback_query(filters.regex("^timer_"))
async def timer_buttons(client, query):

    member = await client.get_chat_member(query.message.chat.id, query.from_user.id)

    if member.status not in ["administrator", "creator"]:
        return await query.answer("Admins only!", show_alert=True)

    chat_id = query.message.chat.id

    data = await get_edit_settings(chat_id)

    timer = data.get("timer", 5)

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
                    f"<b>Timer set to {timer} minutes\nMaximum limit reached</b>",
                    reply_markup=buttons
                )

            else:

                await query.message.edit_text(
                    f"<b>Timer set to {timer} minutes</b>",
                    reply_markup=query.message.reply_markup
                )

    elif query.data == "timer_reset":

        await set_timer(chat_id, 5)

        await query.message.edit_text(
            "<b>Timer reset to default (5 minutes)</b>"
        )

    elif query.data == "timer_close":

        await query.message.delete()


# ---------------- EDIT DETECTION ---------------- #

@Client.on_edited_message(filters.group & filters.text)
async def detect_edit(client, message: Message):

    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    data = await get_edit_settings(chat_id)

    if not data.get("enabled"):
        return

    # skip admins
    try:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status in ["administrator", "creator"]:
            return
    except:
        return

    # skip approved users
    if await is_approved(chat_id, user_id):
        return

    timer = data.get("timer", 5)

    warn = await message.reply_text(
        f"<b>Edit detected.\n{message.from_user.mention} your message will be deleted in {timer} minutes.</b>"
    )

    await asyncio.sleep(timer * 60)

    try:
        await message.delete()
        await warn.delete()
    except:
        pass
