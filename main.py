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

@app.on_message(filters.private & filters.text)
async def private_chat(client, message):
    if message.from_user.is_self:
        return

    logging.info(f"📩 پیام از {message.from_user.id}: {message.text}")

    try:
        # تست ۱: وضعیت تایپ
        await client.send_chat_action(chat_id=message.chat.id, action="typing")
        logging.info("✅ تایپ فرستاده شد")

        # تست ۲: درخواست به OpenAI
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        logging.info("✅ پاسخ از OpenAI اومد")

        # تست ۳: ارسال جواب
        await message.reply(response.choices[0].message.content)
        logging.info("✅ جواب فرستاده شد")

    except Exception as e:
        logging.error(f"❌ خطا: {str(e)}")
        await message.reply(f"❌ {str(e)}")

if __name__ == "__main__":
    print("🤖 ربات روشن شد!")
    app.run()