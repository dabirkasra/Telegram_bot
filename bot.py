from telethon import TelegramClient, events
import asyncio

api_id = 32059999
api_hash = '848e4041e84bff7907db68fd7ac3c37b'  # جدید بذار

# از فایل session استفاده کن
client = TelegramClient('session.session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private and not event.out:
        await event.reply('🔒 پیوی قفل شده! بعداً پیام بده.')

@client.on(events.NewMessage(incoming=True))
async def news_handler(event):
    if event.is_private and 'اخبار' in event.raw_text:
        await event.reply('📰 آخرین اخبار: اینجا خبر میاد...')

async def main():
    await client.start()
    print('✅ ربات روشن شد!')
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())