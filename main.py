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

SPECIAL_CHAT_ID = 123456789  # آیدی اون شخص خاص
OFF_FOR_SPECIAL = False  # وضعیت خاموشی فقط برای اون چت

@app.on_message(filters.private & filters.text)
async def private_chat(client, message):
    global OFF_FOR_SPECIAL
    if message.from_user.is_self:
        return

    chat_id = message.chat.id

    # ======== دستورات فقط برای اون چت خاص ========
    if chat_id == SPECIAL_CHAT_ID:
        if message.text == "/off":
            OFF_FOR_SPECIAL = True
            await message.reply("🔇 ربات در این چت خاموش شد!")
            return

        if message.text == "/on":
            OFF_FOR_SPECIAL = False
            await message.reply("🔊 ربات در این چت روشن شد!")
            return

        # اگه اون چت خاموشه، جواب نده
        if OFF_FOR_SPECIAL:
            return

    # ======== بقیه پیوی‌ها و اون چت (اگه خاموش نباشه) ========
    try:
        await client.send_chat_action(chat_id, "typing")
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        await message.reply(response.choices[0].message.content)
    except Exception as e:
        await message.reply(f"❌ {e}")

if __name__ == "__main__":
    print("🤖 ربات در همه پیوی‌ها فعال است!")
    app.run()