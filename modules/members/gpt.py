# Command: /gpt

import requests
import time
import threading

API_KEY = "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"

def auto_delete(chat_id, user_msg, bot_msg):

    time.sleep(300)

    try:
        bot.delete_message(chat_id, user_msg)
    except:
        pass

    try:
        bot.delete_message(chat_id, bot_msg)
    except:
        pass


try:

    args = message.text.split(" ",1)

    if len(args) < 2:
        bot.reply_to(message,"Usage:\n/gpt question")
        raise Exception("No question")

    question = args[1]

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    r = requests.post(url, headers=headers, json=data)

    res = r.json()

    answer = res["choices"][0]["message"]["content"]

    sent = bot.reply_to(message, answer)

    threading.Thread(
        target=auto_delete,
        args=(message.chat.id, message.message_id, sent.message_id)
    ).start()

except Exception as e:
    bot.reply_to(message, "Error:\n" + str(e))
