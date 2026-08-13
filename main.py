import os
import logging

from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from google import genai

logging.basicConfig(level=logging.INFO)

# Telegram
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Gemini client
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Telegram client
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
        # نمایش حالت typing
        await client.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING
        )

        # درخواست به Gemini
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": (
                                "تو یک دستیار هوشمند و مفید هستی. "
                                "به زبان فارسی و به شکل دوستانه پاسخ بده.\n\n"
                                f"پیام کاربر:\n{message.text}"
                            )
                        }
                    ]
                }
            ]
        )

        answer = response.text

        if answer:
            await message.reply_text(answer)
        else:
            await message.reply_text(
                "❌ Gemini پاسخی برنگرداند."
            )

    except Exception as e:
        logging.exception("Gemini error")

        await message.reply_text(
            f"❌ خطا: {e}"
        )


if __name__ == "__main__":
    print("🤖 Userbot with Gemini is running...")
    app.run()