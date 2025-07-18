import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties

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
    async def handle_doc_or_video(message: types.Message):
        if message.video:
            file = await bot.get_file(message.video.file_id)
        elif message.document:
            file = await bot.get_file(message.document.file_id)
        else:
            await message.reply("❌ Please send a video or document file.")
            return

        file_path = file.file_path
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        await message.reply(f"✅ Telegram File Link:\n<code>{download_url}</code>")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())