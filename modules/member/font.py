from Utils.fonts import convert_font
from Database.fontdb import save_text, get_text, delete_text

fonts = [
"smallcaps","sans","reverse",
"greekmix","greekbold","serif",
"typewriter","bubble","outline",
"sansbold","sansitalic","sansbolditalic",
"monospace","tiny","normal"
]


# Command: /font

try:

    parts = message.text.split(" ",1)

    if len(parts) < 2:
        bot.reply_to(message,"Usage:\n/font text")
        return

    text = parts[1]
    user_id = message.from_user.id

    save_text(user_id,text)

    keyboard = []
    row = []

    for font in fonts:

        row.append({
        "text":font,
        "callback_data":"font_"+font
        })

        if len(row) == 3:
            keyboard.append(row)
            row = []

    keyboard.append([
    {"text":"❌ Close","callback_data":"font_close"}
    ])

    bot.reply_to(
        message,
        text,  # 👈 caption me user ka text
        reply_markup={"inline_keyboard":keyboard}
    )

except:
    pass


# Callback

if data.startswith("font_"):

    user_id = call.from_user.id

    if data == "font_close":

        delete_text(user_id)

        bot.delete_message(
        call.message.chat.id,
        call.message.message_id
        )

    else:

        font = data.replace("font_","")

        text = get_text(user_id)

        if not text:
            bot.answer_callback_query(
            call.id,
            "Text expired"
            )
            return

        result = convert_font(text,font)

        bot.edit_message_text(
            result,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=call.message.reply_markup
        )
