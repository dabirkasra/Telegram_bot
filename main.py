import os
import logging
from pyrogram import Client, filters
from pyrogram.enums import ChatType
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
    logging.info(f"📩 پیام از: {message.chat.type} | متن: {message.text}")
    
    if message.from_user.is_self:
        return
    
    if not message.text:
        return

    # ======== فقط پیوی ========
    if message.chat.type != ChatType.PRIVATE:
        logging.info("⏭️ گروه یا کانال، نادیده گرفتم")
        return

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
        
    except Exception as e:
        await message.reply(f"❌ خطا: {str(e)}")

if __name__ == "__main__":
    print("🤖 فقط پیوی!")
    app.run()