import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

async def main():
    session = AiohttpSession()
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    @dp.message()
    async def extract_link(message: types.Message):
        text = message.text.strip()
        if ".mp4" in text and "https://t.me/" in text:
            parts = text.split()
            if len(parts) == 2 and parts[0].endswith(".mp4") and parts[1].startswith("https://t.me/"):
                filename = parts[0]
                link = parts[1]
                await message.reply(f"✅ Filename: <b>{filename}</b>\n🔗 Link: <code>{link}</code>")
                return

        await message.reply("❌ Send in this format:\n<code>filename.mp4 https://t.me/...</code>")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())