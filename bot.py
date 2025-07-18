import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

# Setup logging
logging.basicConfig(level=logging.INFO)

# Read BOT_TOKEN from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

# Create Bot instance with default HTML parse mode
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()
)

dp = Dispatcher()

@dp.message()
async def on_forwarded_video(message: types.Message):
    video = message.video
    if not video:
        await message.reply("❌ Please forward a video message.")
        return

    file_id = video.file_id
    try:
        file = await bot.get_file(file_id)
        file_path = file.file_path
        download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        await message.reply(
            f"🎬 <b>File ID:</b>\n<code>{file_id}</code>\n\n"
            f"📥 <b>Download Link:</b>\n<code>{download_link}</code>"
        )
    except Exception as e:
        await message.reply(f"❌ Failed to get file path:\n<code>{e}</code>")

async def main():
    # Remove webhook & pending updates if any
    await bot.delete_webhook(drop_pending_updates=True)
    # Start long polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())