import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hcode
from aiogram.utils import executor

from os import getenv

# Replace with your actual token if not using env
BOT_TOKEN = "7511544228:AAGhOAYlausj1uy1018eTp7yaPJcFLg9c9w"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=[ContentType.VIDEO, ContentType.DOCUMENT])
async def handle_file(message: types.Message):
    file_id = message.video.file_id if message.video else message.document.file_id
    try:
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        await message.reply(
            f"✅ Direct File URL:\n{file_url}",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@dp.message_handler()
async def handle_text(message: types.Message):
    await message.reply("📩 Send me a video or document to get the direct file link.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
