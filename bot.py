import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

async def main():
    session = AiohttpSession()
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)
    dp = Dispatcher(storage=MemoryStorage())

    @dp.message()
    async def handle_message(message: types.Message):
        await message.reply("Hello! Send me a video or document.")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())