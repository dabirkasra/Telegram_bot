import os
import logging
from pyrogram import Client, filters
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

ai_client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.openai.com/v1"
)

app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    workdir="./",
    sleep_threshold=60,
    no_updates=True
)

@app.on_message(filters.private & filters.text)
async def private_chat(client, message):
    # این خط رو حتماً توی لاگ میبینی
    logging.info(f"📩 پیام جدید از {message.from_user.id}: {message.text}")
    
    if message.from_user.is_self:
        logging.info("⏭️ پیام از خودم بود، نادیده گرفتم")
        return

    try:
        await client.send_chat_action(chat_id=message.chat.id, action="typing")
        
        logging.info("🤖 ارسال به OpenAI...")
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "تو یک دستیار هوشمند و مفید هستی."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=1000
        )
        
        reply = response.choices[0].message.content
        logging.info(f"✅ پاسخ دریافت شد: {reply[:30]}...")
        await message.reply(reply)
        
    except Exception as e:
        error_msg = f"❌ خطا: {str(e)}"
        logging.error(error_msg)
        await message.reply(error_msg)

if __name__ == "__main__":
    print("🤖 یوزر بات روشن شد!")
    app.run()