import os
import logging
from pyrogram import Client, filters
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

ai_client = OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.openai.com/v1")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# ======== اینجا آیدی خودت رو بذار (یه بار بگیر) ========
MY_ID = 8943898299  # آیدی خودت رو با @userinfobot بگیر

# ======== لیست چت‌هایی که فقط خودت میتونی خاموش کنی ========
off_chats = set()

@app.on_message(filters.private & filters.text)
async def private_chat(client, message):
    if message.from_user.is_self:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # ======== دستور خاموش کردن (فقط برای خودت) ========
    if message.text.startswith("/off") and user_id == MY_ID:
        off_chats.add(chat_id)
        await message.reply("🔇 ربات در این چت خاموش شد!")
        return

    if message.text.startswith("/on") and user_id == MY_ID:
        off_chats.discard(chat_id)
        await message.reply("🔊 ربات در این چت روشن شد!")
        return

    # ======== اگه چت توی لیست خاموشی‌هاست، جواب نده ========
    if chat_id in off_chats:
        return

    # ======== پاسخ به بقیه ========
    try:
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.reply(response.choices[0].message.content)
    except Exception as e:
        await message.reply(f"❌ {e}")

if __name__ == "__main__":
    print("🤖 ربات فعاله!")
    app.run()