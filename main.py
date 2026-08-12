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
    session_string=SESSION_STRING
)

@app.on_message()
async def all_messages(client, message):
    # چاپ کامل اطلاعات برای دیباگ
    logging.info(f"📩 پیام از: {message.chat.type} | آیدی چت: {message.chat.id} | متن: {message.text}")
    
    # نادیده گرفتن پیام‌های خودم
    if message.from_user.is_self:
        logging.info("⏭️ پیام از خودم")
        return
    
    # فقط پیام‌های متنی
    if not message.text:
        logging.info("⏭️ پیام غیر متنی")
        return

    # ======== فقط پیوی ========
    if message.chat.type != "private":
        logging.info(f"⏭️ گروه یا کانال (نوع: {message.chat.type})، نادیده گرفتم")
        return
    
    logging.info("✅ پیوی شناسایی شد! در حال پردازش...")

    try:
        await client.send_chat_action(message.chat.id, "typing")
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "تو یک دستیار هوشمند و مفید هستی."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=1000
        )
        await message.reply(response.choices[0].message.content)
        logging.info("✅ پاسخ ارسال شد")
        
    except Exception as e:
        error_msg = f"❌ خطا: {str(e)}"
        logging.error(error_msg)
        await message.reply(error_msg)

if __name__ == "__main__":
    print("🤖 یوزر بات فقط به پیوی پاسخ میدهد!")
    app.run()