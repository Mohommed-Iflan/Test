import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Set up the bot with parse mode
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message()
async def get_file_id(message: Message):
    if message.video:
        await message.reply(f"🎬 Video file_id:\n<code>{message.video.file_id}</code>")
    elif message.document:
        await message.reply(f"📄 Document file_id:\n<code>{message.document.file_id}</code>")
    else:
        await message.reply("❌ Please send or forward a video or document.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())