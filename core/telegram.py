import asyncio
from telegram import Bot
from django.conf import settings


async def send_telegram_message_async(message):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(
        chat_id=settings.TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown"
    )


def send_telegram_message(message):
    asyncio.run(send_telegram_message_async(message))
