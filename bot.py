import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio
from aiohttp import ClientSession

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

# Logging
logging.basicConfig(level=logging.INFO)

# Main async setup
async def main():
    async with ClientSession() as client:
        session = AiohttpSession(client)
        bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)
        dp = Dispatcher(storage=MemoryStorage())

        @dp.message()
        async def handle_video(message: types.Message):
            if message.video or message.document:
                file = message.video or message.document
                file_id = file.file_id
                try:
                    await bot.send_document(chat_id=message.chat.id, document=file_id)
                except Exception as e:
                    await message.reply(f"❌ Error: {e}")
            else:
                await message.reply("❌ Please send a video or document.")

        await dp.start_polling(bot)

# Start the bot
if __name__ == "__main__":
    asyncio.run(main())