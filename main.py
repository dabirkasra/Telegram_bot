import os
import logging

from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

# Environment Variables
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# OpenAI
ai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

# Pyrogram
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)


@app.on_message(filters.private & filters.text)
async def private_chat(client, message):
    if message.from_user and message.from_user.is_self:
        return

    try:
        # نمایش حالت تایپ کردن
        await client.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING
        )

        # درخواست از OpenAI
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "تو یک دستیار هوشمند و مفید هستی."
                },
                {
                    "role": "user",
                    "content": message.text
                }
            ]
        )

        answer = response.choices[0].message.content

        if answer:
            await message.reply_text(answer)
        else:
            await message.reply_text("❌ پاسخی از هوش مصنوعی دریافت نشد.")

    except Exception as e:
        logging.exception("Error:")
        await message.reply_text(f"❌ خطا: {e}")


if __name__ == "__main__":
    print("🤖 Userbot is running...")
    app.run()