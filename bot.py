import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientSession

# ✅ Load token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

# ✅ Initialize bot and dispatcher
session = AiohttpSession(ClientSession())
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
dp = Dispatcher(storage=MemoryStorage())

# ✅ Respond to any text message
@dp.message(F.text)
async def handle_text(message: Message):
    await message.reply("📩 Received your message!")

# ✅ Respond to video or document messages
@dp.message(F.video | F.document)
async def handle_file(message: Message):
    try:
        file_info = message.video or message.document
        file_id = file_info.file_id
        file_size = file_info.file_size

        # Telegram max file size for download = 20MB for bots without premium
        if file_size > 20 * 1024 * 1024:
            await message.reply("❌ Error: File is too big (Telegram bot limit is 20MB).")
            return

        await message.reply(f"✅ Received file: <b>{file_info.file_name or 'unnamed file'}</b>\nSize: {round(file_size / 1024 / 1024, 2)} MB")

    except Exception as e:
        await message.reply(f"❌ Failed to process file: {e}")

# ✅ Startup
async def main():
    print("✅ Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())