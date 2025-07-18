import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is not set in environment variables!")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message()
async def handle_message(message: Message):
    if message.video:
        await message.reply(f"🎬 Video file_id:\n<code>{message.video.file_id}</code>")
    elif message.document:
        await message.reply(f"📄 Document file_id:\n<code>{message.document.file_id}</code>")
    else:
        await message.reply("❌ Please forward a video or document from Telegram.")


async def main():
    print("✅ Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())