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

# ======== دریافت همه پیام‌های متنی ========
@app.on_message(filters.text)
async def all_messages(client, message):
    # لاگ برای دیباگ
    logging.info(f"📩 پیام از: {message.from_user.id} | چت: {message.chat.id} | متن: {message.text}")
    
    # اگه پیام از خودم بود، نادیده بگیر
    if message.from_user.is_self:
        logging.info("⏭️ پیام از خودم")
        return
    
    # فقط به پیام‌های خصوصی پاسخ بده (گروه رو نادیده بگیر)
    if message.chat.type not in ["private"]:
        logging.info("⏭️ گروه یا کانال، نادیده گرفتم")
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
        logging.info(f"✅ پاسخ: {reply[:30]}...")
        await message.reply(reply)
        
    except Exception as e:
        error_msg = f"❌ خطا: {str(e)}"
        logging.error(error_msg)
        await message.reply(error_msg)

if __name__ == "__main__":
    print("🤖 یوزر بات روشن شد!")
    app.run()