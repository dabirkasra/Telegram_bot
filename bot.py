from telethon import TelegramClient, events
import os

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
phone = os.environ.get('PHONE')

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private and not event.out:
        await event.reply('🔒 پیوی قفل شده! بعداً پیام بده.')

@client.on(events.NewMessage(incoming=True))
async def news_handler(event):
    if event.is_private and 'اخبار' in event.raw_text:
        await event.reply('📰 آخرین اخبار: اینجا خبر میاد...')

async def main():
    await client.start(phone=phone)
    print('✅ ربات روشن شد!')
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
