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
    logging.info(f"📩 پیام دریافت شد")
    
    if message.from_user.is_self:
        return
    
    if not message.text:
        return

    # ======== چک کردن پیوی با روش مطمئن ========
    try:
        chat_type = str(message.chat.type)
        logging.info(f"نوع چت: {chat_type}")
        
        if "PRIVATE" not in chat_type:
            logging.info("⏭️ گروه یا کانال")
            return
    except:
        logging.info("⏭️ خطا در تشخیص نوع چت")
        return

    logging.info("✅ پیوی شناسایی شد!")

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
    print("🤖 فقط پیوی!")
    app.run()