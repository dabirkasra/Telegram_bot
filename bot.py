from telethon import TelegramClient, events
import asyncio

# ============ اطلاعات خودت (دقیق پر کن) ============
api_id = 32059999
api_hash = '848e4041e84bff7907db68fd7ac3c37b'  # این رو عوض کن با جدیدش
phone = '+918527529308'  # شماره با کد کشور (مثل 989123456789)

# ============ ساخت کلاینت ============
client = TelegramClient('session', api_id, api_hash)

# ============ قفل پیوی ============
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private and not event.out:
        await event.reply('🔒 پیوی قفل شده! بعداً پیام بده.')

# ============ پاسخ به اخبار ============
@client.on(events.NewMessage(incoming=True))
async def news_handler(event):
    if event.is_private and 'اخبار' in event.raw_text:
        await event.reply('📰 آخرین اخبار: اینجا خبر میاد...')

# ============ اجرا ============
async def main():
    await client.start(phone=phone)
    print('✅ ربات روشن شد!')
    await client.run_until_disconnected()

# ============ اجرای اصلی ============
if __name__ == '__main__':
    client.loop.run_until_complete(main())