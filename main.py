import os
import logging
from pyrogram import Client, filters
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# ======== هوش مصنوعی ========
ai_client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.openai.com/v1"
)

# ======== اتصال به تلگرام با تنظیمات بیشتر ========
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    workdir="./",
    # برای اتصال بهتر
    sleep_threshold=60,
    no_updates=True
)

# ======== فقط پیوی ========
@app.on_message(filters.private & filters.text)
async def private_chat(client, message):
    if message.from_user.is_self:
        return
    
    logging.info(f"📩 پیوی از {message.from_user.id}: {message.text}")
    
    try:
        # ارسال وضعیت تایپ
        await client.send_chat_action(chat_id=message.chat.id, action="typing")
        
        # دریافت پاسخ از OpenAI
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "تو یک دستیار هوشمند و مفید هستی. پاسخ‌هایت مختصر و دقیق باشد."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=1000
        )
        
        await message.reply(response.choices[0].message.content)
        
    except Exception as e:
        error_msg = f"❌ خطا: {str(e)}"
        logging.error(error_msg)
        await message.reply(error_msg)

# ======== گروه (غیرفعال) ========
# برای فعال کردن گروه، این قسمت رو از حالت کامنت خارج کن
"""
@app.on_message(filters.group & filters.text)
async def group_chat(client, message):
    # فقط به منشن‌ها پاسخ بده
    if not message.mentioned and not message.reply_to_message:
        return
    
    if message.from_user.is_self:
        return
    
    await client.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "تو یک دستیار هوشمند و مفید هستی."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=1000
        )
        await message.reply(response.choices[0].message.content)
    except Exception as e:
        await message.reply(f"❌ خطا: {str(e)}")
"""

# ======== اجرا ========
if __name__ == "__main__":
    print("🤖 یوزر بات فقط در پیوی فعال است!")
    app.run()