import os
from pyrogram import Client, filters
from openai import OpenAI

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

ai_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.on_message(filters.text & (filters.private | filters.group))
async def handle_message(client, message):
    if message.from_user.is_self:
        return
    await client.send_chat_action(message.chat.id, "typing")
    try:
        response = ai_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "تو یک دستیار هوشمند و فارسی‌زبان هستی."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=1000
        )
        await message.reply(response.choices[0].message.content)
    except Exception as e:
        await message.reply(f"❌ خطا: {str(e)}")

if __name__ == "__main__":
    print("🤖 یوزر بات با Session روشن شد!")
    app.run()